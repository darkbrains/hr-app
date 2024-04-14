from fastapi import FastAPI, Request, Form, HTTPException, Response
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import random
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import mysql.connector
from mysql.connector import Error
import bcrypt
import time
import uvicorn
import json
from utils.logger import logger
from starlette.middleware.base import BaseHTTPMiddleware



def create_database_and_tables():
    host = DATABASE_HOST
    user = DATABASE_USER
    passwd = DATABASE_PASSWORD
    database = DATABASE_NAME
    port = DATABASE_PORT

    try:
        conn = mysql.connector.connect(host=host, user=user, passwd=passwd, port=port)
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
            print(f"Database '{database}' created or already exists.")
            conn.database = database

            table_queries = [
                """
                CREATE TABLE IF NOT EXISTS USERS (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    phone VARCHAR(15) NOT NULL,
                    email VARCHAR(255) NOT NULL,
                    name VARCHAR(255) NOT NULL,
                    surname VARCHAR(255) NOT NULL,
                    verification_code VARCHAR(6) DEFAULT NULL,
                    test_completed BOOLEAN DEFAULT FALSE,
                    last_question_completed INT DEFAULT 0,
                    answers JSON DEFAULT NULL,
                    is_verified BOOLEAN DEFAULT FALSE,
                    test_score FLOAT DEFAULT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    UNIQUE(email, phone),
                    INDEX(email),
                    INDEX(phone)
                )
                """,
                """
                CREATE TABLE IF NOT EXISTS VERIFICATION_CODES (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    email VARCHAR(255) NOT NULL,
                    code VARCHAR(6) NOT NULL,
                    timestamp INT NOT NULL,
                    INDEX(email),
                    FOREIGN KEY (email) REFERENCES USERS(email) ON DELETE CASCADE
                )
                """
            ]

            for query in table_queries:
                cursor.execute(query)
            cursor.close()
            conn.close()
            print("Database tables are created successfully.")
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    create_database_and_tables()

class EnsureTestCompletionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        user_email = request.cookies.get('user_email')
        if user_email and is_user_verified(user_email):
            user_data = get_user_progress(user_email)
            if user_data and not user_data['test_completed'] and request.url.path not in ["/answers", "/logout", "/static"]:
                return RedirectResponse(url="/answers")
        response = await call_next(request)
        return response

app.add_middleware(EnsureTestCompletionMiddleware)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

TOTAL_QUESTIONS = 20
DATABASE_HOST = os.environ['MYSQL_HOST']
DATABASE_USER = os.environ['MYSQL_USER']
DATABASE_PASSWORD = os.environ['MYSQL_PASSWORD']
DATABASE_NAME = os.environ['MYSQL_DB']
DATABASE_PORT = os.environ['MYSQL_PORT']
EMAIL_ADDRESS = os.environ['EMAIL_ADDRESS']
EMAIL_PASSWORD = os.environ['EMAIL_PASSWORD']

def create_db_connection():
    try:
        return mysql.connector.connect(
            host=DATABASE_HOST,
            user=DATABASE_USER,
            passwd=DATABASE_PASSWORD,
            database=DATABASE_NAME,
            port=DATABASE_PORT
        )
    except Error as e:
        logger.error(f"Error connecting to MySQL database: {e}")
        return None

def user_exists(email: str, phone: str):
    connection = create_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT COUNT(*) FROM USERS WHERE email = %s OR phone = %s",
                (email, phone)
            )
            result = cursor.fetchone()
            return result[0] > 0
        finally:
            cursor.close()
            connection.close()
    return False

def is_user_verified(email: str) -> bool:
    connection = create_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT is_verified FROM USERS WHERE email = %s",
                (email,)
            )
            result = cursor.fetchone()
            return result[0] if result else False
        finally:
            cursor.close()
            connection.close()
    return False

def get_user_progress(email: str):
    connection = create_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT last_question_completed, answers, test_completed FROM USERS WHERE email = %s",
                (email,)
            )
            result = cursor.fetchone()
            if result:
                print(f"User {email} progress retrieved: {result}")
                return {
                    'last_question_completed': result[0],
                    'answers': json.loads(result[1]) if result[1] else {},
                    'test_completed': result[2]
                }
        finally:
            cursor.close()
            connection.close()
    return None

def store_verification_code(email: str, code: str):
    current_time = int(time.time())
    connection = create_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO VERIFICATION_CODES (email, code, timestamp) VALUES (%s, %s, %s)",
                (email, code, current_time)
            )
            connection.commit()
        finally:
            cursor.close()
            connection.close()

def get_verification_code(email: str):
    connection = create_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT code, timestamp FROM VERIFICATION_CODES WHERE email = %s ORDER BY timestamp DESC LIMIT 1",
                (email,)
            )
            result = cursor.fetchone()
            return result if result else (None, None)
        finally:
            cursor.close()
            connection.close()
    return None, None

def mark_user_as_verified(email: str):
    connection = create_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE USERS SET is_verified = TRUE WHERE email = %s",
                (email,)
            )
            connection.commit()
        finally:
            cursor.close()
            connection.close()

def register_user(email: str, phone: str, name: str, surname: str, verification_code: str):
    connection = create_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO USERS (email, phone, name, surname, verification_code) VALUES (%s, %s, %s, %s, %s)",
                (email, phone, name, surname, verification_code)
            )
            connection.commit()
        finally:
            cursor.close()
            connection.close()



