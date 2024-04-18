import time
import uvicorn
import asyncio
from fastapi import FastAPI, Request, Form
from fastapi import Request
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from utils.logger import logger
from utils.user_operations import is_user_verified, get_user_progress, user_exists, register_user, get_user_data, mark_user_as_verified, mark_test_as_completed, save_user_progress, check_password
from utils.db_operations import create_database_and_tables
from utils.completion_middleware import EnsureTestCompletionMiddleware
from utils.formater import ensure_phone_format, format_name, format_email
from utils.verification_codes import generate_verification_code, store_verification_code, get_verification_code, update_verification_code
from utils.email_operations import send_email, send_email_with_delay
from utils.counter import calculate_suitability_score, get_suitability_description
from utils.envs import TOTAL_QUESTIONS
from utils.email_resend import setup_scheduler
from utils.password import hash_password

app = FastAPI()


app.add_event_handler("startup", create_database_and_tables)
app.add_event_handler("startup", setup_scheduler)
# app.add_middleware(EnsureTestCompletionMiddleware)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root(request: Request):
    try:
        return RedirectResponse(url="/signup", status_code=303)
    except Exception as e:
        logger.error(f"Error processing root endpoint: {e}")
        return templates.TemplateResponse("errors.html", {"request": request, "error": "Error processing root endpoint"})


@app.get("/signup")
async def signup(request: Request):
    try:
        return templates.TemplateResponse("signup.html", {"request": request})
    except Exception as e:
        logger.error(f"Failed to render the signup page: {e}")
        return templates.TemplateResponse("error.html", {"request": request, "error": "An error occurred while loading the signup page."})


@app.post("/signup")
async def handle_signup(request: Request, email: str = Form(...), phone: str = Form(...),
                        name: str = Form(...), surname: str = Form(...),
                        password: str = Form(...)):
    try:
        email = format_email(email)
        phone = ensure_phone_format(phone)
        name = format_name(name)
        surname = format_name(surname)

        # Check if user exists
        if user_exists(email, phone):
            # If user exists, check verification status
            if is_user_verified(email, phone):
                # If user is verified, but test not completed, render signup page again
                if not get_user_data(email, phone).get('test_completed'):
                    return templates.TemplateResponse("signup.html", {"request": request, "message": "You are already verified. Please complete the test."})
                # If user is verified and test is completed, show already registered page
                return templates.TemplateResponse("already-registered.html", {"request": request, "email": email})
            else:
                # If user exists but not verified, allow verification
                return templates.TemplateResponse("verify.html", {"request": request, "email": email})
        else:
            # If user does not exist, check password
            if check_password(email, password):
                # If password is correct, proceed to the test page
                hashed_password = hash_password(password)  # Hash the password
                verification_code = generate_verification_code()  # Generate verification code
                register_user(email, phone, name, surname, verification_code, hashed_password)  # Register user
                store_verification_code(email, verification_code)  # Store verification code
                send_email(email, verification_code)  # Send verification email
                return RedirectResponse(url="/questions", status_code=303)
            else:
                # If password is incorrect, render error page
                return templates.TemplateResponse("error.html", {"request": request, "error": "Incorrect password."})
    except Exception as e:
        logger.error(f"Error during signup for user {email}: {e}")
        return templates.TemplateResponse("errors.html", {"request": request, "error": "An internal error occurred during signup."})



@app.get("/questions")
async def show_answers(request: Request):
    try:
        user_email = request.cookies.get('user_email')
        user_phone = request.cookies.get('user_phone')
        if not user_email or not user_phone:
            return RedirectResponse(url="/", status_code=303)

        if not is_user_verified(user_email, user_phone):
            return RedirectResponse(url="/", status_code=303)

        user_data = get_user_data(user_email, user_phone)
        if not user_data:
            return RedirectResponse(url="/", status_code=303)

        return templates.TemplateResponse("index.html", {
            "request": request,
            "user_data": user_data
        })
    except Exception as e:
        logger.error(f"Error showing answers: {e}")
        return templates.TemplateResponse("errors.html", {"request": request})


@app.post("/verify")
async def verify(request: Request, code1: str = Form(...), code2: str = Form(...), code3: str = Form(...),
                 code4: str = Form(...), code5: str = Form(...), code6: str = Form(...)):
    try:
        email = request.cookies.get('user_email')
        phone = request.cookies.get('user_phone')

        full_code = ''.join([code1, code2, code3, code4, code5, code6])
        stored_code, timestamp = get_verification_code(email)

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
        return templates.TemplateResponse("errors.html", {"request": request, "error": "An internal error occurred."})


@app.get("/logout")
async def logout(request: Request):
    try:
        response = RedirectResponse(url="/signup", status_code=303)
        response.delete_cookie(key="user_email")
        response.delete_cookie(key="user_phone")
        return response
    except Exception as e:
        logger.error(f"Error during logout: {e}")
        return templates.TemplateResponse("errors.html", {"request": request})


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

        asyncio.create_task(send_email_with_delay(email, score))

        response = templates.TemplateResponse('results.html', {
            "request": request,
            "suitability": suitability_description
        })
        response.delete_cookie(key="user_email")
        response.delete_cookie(key="user_phone")
        return response
    except Exception as e:
        logger.error(f"Error during form submission: {e}")
        return templates.TemplateResponse("errors.html", {"request": request})


@app.get("/check_code_expiration")
async def check_code_expiration(request: Request):
    try:
        email = request.cookies.get('user_email')
        if not email:
            return {"expired": True}

        stored_code, timestamp = get_verification_code(email)
        current_time = int(time.time())
        expired = current_time - timestamp > 300
        return {"expired": expired}
    except Exception as e:
        logger.error(f"Error checking code expiration for email {email}: {e}")
        return {"error": "An error occurred while checking code expiration."}


@app.post("/regenerate_code")
async def regenerate_code(request: Request):
    try:
        user_email = request.cookies.get('user_email')
        user_phone = request.cookies.get('user_phone')

        if user_email and user_phone:
            new_code = generate_verification_code()
            update_verification_code(user_email, new_code)
            send_email(user_email, new_code)
            return {"message": "New verification code sent", "success": True}
        else:
            return {"message": "Failed to identify user", "success": False}
    except Exception as e:
        logger.error(f"Error regenerating code for {user_email}: {e}")
        return {"error": "An error occurred during code regeneration."}



if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8085, log_config=None)
