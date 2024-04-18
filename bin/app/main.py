import time
import uvicorn
from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi import HTTPException

from fastapi.templating import Jinja2Templates
from utils.logger import logger
from utils.user_operations import (
    is_user_verified, get_user_data, register_user, mark_test_as_completed,
    save_user_progress, check_password, mark_user_as_verified
)
from utils.db_operations import create_database_and_tables
from utils.formater import format_name, format_email
from utils.verification_codes import generate_verification_code, store_verification_code, get_verification_code, update_verification_code
from utils.email_operations import send_email
from utils.counter import calculate_suitability_score, get_suitability_description
from utils.email_resend import setup_scheduler
from utils.envs import TOTAL_QUESTIONS
from utils.password import hash_password
import secrets

tokens = {}

def generate_token(email, phone):
    """Generate a secure token and store it with the user's email and phone as a reference."""
    token = secrets.token_urlsafe()
    tokens[token] = {'email': email, 'phone': phone}
    return token

def get_user_data_from_token(token):
    """Retrieve the email and phone associated with a given token."""
    return tokens.get(token)


def invalidate_token(token):
    """Invalidate a token when it's no longer needed or when the user logs out."""
    if token in tokens:
        del tokens[token]

app = FastAPI()

app.add_event_handler("startup", create_database_and_tables)
app.add_event_handler("startup", setup_scheduler)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return RedirectResponse(url="/signup", status_code=303)

@app.get("/signup")
async def signup(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})


@app.post("/signup")
async def handle_signup(request: Request,
                        email: str = Form(...),
                        phone: str = Form(...),
                        name: str = Form(...),
                        surname: str = Form(...),
                        password: str = Form(...)):
    email = format_email(email)
    name = format_name(name)
    surname = format_name(surname)
    hashed_password = hash_password(password)

    user_data = get_user_data(email, phone)
    if user_data:
        if check_password(email, password):
            is_verified = user_data.get('is_verified', False)
            if is_verified:
                test_completed = user_data.get('test_completed', False)
                if not test_completed:
                    # Generate token and redirect securely
                    token = generate_token(email, phone)  # pass both email and phone
                    response = RedirectResponse(url=f"/questions?token={token}", status_code=303)
                    return response
                else:
                    return templates.TemplateResponse("already-registered.html", {"request": request, "email": email})
            else:
                new_code = generate_verification_code()
                update_verification_code(email, new_code)
                send_email(email, new_code)
                return templates.TemplateResponse("verify.html", {"request": request, "email": email, "phone": phone})
        else:
            raise HTTPException(status_code=401, detail="Incorrect password")
    else:
        verification_code = generate_verification_code()
        register_user(email, phone, name, surname, verification_code, hashed_password)
        store_verification_code(email, verification_code)
        send_email(email, verification_code)
        return templates.TemplateResponse("verify.html", {"request": request, "email": email, "phone": phone})


@app.get("/questions")
async def show_questions(request: Request, token: str):
    token_data = get_user_data_from_token(token)
    if not token_data:
        raise HTTPException(status_code=401, detail="Unauthorized access")

    email = token_data['email']
    phone = token_data['phone']
    user_data = get_user_data(email, phone)
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")

    return templates.TemplateResponse("index.html", {"request": request, "user_data": user_data, "auth_token": token})


@app.post('/submit', response_class=HTMLResponse)
async def submit_form(request: Request, auth_token: str = Form(...)):
    token_data = get_user_data_from_token(auth_token)
    if not token_data:
        return HTMLResponse(content="Session expired or invalid. Please login again.", status_code=401)

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
    mark_test_as_completed(score, email, phone)
    save_user_progress(TOTAL_QUESTIONS, responses, email, phone)

    logger.info(score)

@app.post("/verify")
async def verify(request: Request,
                 email: str = Form(...), phone: str = Form(...),
                 code1: str = Form(...), code2: str = Form(...), code3: str = Form(...),
                 code4: str = Form(...), code5: str = Form(...), code6: str = Form(...)):
    try:
        full_code = ''.join([code1, code2, code3, code4, code5, code6])
        stored_code, timestamp = get_verification_code(email)

        if timestamp is None:
            logger.error(f"No verification code or timestamp found for {email}")
            return templates.TemplateResponse("error.html", {"request": request, "error": "No verification code found. Please request a new code."})

        current_time = int(time.time())
        if stored_code == full_code and current_time - timestamp <= 300:
            mark_user_as_verified(email, phone)
            return templates.TemplateResponse("verify-success.html", {"request": request, "email": email})
        elif current_time - timestamp > 300:
            new_code = generate_verification_code()
            update_verification_code(email, new_code)
            send_email(email, new_code)
            return templates.TemplateResponse("verify.html", {"request": request, "email": email, "error": "Verification code expired. A new code has been sent to your email."})
        else:
            new_code = generate_verification_code()
            update_verification_code(email, new_code)
            send_email(email, new_code)
            return templates.TemplateResponse("verify.html", {"request": request, "email": email, "error": "Invalid verification code. A new code has been sent to your email."})
    except Exception as e:
        logger.error(f"Verification process failed for {email}: {e}")
        return templates.TemplateResponse("error.html", {"request": request, "error": "An internal error occurred."})


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