def send_email(receiver_email, code):
    message = MIMEMultipart("alternative")
    message["Subject"] = "Verification Code"
    message["From"] = EMAIL_ADDRESS
    message["To"] = receiver_email
    text = f"Your verification code is: {code}. This code will expire in 5 minutes."
    part1 = MIMEText(text, "plain")
    message.attach(part1)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, receiver_email, message.as_string())

def generate_verification_code():
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])

def calculate_suitability_score(responses):
    max_score = len(responses) * 4
    candidate_score = sum(responses)
    return (candidate_score / max_score) * 100

def get_suitability_description(score):
    if score >= 75:
        return "Highly Suitable"
    elif score >= 50:
        return "Suitable"
    elif score >= 25:
        return "Moderately Suitable"
    elif score > 0:
        return "Slightly Suitable"
    else:
        return "Not Suitable"

def mark_test_as_completed(email: str, score: float):
    connection = create_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE USERS SET test_completed = TRUE, test_score = %s WHERE email = %s",
                (int(score), email)
            )
            connection.commit()
        finally:
            cursor.close()
            connection.close()

def save_user_progress(email: str, last_question_completed: int, answers):
    connection = create_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            answers_json = json.dumps(answers)
            cursor.execute(
                "UPDATE USERS SET last_question_completed = %s, answers = %s WHERE email = %s",
                (last_question_completed, answers_json, email)
            )
            connection.commit()
        finally:
            cursor.close()
            connection.close()

def format_name(name: str) -> str:
    """Capitalize only the first letter of the name, others are lowercase."""
    return name.strip().capitalize()

def ensure_phone_format(phone: str) -> str:
    """Ensure the phone number starts with a + and contains only digits afterwards."""
    phone = phone.strip()
    if not phone.startswith('+'):
        phone = '+' + phone
    return phone

def format_email(email: str) -> str:
    """Convert email to all lowercase."""
    return email.strip().lower()

@app.get("/")
async def root(request: Request):
    user_email = request.cookies.get('user_email')
    if user_email and is_user_verified(user_email):
        user_data = get_user_progress(user_email)
        if user_data and not user_data['test_completed']:
            return RedirectResponse(url="/answers", status_code=303)
    return RedirectResponse(url="/signup", status_code=303)

@app.get("/signup")
async def signup(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.post("/signup")
async def handle_signup(request: Request, email: str = Form(...), phone: str = Form(...), name: str = Form(...), surname: str = Form(...)):
    email = format_email(email)
    phone = ensure_phone_format(phone)
    name = format_name(name)
    surname = format_name(surname)

    if user_exists(email, phone):
        return templates.TemplateResponse("already-registered.html", {"request": request, "email": email, "error": "Email or phone already registered."})

    verification_code = generate_verification_code()
    register_user(email, phone, name, surname, verification_code)

    store_verification_code(email, verification_code)
    send_email(email, verification_code)

    response = templates.TemplateResponse("verify.html", {"request": request, "email": email})
    response.set_cookie(key="user_email", value=email, httponly=True)
    return response



@app.get("/answers")
async def show_answers(request: Request):
    user_email = request.cookies.get('user_email')
    if not user_email:
        return RedirectResponse(url="/signup", status_code=303)

    user_data = get_user_progress(user_email)
    if not user_data or user_data['test_completed']:
        return RedirectResponse(url="/signup", status_code=303)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "last_question_completed": user_data['last_question_completed'],
        "answers": json.dumps(user_data['answers'])
    })


@app.post("/verify")
async def verify(request: Request, email: str = Form(...),
                 code1: str = Form(...), code2: str = Form(...),
                 code3: str = Form(...), code4: str = Form(...),
                 code5: str = Form(...), code6: str = Form(...)):
    full_code = code1 + code2 + code3 + code4 + code5 + code6
    stored_code, timestamp = get_verification_code(email)
    if stored_code is None:
        return templates.TemplateResponse("verify-error.html", {"request": request, "email": email, "error": "Verification code not found"})
    current_time = int(time.time())
    if stored_code == full_code and current_time - timestamp <= 300:
        mark_user_as_verified(email)
        return templates.TemplateResponse("verify-success.html", {"request": request, "email": email})
    else:
        return templates.TemplateResponse("verify-error.html", {"request": request, "email": email, "error": "Invalid verification code or code expired"})


@app.get("/logout")
async def logout(response: Response):
    response = RedirectResponse(url="/signup", status_code=303)
    response.delete_cookie(key="user_email")
    return response

@app.post('/submit', response_class=HTMLResponse)
async def submit_form(request: Request):
    form_data = await request.form()
    responses = {f'q{i+1}': form_data.get(f'q{i+1}') for i in range(TOTAL_QUESTIONS)}

    if any(response is None for response in responses.values()):
        return HTMLResponse(content="All questions must be answered.", status_code=400)

    email = request.cookies.get('user_email')
    if not email:
        return RedirectResponse(url="/signup", status_code=303)

    last_question_completed = TOTAL_QUESTIONS
    score = calculate_suitability_score([int(v) for v in responses.values() if v is not None])
    mark_test_as_completed(email, score)
    suitability_description = get_suitability_description(score)

    response = templates.TemplateResponse('results.html', {"request": request, "suitability": suitability_description})
    response.delete_cookie(key="user_email")
    return response


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8085, log_level="info")
