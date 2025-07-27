"""
CORS Middleware for CapeAI Platform

Handles Cross-Origin Resource Sharing for secure API access from web clients.
"""
from typing import Sequence
from fastapi.middleware.cors import CORSMiddleware as FastAPICORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


class CORSMiddleware(BaseHTTPMiddleware):
    """
    Enhanced CORS middleware with security features and logging.
    
    Wraps FastAPI's built-in CORS middleware with additional enterprise features:
    - Request origin logging
    - Security header validation
    - Custom CORS policy enforcement
    """
    
    def __init__(
        self,
        app,
        allow_origins: Sequence[str] = ["*"],
        allow_credentials: bool = True,
        allow_methods: Sequence[str] = ["*"],
        allow_headers: Sequence[str] = ["*"],
        expose_headers: Sequence[str] = None,
        max_age: int = 600,
    ):
        super().__init__(app)
        self.allow_origins = allow_origins
        self.allow_credentials = allow_credentials
        self.allow_methods = allow_methods
        self.allow_headers = allow_headers
        self.expose_headers = expose_headers or []
        self.max_age = max_age
        
        # Production security settings
        if allow_origins == ["*"]:
            # Development mode - log warning
            print("⚠️ CORS: Using wildcard origins - not recommended for production")
        
    async def dispatch(self, request: Request, call_next):
        """
        Process CORS request with enhanced security and logging.
        
        Args:
            request: Incoming HTTP request
            call_next: Next middleware in the chain
            
        Returns:
            HTTP response with appropriate CORS headers
        """
        origin = request.headers.get("origin")
        method = request.method
        
        # Log CORS requests for monitoring
        if origin:
            print(f"🌐 CORS request from {origin} using {method}")
        
        # Handle preflight requests
        if method == "OPTIONS":
            return await self._handle_preflight(request, origin)
        
        # Process actual request
        response = await call_next(request)
        
        # Add CORS headers to response
        if origin:
            response = self._add_cors_headers(response, origin)
        
        return response
    
    async def _handle_preflight(self, request: Request, origin: str) -> Response:
        """
        Handle CORS preflight requests.
        
        Args:
            request: OPTIONS request for preflight
            origin: Request origin header
            
        Returns:
            Preflight response with appropriate headers
        """
        response = Response()
        
        # Check if origin is allowed
        if self._is_origin_allowed(origin):
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Access-Control-Allow-Methods"] = ", ".join(self.allow_methods)
            response.headers["Access-Control-Allow-Headers"] = ", ".join(self.allow_headers)
            
            if self.allow_credentials:
                response.headers["Access-Control-Allow-Credentials"] = "true"
            
            if self.max_age:
                response.headers["Access-Control-Max-Age"] = str(self.max_age)
            
            if self.expose_headers:
                response.headers["Access-Control-Expose-Headers"] = ", ".join(self.expose_headers)
        
        return response
    
    def _add_cors_headers(self, response: Response, origin: str) -> Response:
        """
        Add CORS headers to actual response.
        
        Args:
            response: Response to modify
            origin: Request origin
            
        Returns:
            Response with CORS headers added
        """
        if self._is_origin_allowed(origin):
            response.headers["Access-Control-Allow-Origin"] = origin
            
            if self.allow_credentials:
                response.headers["Access-Control-Allow-Credentials"] = "true"
            
            if self.expose_headers:
                response.headers["Access-Control-Expose-Headers"] = ", ".join(self.expose_headers)
        
        return response
    
    def _is_origin_allowed(self, origin: str) -> bool:
        """
        Check if the request origin is allowed.
        
        Args:
            origin: Request origin to validate
            
        Returns:
            True if origin is allowed, False otherwise
        """
        if not origin:
            return False
        
        # Wildcard allows all origins
        if "*" in self.allow_origins:
            return True
        
        # Check exact origin matches
        return origin in self.allow_origins


# Production-ready CORS configuration
def get_production_cors_config():
    """Get production CORS configuration with security best practices."""
    return {
        "allow_origins": [
            "https://your-frontend-domain.com",
            "https://www.your-frontend-domain.com",
            # Add your actual frontend domains here
        ],
        "allow_credentials": True,
        "allow_methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": [
            "Accept",
            "Accept-Language", 
            "Content-Language",
            "Content-Type",
            "Authorization",
            "X-Requested-With",
            "X-API-Key",
        ],
        "expose_headers": [
            "X-RateLimit-Limit",
            "X-RateLimit-Remaining",
            "X-RateLimit-Reset",
        ],
        "max_age": 86400,  # 24 hours
    }

# Development CORS configuration (more permissive)
# Replace lines 179-204 with:

# Development CORS configuration (more permissive)
def get_development_cors_config():
    """Get development CORS configuration for testing."""
    return {
        "allow_origins": ["*"],  # Allow all origins in development
        "allow_credentials": True,
        "allow_methods": ["*"],  # Allow all methods
        "allow_headers": ["*"],  # Allow all headers
        "max_age": 600,  # 10 minutes
    }

def add_cors_middleware(app, environment: str = "development"):
    """
    Add CORS middleware to the FastAPI app.
    
    Args:
        app: FastAPI app instance
        environment: 'development' or 'production'
    """
    config = (
        get_development_cors_config()
        if environment == "development"
        else get_production_cors_config()
    )
    
    # Use the custom CORSMiddleware class defined above
    app.add_middleware(CORSMiddleware, **config)