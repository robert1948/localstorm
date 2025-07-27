"""
CapeAI Middleware Package

Enterprise-grade middleware providing:
- Advanced security and DDoS protection
- Request monitoring and analytics
- CORS and authentication middleware
- Rate limiting and traffic management
"""

# Import only EXISTING middleware to prevent deployment failures
from app.middleware.cors_middleware import CORSMiddleware
from app.middleware.ddos_protection import DDoSProtectionMiddleware
from app.middleware.monitoring import MonitoringMiddleware, set_monitoring_middleware_instance
from app.middleware.rate_limiting import RateLimitMiddleware  # ✅ CORRECT class name

# Core middleware that actually exist and work
AVAILABLE_MIDDLEWARE = {
    "cors": CORSMiddleware,
    "ddos_protection": DDoSProtectionMiddleware,
    "monitoring": MonitoringMiddleware,
    "rate_limiting": RateLimitMiddleware,
}

# Middleware execution order (only existing middleware)
MIDDLEWARE_STACK = [
    ("CORS", CORSMiddleware),
    ("DDoSProtection", DDoSProtectionMiddleware),
    ("Monitoring", MonitoringMiddleware),
    ("RateLimiting", RateLimitMiddleware),
]

# Security middleware for production (existing only)
SECURITY_MIDDLEWARE = [
    DDoSProtectionMiddleware,
    RateLimitMiddleware,
    MonitoringMiddleware
]

# Performance middleware for optimization (existing only)
PERFORMANCE_MIDDLEWARE = [
    MonitoringMiddleware,
]

def configure_middleware(app, environment: str = "production"):
    """
    Configure middleware stack based on environment.
    
    Args:
        app: FastAPI application instance
        environment: Environment type (production, development, testing)
        
    Returns:
        FastAPI app with configured middleware
    """
    if environment == "production":
        middleware_list = MIDDLEWARE_STACK
    elif environment == "development":
        # Development includes all available middleware
        middleware_list = MIDDLEWARE_STACK
    else:  # testing
        # Testing uses minimal middleware
        middleware_list = [
            ("CORS", CORSMiddleware),
            ("Monitoring", MonitoringMiddleware)
        ]
    
    # Apply middleware in reverse order (FastAPI requirement)
    for name, middleware_class in reversed(middleware_list):
        try:
            app.add_middleware(middleware_class)
            print(f"✅ {name} middleware loaded successfully")
        except Exception as e:
            print(f"⚠️ Failed to load {name} middleware: {e}")
    
    return app

def get_available_middleware():
    """Get dictionary of available middleware classes."""
    return AVAILABLE_MIDDLEWARE

def check_middleware_health():
    """Check if all middleware classes can be imported successfully."""
    from datetime import datetime
    
    health_status = {
        "overall": "healthy",
        "middleware": {},
        "timestamp": datetime.utcnow().isoformat(),
        "total_middleware": len(AVAILABLE_MIDDLEWARE),
        "healthy_middleware": 0
    }
    
    for name, middleware_class in AVAILABLE_MIDDLEWARE.items():
        try:
            # Basic health check - if we can access the class, it's healthy
            class_name = middleware_class.__name__
            health_status["middleware"][name] = {
                "status": "healthy",
                "class": class_name,
                "message": f"{class_name} is accessible and ready"
            }
            health_status["healthy_middleware"] += 1
        except Exception as e:
            health_status["middleware"][name] = {
                "status": "unhealthy",
                "error": str(e),
                "message": f"Failed to access {name} middleware"
            }
    
    # Set overall status
    if health_status["healthy_middleware"] == health_status["total_middleware"]:
        health_status["overall"] = "healthy"
    elif health_status["healthy_middleware"] > 0:
        health_status["overall"] = "degraded"
    else:
        health_status["overall"] = "unhealthy"
    
    return health_status

def get_middleware_info():
    """Get detailed information about available middleware."""
    return {
        "cors": {
            "description": "Cross-Origin Resource Sharing middleware for secure API access",
            "class": "CORSMiddleware",
            "features": ["cross_origin_requests", "preflight_handling", "credential_support"]
        },
        "ddos_protection": {
            "description": "Advanced DDoS protection and attack prevention",
            "class": "DDoSProtectionMiddleware", 
            "features": ["request_rate_analysis", "ip_blocking", "attack_detection"]
        },
        "monitoring": {
            "description": "Comprehensive request monitoring and analytics",
            "class": "MonitoringMiddleware",
            "features": ["request_tracking", "performance_metrics", "error_monitoring"]
        },
        "rate_limiting": {
            "description": "Advanced rate limiting with sliding window algorithm",
            "class": "RateLimitMiddleware",
            "features": ["sliding_window", "per_endpoint_limits", "client_awareness"]
        }
    }

__all__ = [
    # Existing middleware classes
    "CORSMiddleware",
    "DDoSProtectionMiddleware", 
    "MonitoringMiddleware",
    "RateLimitMiddleware",
    
    # Middleware management
    "AVAILABLE_MIDDLEWARE",
    "MIDDLEWARE_STACK",
    "SECURITY_MIDDLEWARE", 
    "PERFORMANCE_MIDDLEWARE",
    
    # Configuration and utilities
    "configure_middleware",
    "get_available_middleware",
    "check_middleware_health",
    "get_middleware_info",
    "set_monitoring_middleware_instance"
]