"""
Task 1.2.2: AI-Specific Rate Limiting Implementation
Enhanced rate limiting middleware with path-based configurations
"""

import time
from typing import Dict, Tuple
from collections import defaultdict, deque
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware


class AISpecificRateLimitMiddleware(BaseHTTPMiddleware):
    """
    Enhanced rate limiting middleware with AI-specific limits
    Supports different rate limits based on endpoint paths
    """
    
    def __init__(self, app):
        super().__init__(app)
        # Track requests per IP per endpoint type
        self.request_times: Dict[str, Dict[str, deque]] = defaultdict(lambda: defaultdict(deque))
        
        # Rate limit configurations
        self.rate_limits = {
            "ai": {"calls_per_minute": 30, "calls_per_hour": 500},           # AI-specific limits
            "authentication": {"calls_per_minute": 10, "calls_per_hour": 100}, # Auth endpoints
            "registration": {"calls_per_minute": 5, "calls_per_hour": 20},     # Registration
            "general": {"calls_per_minute": 60, "calls_per_hour": 1000},       # General API
        }
    
    def get_client_ip(self, request: Request) -> str:
        """Get client IP address with proxy support"""
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
    
    def get_endpoint_type(self, path: str) -> str:
        """Determine endpoint type based on path for rate limiting"""
        
        # AI endpoints - most restrictive (30/min, 500/hour)
        if path.startswith("/api/ai/"):
            return "ai"
        
        # Authentication endpoints
        if any(auth_path in path for auth_path in ["/auth/login", "/auth/token", "/auth/refresh"]):
            return "authentication"
        
        # Registration endpoints
        if any(reg_path in path for reg_path in ["/auth/register", "/auth/signup", "/register"]):
            return "registration"
        
        # Default to general limits
        return "general"
    
    def clean_old_requests(self, client_ip: str, endpoint_type: str, current_time: float):
        """Remove requests older than 1 hour"""
        requests = self.request_times[client_ip][endpoint_type]
        while requests and current_time - requests[0] > 3600:  # 1 hour
            requests.popleft()
    
    def is_rate_limited(self, client_ip: str, endpoint_type: str, current_time: float) -> Tuple[bool, str]:
        """Check if client has exceeded rate limits for this endpoint type"""
        
        # Get rate limits for this endpoint type
        limits = self.rate_limits[endpoint_type]
        calls_per_minute = limits["calls_per_minute"]
        calls_per_hour = limits["calls_per_hour"]
        
        requests = self.request_times[client_ip][endpoint_type]
        
        # Clean old requests
        self.clean_old_requests(client_ip, endpoint_type, current_time)
        
        # Check requests in last minute
        minute_requests = sum(1 for req_time in requests 
                            if current_time - req_time <= 60)
        if minute_requests >= calls_per_minute:
            return True, f"Rate limit exceeded for {endpoint_type} endpoints: {minute_requests}/{calls_per_minute} requests per minute"
        
        # Check requests in last hour
        hour_requests = len(requests)
        if hour_requests >= calls_per_hour:
            return True, f"Rate limit exceeded for {endpoint_type} endpoints: {hour_requests}/{calls_per_hour} requests per hour"
        
        return False, ""
    
    def get_rate_limit_headers(self, client_ip: str, endpoint_type: str, current_time: float) -> Dict[str, str]:
        """Generate rate limit headers for the response"""
        
        limits = self.rate_limits[endpoint_type]
        requests = self.request_times[client_ip][endpoint_type]
        
        minute_requests = sum(1 for req_time in requests 
                            if current_time - req_time <= 60)
        hour_requests = len(requests)
        
        return {
            "X-RateLimit-Type": endpoint_type,
            "X-RateLimit-Limit-Minute": str(limits["calls_per_minute"]),
            "X-RateLimit-Remaining-Minute": str(max(0, limits["calls_per_minute"] - minute_requests)),
            "X-RateLimit-Limit-Hour": str(limits["calls_per_hour"]),
            "X-RateLimit-Remaining-Hour": str(max(0, limits["calls_per_hour"] - hour_requests)),
        }
    
    async def dispatch(self, request: Request, call_next):
        # Skip rate limiting for health checks and static files
        if request.url.path in ["/api/health", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)
        
        client_ip = self.get_client_ip(request)
        endpoint_type = self.get_endpoint_type(request.url.path)
        current_time = time.time()
        
        # Check rate limits for this endpoint type
        is_limited, message = self.is_rate_limited(client_ip, endpoint_type, current_time)
        if is_limited:
            raise HTTPException(status_code=429, detail=message)
        
        # Record this request
        self.request_times[client_ip][endpoint_type].append(current_time)
        
        response = await call_next(request)
        
        # Add rate limit headers
        headers = self.get_rate_limit_headers(client_ip, endpoint_type, current_time)
        for key, value in headers.items():
            response.headers[key] = value
        
        return response
