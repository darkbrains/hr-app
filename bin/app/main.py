import time
import uvicorn
from fastapi import FastAPI, Request, Form
from fastapi import Request
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from utils.logger import logger
from utils.user_operations import is_user_verified, get_user_progress, user_exists, register_user, get_user_data, mark_user_as_verified, mark_test_as_completed, save_user_progress
from utils.db_operations import create_database_and_tables
from utils.completion_middleware import EnsureTestCompletionMiddleware
from utils.formater import ensure_phone_format, format_name, format_email
from utils.verification_codes import generate_verification_code, store_verification_code, get_verification_code
from utils.email_operations import send_email
from utils.counter import calculate_suitability_score, get_suitability_description
from utils.envs import TOTAL_QUESTIONS


app = FastAPI()

app.add_event_handler("startup", create_database_and_tables)
app.add_middleware(EnsureTestCompletionMiddleware)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root(request: Request):
    try:
        user_email = request.cookies.get('user_email')
        user_phone = request.cookies.get('user_phone')
        if user_email and is_user_verified(user_email, user_phone):
            user_data = get_user_progress(user_email, user_phone)
            if user_data and not user_data['test_completed']:
                return RedirectResponse(url="/questions", status_code=303)
        return RedirectResponse(url="/signup", status_code=303)
    except Exception as e:
        logger.error(f"Error in root route: {e}")
        return templates.TemplateResponse("error.html", {"request": request})

@app.get("/signup")
async def signup(request: Request):
    try:
        user_email = request.cookies.get('user_email')
        user_phone = request.cookies.get('user_phone')
        if user_email:
            user_data = get_user_progress(user_email, user_phone)
            if user_data and not user_data['test_completed']:
                return RedirectResponse(url="/questions", status_code=303)
        return templates.TemplateResponse("signup.html", {"request": request})
    except Exception as e:
        logger.error(f"Error in signup route: {e}")
        return templates.TemplateResponse("error.html", {"request": request})

@app.post("/signup")
async def handle_signup(request: Request, email: str = Form(...), phone: str = Form(...), name: str = Form(...), surname: str = Form(...)):
    try:
        email = format_email(email)
        phone = ensure_phone_format(phone)
        name = format_name(name)
        surname = format_name(surname)

        if user_exists(email, phone):
            user_data = get_user_progress(email, phone)
            if user_data and not user_data['test_completed']:
                response = RedirectResponse(url="/questions", status_code=303)
                response.set_cookie(key="user_email", value=email, httponly=True)
                response.set_cookie(key="user_phone", value=phone, httponly=True)
                return response
            return templates.TemplateResponse("already-registered.html", {
                "request": request,
                "email": email,
                "error": "Email or phone already registered, and test completed."
            })

        verification_code = generate_verification_code()
        register_user(email, phone, name, surname, verification_code)
        store_verification_code(email, verification_code)
        send_email(email, verification_code)

        response = templates.TemplateResponse("verify.html", {"request": request, "email": email})
        response.set_cookie(key="user_email", value=email, httponly=True)
        response.set_cookie(key="user_phone", value=phone, httponly=True)
        return response
    except Exception as e:
        logger.error(f"Error handling signup: {e}")
        return templates.TemplateResponse("error.html", {"request": request})

@app.get("/questions")
async def show_answers(request: Request):
    try:
        user_email = request.cookies.get('user_email')
        user_phone = request.cookies.get('user_phone')
        if not user_email or not user_phone:
            return RedirectResponse(url="/signup", status_code=303)

        user_data = get_user_data(user_email, user_phone)
        if not user_data:
            return RedirectResponse(url="/signup", status_code=303)

        return templates.TemplateResponse("index.html", {
            "request": request,
            "user_data": user_data
        })
    except Exception as e:
        logger.error(f"Error showing answers: {e}")
        return templates.TemplateResponse("error.html", {"request": request})

@app.post("/verify")
async def verify(request: Request, code1: str = Form(...), code2: str = Form(...), code3: str = Form(...),
                 code4: str = Form(...), code5: str = Form(...), code6: str = Form(...)):
    try:
        email = request.cookies.get('user_email')
        phone = request.cookies.get('user_phone')

        if not email or not phone:
            return templates.TemplateResponse("verify-error.html", {"request": request, "error": "Session error. Please log in again."})

        full_code = ''.join([code1, code2, code3, code4, code5, code6])
        stored_code, timestamp = get_verification_code(email)

        if stored_code is None:
            return templates.TemplateResponse("verify-error.html", {"request": request, "email": email, "error": "Verification code not found"})

        current_time = int(time.time())
        if stored_code == full_code and current_time - timestamp <= 300:
            mark_user_as_verified(email, phone)
            return templates.TemplateResponse("verify-success.html", {"request": request, "email": email})
        else:
            return templates.TemplateResponse("verify-error.html", {"request": request, "email": email, "error": "Invalid verification code or code expired"})
    except Exception as e:
        logger.error(f"Error during verification: {e}")
        return templates.TemplateResponse("error.html", {"request": request})

@app.get("/logout")
async def logout(request: Request):
    try:
        response = RedirectResponse(url="/signup", status_code=303)
        response.delete_cookie(key="user_email")
        response.delete_cookie(key="user_phone")
        return response
    except Exception as e:
        logger.error(f"Error during logout: {e}")
        return templates.TemplateResponse("error.html", {"request": request})

@app.post('/submit', response_class=HTMLResponse)
async def submit_form(request: Request):
    try:
        form_data = await request.form()
        responses = {f'q{i+1}': form_data.get(f'q{i+1}') for i in range(TOTAL_QUESTIONS)}

        if any(response is None for response in responses.values()):
            return HTMLResponse(content="All questions must be answered.", status_code=400)

        email = request.cookies.get('user_email')
        phone = request.cookies.get('user_phone')
        if not email or not phone:
            return RedirectResponse(url="/signup", status_code=303)

        last_question_completed = TOTAL_QUESTIONS
        score = calculate_suitability_score([int(v) for v in responses.values() if v is not None])
        mark_test_as_completed(email, score, phone)
        suitability_description = get_suitability_description(score)

        save_user_progress(email, last_question_completed, responses, phone)

        response = templates.TemplateResponse('results.html', {
            "request": request,
            "suitability": suitability_description
        })
        response.delete_cookie(key="user_email")
        response.delete_cookie(key="user_phone")
        return response
    except Exception as e:
        logger.error(f"Error during form submission: {e}")
        return templates.TemplateResponse("error.html", {"request": request})

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8085, log_config=None)
