# backend/app/middleware/audit_logging.py
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

class AuditLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        return response
