import time
import uvicorn
from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from utils.logger import logger
from utils.user_operations import (
    is_user_verified, get_user_data, user_exists, register_user, get_user_progress, mark_test_as_completed,
    save_user_progress, check_password
)
from utils.db_operations import create_database_and_tables
from utils.formater import ensure_phone_format, format_name, format_email
from utils.verification_codes import generate_verification_code, store_verification_code, get_verification_code, update_verification_code
from utils.email_operations import send_email
from utils.counter import calculate_suitability_score, get_suitability_description
from utils.email_resend import setup_scheduler
from utils.envs import TOTAL_QUESTIONS

app = FastAPI()

app.add_event_handler("startup", create_database_and_tables)
app.add_event_handler("startup", setup_scheduler)

# app.add_middleware(EnsureTestCompletionMiddleware)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root(request: Request):
    try:
        user_email = request.cookies.get('user_email')
        user_phone = request.cookies.get('user_phone')
        if user_email and user_phone:
            if is_user_verified(user_email, user_phone):
                user_data = get_user_progress(user_email, user_phone)
                if user_data:
                    if not user_data['test_completed']:
                        return RedirectResponse(url="/questions", status_code=303)
                    else:
                        return RedirectResponse(url="/results", status_code=303)
                else:
                    logger.error(f"No user data found for verified user: {user_email}")
                    return RedirectResponse(url="/signup", status_code=303)
            else:
                return RedirectResponse(url="/signup", status_code=303)
        return RedirectResponse(url="/signup", status_code=303)
    except Exception as e:
        logger.error(f"Error processing root endpoint for user {user_email}: {e}")
        return RedirectResponse(url="/signup", status_code=303)

@app.get("/signup")
async def signup(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.post("/signup")
async def handle_signup(request: Request, email: str = Form(...), phone: str = Form(...), name: str = Form(...), surname: str = Form(...), password: str = Form(...)):
    try:
        email = format_email(email)
        phone = ensure_phone_format(phone)
        name = format_name(name)
        surname = format_name(surname)

        if user_exists(email, phone):
            if check_password(email, password):
                if is_user_verified(email, phone):
                    user_data = get_user_data(email, phone)
                    if user_data and not user_data.get('test_completed'):
                        return RedirectResponse(url="/questions", status_code=303)
                    return templates.TemplateResponse("already-registrated.html", {"request": request, "email": email})
                else:
                    return templates.TemplateResponse("verify.html", {"request": request, "email": email})
            else:
                return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid password."})
        else:
            verification_code = generate_verification_code()
            register_user(email, phone, name, surname, verification_code, password)
            store_verification_code(email, verification_code)
            send_email(email, verification_code)
            response = templates.TemplateResponse("verify.html", {"request": request, "email": email})
            response.set_cookie(key="user_email", value=email, httponly=True)
            response.set_cookie(key="user_phone", value=phone, httponly=True)
            return response
    except Exception as e:
        logger.error(f"Error during signup for user {email}: {e}")
        return templates.TemplateResponse("error.html", {"request": request, "error": "An internal error occurred during signup."})


@app.get("/questions")
async def show_questions(request: Request, email: str, password: str):
    user_data = get_user_data(email)
    if user_data and check_password(password, user_data['password_hash']):
        if not is_user_verified(email):
            return RedirectResponse(url="/signup", status_code=303)
        return templates.TemplateResponse("index.html", {"request": request, "user_data": user_data})
    return RedirectResponse(url="/signup", status_code=303)

@app.post('/submit', response_class=HTMLResponse)
async def submit_form(request: Request, email: str = Form(...), password: str = Form(...)):
    user_data = get_user_data(email)
    if user_data and check_password(password, user_data['password_hash']):
        form_data = await request.form()
        responses = {f'q{i+1}': form_data.get(f'q{i+1}') for i in range(TOTAL_QUESTIONS)}

        if any(response is None for response in responses.values()):
            return HTMLResponse(content="All questions must be answered.", status_code=400)

        score = calculate_suitability_score([int(v) for v in responses.values() if v is not None])
        mark_test_as_completed(email, score)
        suitability_description = get_suitability_description(score)
        save_user_progress(email, TOTAL_QUESTIONS, responses)

        response = templates.TemplateResponse('results.html', {
            "request": request,
            "suitability": suitability_description
        })
        return response
    return RedirectResponse(url="/signup", status_code=303)

@app.get("/check_code_expiration")
async def check_code_expiration(request: Request, email: str, password: str):
    user_data = get_user_data(email)
    if user_data and check_password(password, user_data['password_hash']):
        stored_code, timestamp = get_verification_code(email)
        current_time = int(time.time())
        expired = current_time - timestamp > 300
        return {"expired": expired}
    return {"error": "Authentication failed"}

@app.post("/regenerate_code")
async def regenerate_code(request: Request, email: str = Form(...), password: str = Form(...)):
    user_data = get_user_data(email)
    if user_data and check_password(password, user_data['password_hash']):
        new_code = generate_verification_code()
        update_verification_code(email, new_code)
        send_email(email, new_code)
        return {"message": "New verification code sent", "success": True}
    return {"error": "Authentication failed"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8085, log_config=None)
