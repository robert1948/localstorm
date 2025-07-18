"""
Rate limiting middleware for CapeControl API
"""
import time
from typing import Dict, Optional
from fastapi import Request, HTTPException
from fastapi.middleware.base import BaseHTTPMiddleware
from collections import defaultdict, deque


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Rate limiting middleware with sliding window approach
    """
    
    def __init__(self, app, calls_per_minute: int = 60, calls_per_hour: int = 1000):
        super().__init__(app)
        self.calls_per_minute = calls_per_minute
        self.calls_per_hour = calls_per_hour
        self.request_times: Dict[str, deque] = defaultdict(deque)
    
    def get_client_ip(self, request: Request) -> str:
        """Get client IP address"""
        # Check for X-Forwarded-For header (for proxy/load balancer)
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        
        # Check for X-Real-IP header
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip
        
        # Fallback to client host
        return request.client.host if request.client else "unknown"
    
    def clean_old_requests(self, client_ip: str, current_time: float):
        """Remove requests older than 1 hour"""
        while (self.request_times[client_ip] and 
               current_time - self.request_times[client_ip][0] > 3600):
            self.request_times[client_ip].popleft()
    
    def is_rate_limited(self, client_ip: str, current_time: float) -> tuple[bool, str]:
        """Check if client is rate limited"""
        requests = self.request_times[client_ip]
        
        # Clean old requests
        self.clean_old_requests(client_ip, current_time)
        
        # Check requests in last minute
        minute_requests = sum(1 for req_time in requests 
                            if current_time - req_time <= 60)
        if minute_requests >= self.calls_per_minute:
            return True, f"Rate limit exceeded: {minute_requests}/{self.calls_per_minute} requests per minute"
        
        # Check requests in last hour
        hour_requests = len(requests)
        if hour_requests >= self.calls_per_hour:
            return True, f"Rate limit exceeded: {hour_requests}/{self.calls_per_hour} requests per hour"
        
        return False, ""
    
    async def dispatch(self, request: Request, call_next):
        # Skip rate limiting for health checks and static files
        if request.url.path in ["/api/health", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)
        
        client_ip = self.get_client_ip(request)
        current_time = time.time()
        
        # Check rate limits
        is_limited, message = self.is_rate_limited(client_ip, current_time)
        if is_limited:
            raise HTTPException(status_code=429, detail=message)
        
        # Record this request
        self.request_times[client_ip].append(current_time)
        
        response = await call_next(request)
        
        # Add rate limit headers
        response.headers["X-RateLimit-Limit-Minute"] = str(self.calls_per_minute)
        response.headers["X-RateLimit-Limit-Hour"] = str(self.calls_per_hour)
        response.headers["X-RateLimit-Remaining-Minute"] = str(
            max(0, self.calls_per_minute - sum(1 for req_time in self.request_times[client_ip] 
                                             if current_time - req_time <= 60))
        )
        response.headers["X-RateLimit-Remaining-Hour"] = str(
            max(0, self.calls_per_hour - len(self.request_times[client_ip]))
        )
        
        return response


# Configuration for different endpoints
RATE_LIMITS = {
    "authentication": {"calls_per_minute": 10, "calls_per_hour": 100},  # Stricter for auth
    "registration": {"calls_per_minute": 5, "calls_per_hour": 20},     # Very strict for registration  
    "general": {"calls_per_minute": 60, "calls_per_hour": 1000},       # General API
}
