from fastapi import Request, Response
from fastapi.responses import RedirectResponse
from utils.logger import logger
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.base import RequestResponseEndpoint
from utils.user_operations import is_user_verified, get_user_progress

class EnsureTestCompletionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        if request.url.path.startswith("/static"):
            return await call_next(request)

        user_email = request.cookies.get('user_email')
        user_phone = request.cookies.get('user_phone')

        if request.method == "POST":
            return await call_next(request)

        if user_email and is_user_verified(user_email, user_phone):
            user_data = get_user_progress(user_email, user_phone)
            if user_data and not user_data['test_completed'] and request.url.path not in ["/questions", "/logout", "/static"]:
                return RedirectResponse(url="/questions")

        return await call_next(request)
