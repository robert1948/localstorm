"""
Enhanced monitoring and logging for CapeControl
"""
import logging
import time
from typing import Dict, Any
from fastapi import Request, Response
from fastapi.middleware.base import BaseHTTPMiddleware
import json
from datetime import datetime


class MonitoringMiddleware(BaseHTTPMiddleware):
    """
    Middleware for monitoring API performance and usage
    """
    
    def __init__(self, app):
        super().__init__(app)
        self.setup_logging()
    
    def setup_logging(self):
        """Setup structured logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger("capecontrol.monitoring")
        
        # Create separate loggers for different concerns
        self.performance_logger = logging.getLogger("capecontrol.performance")
        self.security_logger = logging.getLogger("capecontrol.security")
        self.error_logger = logging.getLogger("capecontrol.errors")
    
    def log_request_metrics(self, request: Request, response: Response, 
                          processing_time: float):
        """Log request metrics in structured format"""
        metrics = {
            "timestamp": datetime.utcnow().isoformat(),
            "method": request.method,
            "url": str(request.url),
            "path": request.url.path,
            "status_code": response.status_code,
            "processing_time_ms": round(processing_time * 1000, 2),
            "client_ip": request.client.host if request.client else "unknown",
            "user_agent": request.headers.get("user-agent", ""),
            "response_size": response.headers.get("content-length", 0)
        }
        
        # Log performance metrics
        self.performance_logger.info(f"API_REQUEST: {json.dumps(metrics)}")
        
        # Alert on slow requests
        if processing_time > 2.0:  # 2 seconds
            self.logger.warning(f"SLOW_REQUEST: {metrics['path']} took {processing_time:.2f}s")
        
        # Alert on errors
        if response.status_code >= 400:
            error_metrics = {
                **metrics,
                "error_type": "client_error" if response.status_code < 500 else "server_error"
            }
            self.error_logger.error(f"API_ERROR: {json.dumps(error_metrics)}")
    
    def log_security_event(self, request: Request, event_type: str, details: Dict[str, Any]):
        """Log security-related events"""
        security_event = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            "client_ip": request.client.host if request.client else "unknown",
            "path": request.url.path,
            "user_agent": request.headers.get("user-agent", ""),
            "details": details
        }
        self.security_logger.warning(f"SECURITY_EVENT: {json.dumps(security_event)}")
    
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Log incoming request
        self.logger.info(f"Incoming {request.method} {request.url.path}")
        
        try:
            response = await call_next(request)
            processing_time = time.time() - start_time
            
            # Log metrics
            self.log_request_metrics(request, response, processing_time)
            
            return response
            
        except Exception as e:
            processing_time = time.time() - start_time
            self.error_logger.error(f"REQUEST_EXCEPTION: {request.url.path} - {str(e)}")
            raise


# Health check endpoint for monitoring
async def health_check_detailed():
    """Detailed health check with system metrics"""
    import psutil
    import os
    
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "system": {
            "cpu_percent": psutil.cpu_percent(),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_usage": psutil.disk_usage('/').percent,
            "load_average": os.getloadavg() if hasattr(os, 'getloadavg') else None
        },
        "application": {
            "version": "2.0.0",
            "environment": os.getenv("ENVIRONMENT", "development"),
            "database_connected": True  # TODO: Add actual DB health check
        }
    }
