from fastapi import Request, Response
from fastapi.responses import RedirectResponse
from utils.logger import logger
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from utils.user_operations import is_user_verified, get_user_progress

class EnsureTestCompletionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        try:
            if request.url.path.startswith("/static") or request.method == "POST":
                return await call_next(request)

            user_email = request.cookies.get('user_email')
            user_phone = request.cookies.get('user_phone')

            logger.debug(f"Middleware processing for {user_email}, {user_phone}")

            if user_email and user_phone:
                verified = is_user_verified(user_email, user_phone)
                logger.debug(f"Verification status: {verified} for {user_email}")

                if verified:
                    user_data = get_user_progress(user_email, user_phone)
                    logger.debug(f"User data: {user_data} for {user_email}")

                    if user_data and not user_data['test_completed'] and request.url.path not in ["/questions", "/logout"]:
                        logger.debug(f"Redirecting {user_email} to questions.")
                        return RedirectResponse(url="/questions")

            return await call_next(request)
        except Exception as e:
            logger.error(f"Error during middleware execution: {e}")
            return Response("An internal server error occurred", status_code=500)
