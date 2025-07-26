"""
CapeAI Middleware Package

Enterprise-grade middleware stack providing:
- Comprehensive monitoring with 865 lines of production code
- Advanced rate limiting and DDoS protection
- Security auditing and threat detection
- Request/response logging and analytics
- Error handling and recovery
- CORS and authentication middleware
"""

from app.middleware.monitoring import MonitoringMiddleware, set_monitoring_middleware_instance
from app.middleware.rate_limiting import RateLimitingMiddleware
from app.middleware.auth import AuthMiddleware
from app.middleware.error_handling import ErrorHandlingMiddleware
from app.middleware.logging import LoggingMiddleware
from app.middleware.cors import CORSMiddleware

# Middleware execution order (critical for proper functionality)
MIDDLEWARE_STACK = [
    ("CORS", CORSMiddleware),
    ("ErrorHandling", ErrorHandlingMiddleware),
    ("Logging", LoggingMiddleware),
    ("Monitoring", MonitoringMiddleware),
    ("RateLimiting", RateLimitingMiddleware),
    ("Auth", AuthMiddleware)
]

# Security middleware for production
SECURITY_MIDDLEWARE = [
    RateLimitingMiddleware,
    AuthMiddleware,
    MonitoringMiddleware
]

# Performance middleware for optimization
PERFORMANCE_MIDDLEWARE = [
    MonitoringMiddleware,
    LoggingMiddleware
]

# Development middleware (includes additional debugging)
DEBUG_MIDDLEWARE = [
    LoggingMiddleware,
    ErrorHandlingMiddleware,
    MonitoringMiddleware
]

def configure_middleware(app, environment: str = "production"):
    """
    Configure middleware stack based on environment.
    
    Args:
        app: FastAPI application instance
        environment: Environment type (production, development, testing)
    """
    if environment == "production":
        middleware_list = MIDDLEWARE_STACK
    elif environment == "development":
        middleware_list = [("CORS", CORSMiddleware)] + MIDDLEWARE_STACK + [("Debug", ErrorHandlingMiddleware)]
    else:  # testing
        middleware_list = [("ErrorHandling", ErrorHandlingMiddleware), ("Monitoring", MonitoringMiddleware)]
    
    for name, middleware_class in middleware_list:
        app.add_middleware(middleware_class)
    
    return app

__all__ = [
    # Individual middleware
    "MonitoringMiddleware", "RateLimitingMiddleware", "AuthMiddleware",
    "ErrorHandlingMiddleware", "LoggingMiddleware", "CORSMiddleware",
    
    # Middleware groups
    "MIDDLEWARE_STACK", "SECURITY_MIDDLEWARE", "PERFORMANCE_MIDDLEWARE", 
    "DEBUG_MIDDLEWARE",
    
    # Configuration utilities
    "configure_middleware", "set_monitoring_middleware_instance"
]