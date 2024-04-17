from fastapi import Request, Response
from fastapi.responses import RedirectResponse
from utils.logger import logger
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from utils.user_operations import is_user_verified, get_user_progress

class EnsureTestCompletionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        try:
            logger.debug(f"Handling request to {request.url.path}")

            if request.url.path.startswith("/static"):
                logger.debug("Request is for static content, bypassing test completion checks.")
                return await call_next(request)

            user_email = request.cookies.get('user_email')
            user_phone = request.cookies.get('user_phone')

            logger.debug(f"Extracted user email: {user_email} and phone: {user_phone}")

            if request.method == "POST":
                logger.debug("POST request detected, proceeding without test completion checks.")
                return await call_next(request)

            if user_email and is_user_verified(user_email, user_phone):
                user_data = get_user_progress(user_email, user_phone)
                logger.debug(f"User verification status: {'verified' if user_data else 'not verified'}")

                if user_data and not user_data['test_completed'] and request.url.path not in ["/questions", "/logout", "/static"]:
                    logger.info(f"Redirecting {user_email} to /questions due to incomplete test.")
                    return RedirectResponse(url="/questions")

            return await call_next(request)
        except Exception as e:
            logger.error(f"Error during request handling: {e}")
            return Response("An internal server error occurred", status_code=500)
