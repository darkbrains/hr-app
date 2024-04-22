import time
import uvicorn
from fastapi import FastAPI, Request, Form, Body, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import RequestValidationError
from utils.logger import logger
from utils.user_operations import (
    get_user_data, register_user, mark_test_as_completed,
    save_user_progress, check_password, mark_user_as_verified
)
from utils.db_operations import create_database_and_tables, check_db_health
from utils.formater import format_name, format_email
from utils.verification_codes import generate_verification_code, store_verification_code, get_verification_code, update_verification_code
from utils.email_operations import send_email
from utils.counter import calculate_suitability_score
from utils.envs import TOTAL_QUESTIONS, PORT, ZADARMA_API_KEY, ZADARMA_API_SECRET
from utils.password import hash_password
from utils.tokens import  generate_token, get_user_data_from_token, tokens
from utils.error_messages import get_message
from utils.phone_operations import ZadarmaAPI


api = ZadarmaAPI(ZADARMA_API_KEY, ZADARMA_API_SECRET)

app = FastAPI()

app.add_event_handler("startup", create_database_and_tables)


templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle specific HTTP exceptions."""
    return templates.TemplateResponse("error.html", {"request": request, "error": exc.detail, "status_code": exc.status_code}, status_code=exc.status_code)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle request validation errors."""
    return templates.TemplateResponse("error.html", {"request": request, "error": "Validation error in request parameters.", "status_code": 400}, status_code=400)

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions."""
    logger.error(f"Unexpected error: {str(exc)}")
    return templates.TemplateResponse("error.html", {"request": request, "error": "An internal error occurred. Please try again later.", "status_code": 500}, status_code=500)


@app.get("/")
async def root():
    try:
        logger.info('Handling request for "/". Redirectiong request to "/signup".')
        return RedirectResponse(url="/signup", status_code=303)
    except Exception as e:
        logger.error(f'Unexpected error occurred for "/": {e}')


@app.get("/signup")
async def signup(request: Request):
    try:
        logger.info('Handling request for "/singup"')
        return templates.TemplateResponse("signup.html", {"request": request})
    except Exception as e:
        logger.error(f'Unexpected error occurred for "/singup": {e}')


@app.post("/signup")
async def handle_signup(request: Request, email: str = Form(...), phone: str = Form(...),
                        name: str = Form(None), surname: str = Form(None), password: str = Form(...), lang: str = Form(...)):
    try:
        email = format_email(email)
        name = format_name(name)
        surname = format_name(surname)
        user_data = get_user_data(email, phone)

        if user_data:
            if check_password(email, password):
                is_verified = user_data.get('is_verified', False)
                if is_verified:
                    test_completed = user_data.get('test_completed', False)
                    if not test_completed:
                        token = generate_token(email, phone)
                        return RedirectResponse(url=f"/questions?token={token}&lang={lang}", status_code=303)
                    else:
                        return templates.TemplateResponse("already_registered.html", {"request": request, "email": email, "lang": lang})
                else:
                    token = generate_token(email, phone)
                    new_email_code = generate_verification_code()
                    update_verification_code(email, new_email_code, new_phone_code=None)
                    send_email(email, new_email_code, lang)
                    return templates.TemplateResponse("verify.html", {"request": request, "email": email, "phone": phone, "auth_token": token, "lang": lang})
            else:
                message = get_message('incorrect_password', lang)
                return templates.TemplateResponse("error.html", {"request": request, "error": message, "status_code": 401, "lang": lang})
        else:
            hashed_password = hash_password(password)
            email_verification_code = generate_verification_code()
            phone_verification_code = generate_verification_code()
            register_user(email, phone, name, surname, email_verification_code, phone_verification_code, hashed_password)
            store_verification_code(email, email_verification_code, phone_verification_code)
            send_email(email, email_verification_code, lang)
            token = generate_token(email, phone)
            return templates.TemplateResponse("verify.html", {"request": request, "email": email, "phone": phone, "auth_token": token, "lang": lang})
    except Exception as e:
        logger.error(f'Error during signup for {email}: {e}')
        message = get_message('signup_error', lang)
        return templates.TemplateResponse("error.html", {"request": request, "error": message, "lang": lang, "status_code": 500})


@app.get("/questions")
async def show_questions(request: Request, token: str, lang: str):
    try:
        token_data = get_user_data_from_token(token)
        if not token_data:
            raise HTTPException(status_code=401, detail="Unauthorized access")

        email = token_data['email']
        phone = token_data['phone']
        user_data = get_user_data(email, phone)
        if not user_data:
            raise HTTPException(status_code=404, detail="User not found")

        return templates.TemplateResponse("questions.html", {"request": request, "user_data": user_data, "auth_token": token , "lang": lang})
    except Exception as e:
        logger.error(f'Error displaying questions: {e}')
        message = get_message('questions_error', lang)
        return templates.TemplateResponse("error.html", {"request": request,  "error": message, "lang": lang, "status_code": 500})


@app.post('/submit', response_class=HTMLResponse)
async def submit_form(request: Request, auth_token: str = Form(...), lang: str = Form(...)):
    try:
        token_data = get_user_data_from_token(auth_token)
        if not token_data:
            return HTMLResponse(content="Session expired or invalid. Please log in again.", status_code=401)

        email = token_data['email']
        phone = token_data['phone']
        user_data = get_user_data(email, phone)
        if not user_data:
            return HTMLResponse(content="User not found. Please register or check your details.", status_code=404)

        form_data = await request.form()
        responses = {f'q{i+1}': form_data.get(f'q{i+1}') for i in range(TOTAL_QUESTIONS)}
        if any(response is None for response in responses.values()):
            return HTMLResponse(content="All questions must be answered.", status_code=400)

        score = calculate_suitability_score([int(v) for v in responses.values() if v is not None])
        mark_test_as_completed(email, score, phone, lang)
        save_user_progress(email, TOTAL_QUESTIONS, responses, phone)
        return templates.TemplateResponse("results.html", {"request": request, "lang": lang})
    except Exception as e:
        logger.error(f'Error during form submission: {e}')
        message = get_message('submit_error', lang)
        return templates.TemplateResponse("error.html", {"request": request, "error": message, "lang": lang,  "status_code": 500})


@app.get("/verify")
async def show_verify(request: Request, token: str, lang: str = Form(...)):
    try:
        token_data = get_user_data_from_token(token)
        if not token_data:
            raise HTTPException(status_code=401, detail="Unauthorized access")
        email = token_data['email']
        phone = token_data['phone']
        user_data = get_user_data(email, phone)
        if not user_data:
            raise HTTPException(status_code=404, detail="User not found")

        return templates.TemplateResponse("verify.html", {"request": request, "email": email, "phone": phone, "auth_token": token, "lang": lang})
    except Exception as e:
        logger.error(f'Error displaying verify page: {e}')
        message = get_message('verify_error', lang)
        return templates.TemplateResponse("error.html", {"request": request,  "error": message, "lang": lang, "status_code": 500})


@app.post("/verify")
async def verify(request: Request, email: str = Form(...), phone: str = Form(...), token: str = Form(...),
                 lang: str = Form(...), code_email: str = Form(None), code_phone: str = Form(None)):
    try:
        stored_email_code, stored_phone_code, timestamp = get_verification_code(email)
        current_time = int(time.time())

        if code_email and not code_phone:
            if stored_email_code == code_email and current_time - timestamp <= 300:
                api.send_verification_code(phone, code_phone, lang)
                return templates.TemplateResponse("verify_phone.html", {"request": request, "email": email, "phone": phone, "auth_token": token, "lang": lang, "code_email": code_email})
            else:
                message = get_message('verify_incorrect', lang)
                return templates.TemplateResponse("error.html", {"request": request, "error": message, "lang": lang})

        elif code_phone:
            if stored_phone_code == code_phone and current_time - timestamp <= 300:
                mark_user_as_verified(email, phone)
                return templates.TemplateResponse("verify_success.html", {"request": request, "email": email, "auth_token": token, "lang": lang})
            else:
                message = get_message('verify_incorrect', lang)
                return templates.TemplateResponse("error.html", {"request": request, "error": message, "lang": lang})

        else:
            message = get_message('verify_missing_code', lang)
            return templates.TemplateResponse("error.html", {"request": request, "error": message, "lang": lang})

    except Exception as e:
        logger.error(f"Verification process failed for {email}: {e}")
        message = get_message('verify_error', lang)
        return templates.TemplateResponse("error.html", {"request": request, "error": message, "lang": lang, "status_code": 500})


@app.post("/api/v1/check_code_expiration")
async def check_code_expiration(request: Request, data: dict = Body(...)):
    email = data.get('email')
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    user_data = tokens.get(token)
    if user_data and user_data['email'] == email:
        try:
            code, timestamp = get_verification_code(email)
            if not code:
                return {"expired": True}
            current_time = int(time.time())
            expired = current_time - timestamp > 300
            return {"expired": expired}
        except Exception as e:
            logger.error(f'Unexpected error occurred for "/check_code_expiration": {e}')
            return {"error": "Failed to check codes expiration. Please try again later."}
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")


@app.post("/api/v1/regenerate_code")
async def regenerate_code(request: Request, data: dict = Body(...)):
    email = data.get('email')
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    user_data = tokens.get(token)
    if user_data and user_data['email'] == email:
        try:
            new_email_code = generate_verification_code()
            new_phone_code = generate_verification_code()
            update_verification_code(email, new_email_code, new_phone_code)
            return JSONResponse(content={"success": True})
        except Exception as e:
            logger.error(f'Error regenerating codes for {email}: {e}')
            return JSONResponse(content={"success": False, "error": "Failed to regenerate codes. Please try again."})
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")


@app.post("/api/v1/check-user")
async def check_user_exists(request: Request, email: str = Form(...), phone: str = Form(...)):
    user_data = get_user_data(email, phone)
    exists = bool(user_data)
    return JSONResponse(content={"exists": exists})


@app.get("/api/v1/healthz")
async def health_check(request: Request):
    """Health check endpoint to verify database connectivity."""
    try:
        if check_db_health():
            return {"status": "Healthy"}
        else:
            return templates.TemplateResponse(
                "error.html",
                {
                    "request": request,
                    "error": "Database connection is unhealthy.",
                    "status_code": 503
                },
                status_code=503
            )
    except Exception as e:
        logger.error(f"Error in  health_check(): {e}")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(PORT), log_config=None)
