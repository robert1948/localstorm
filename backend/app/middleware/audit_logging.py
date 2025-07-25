"""
Audit Logging Middleware for Task 1.2.6 - Audit Logging
=======================================================

Middleware that automatically logs all requests and responses for audit purposes.
Integrates with the comprehensive audit logging system to provide complete event tracking.
"""

import time
import json
import uuid
from typing import Dict, Any, Optional
from datetime import datetime
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.audit_service import get_audit_logger, AuditEventType, AuditLogLevel
from app.auth import get_current_user_from_token


class AuditLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware for comprehensive audit logging of all API requests and responses
    
    Features:
    - Automatic request/response logging
    - Performance metrics tracking
    - Security event detection
    - User activity monitoring
    - Error tracking
    - Compliance support
    """
    
    def __init__(self, app):
        super().__init__(app)
        self.audit_logger = get_audit_logger()
        
        # Configure which endpoints to audit
        self.audit_config = {
            # Always audit these endpoints
            "critical_endpoints": [
                "/api/auth/",
                "/api/admin/",
                "/api/user/",
            ],
            
            # Skip these endpoints (health checks, static files)
            "skip_endpoints": [
                "/api/health",
                "/docs",
                "/redoc",
                "/openapi.json",
                "/favicon.ico"
            ],
            
            # Security-sensitive endpoints
            "security_endpoints": [
                "/api/auth/login",
                "/api/auth/register", 
                "/api/auth/logout",
                "/api/auth/password-reset",
                "/api/user/profile",
                "/api/admin/"
            ]
        }
    
    async def dispatch(self, request: Request, call_next):
        """
        Process request and response with comprehensive audit logging
        """
        start_time = time.time()
        request_id = str(uuid.uuid4())
        
        # Add request ID to request state for tracking
        request.state.request_id = request_id
        
        # Check if this endpoint should be audited
        should_audit = self._should_audit_endpoint(request.url.path)
        
        # Get database session for audit logging
        db = next(get_db())
        
        try:
            # Extract user information from token if available
            user_info = await self._extract_user_info(request)
            
            # Log incoming request if critical endpoint
            if should_audit:
                self._log_request_start(db, request, user_info, request_id)
            
            # Process the request
            response = await call_next(request)
            
            # Calculate processing time
            processing_time = time.time() - start_time
            processing_time_ms = int(processing_time * 1000)
            
            # Log the completed request
            if should_audit:
                self._log_request_complete(
                    db, request, response, user_info, 
                    processing_time_ms, request_id
                )
            
            # Check for security events
            self._check_security_events(
                db, request, response, user_info, processing_time_ms
            )
            
            return response
            
        except Exception as e:
            processing_time = time.time() - start_time
            processing_time_ms = int(processing_time * 1000)
            
            # Log the error
            self._log_request_error(
                db, request, user_info, str(e), processing_time_ms, request_id
            )
            
            raise
        finally:
            db.close()
    
    def _should_audit_endpoint(self, path: str) -> bool:
        """
        Determine if an endpoint should be audited based on configuration
        """
        # Skip certain endpoints
        for skip_pattern in self.audit_config["skip_endpoints"]:
            if skip_pattern in path:
                return False
        
        # Always audit critical endpoints
        for critical_pattern in self.audit_config["critical_endpoints"]:
            if path.startswith(critical_pattern):
                return True
        
        # Audit AI endpoints
        if "/api/ai/" in path:
            return True
        
        # Default: audit most endpoints
        return True
    
    async def _extract_user_info(self, request: Request) -> Dict[str, Any]:
        """
        Extract user information from request if available
        """
        user_info = {
            "user_id": None,
            "user_email": None,
            "user_role": None,
            "authenticated": False
        }
        
        try:
            # Try to get user from Authorization header
            auth_header = request.headers.get("authorization")
            if auth_header and auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]
                # Note: This is a simplified version - in production you'd verify the token
                # user = get_current_user_from_token(token)
                # For now, we'll extract basic info if available
                user_info["authenticated"] = True
                
        except Exception:
            # Token extraction failed - user is anonymous
            pass
        
        return user_info
    
    def _log_request_start(self, 
                          db: Session, 
                          request: Request, 
                          user_info: Dict[str, Any],
                          request_id: str):
        """
        Log the start of a request for critical endpoints
        """
        try:
            # Determine event type based on endpoint
            event_type = self._get_event_type_for_endpoint(request.url.path, request.method)
            
            metadata = {
                "request_id": request_id,
                "request_start": True,
                "content_type": request.headers.get("content-type"),
                "content_length": request.headers.get("content-length"),
                "referer": request.headers.get("referer"),
                "query_params": dict(request.query_params)
            }
            
            self.audit_logger.log_event(
                db=db,
                event_type=event_type,
                event_category="request",
                request=request,
                user_id=user_info.get("user_id"),
                user_email=user_info.get("user_email"),
                user_role=user_info.get("user_role"),
                event_description=f"Request started: {request.method} {request.url.path}",
                metadata=metadata
            )
            
        except Exception as e:
            # Don't let audit logging break the main request
            print(f"Audit logging error in request start: {e}")
    
    def _log_request_complete(self,
                             db: Session,
                             request: Request,
                             response: Response,
                             user_info: Dict[str, Any],
                             processing_time_ms: int,
                             request_id: str):
        """
        Log the completion of a request
        """
        try:
            # Determine if this was successful
            success = 200 <= response.status_code < 400
            
            # Get event type
            event_type = self._get_event_type_for_endpoint(request.url.path, request.method)
            
            metadata = {
                "request_id": request_id,
                "request_complete": True,
                "response_headers": dict(response.headers),
                "processing_time_ms": processing_time_ms,
            }
            
            # Add authentication-specific metadata
            if "/api/auth/" in request.url.path:
                if request.url.path.endswith("/login"):
                    event_type = AuditEventType.USER_LOGIN if success else AuditEventType.LOGIN_FAILED
                elif request.url.path.endswith("/register"):
                    event_type = AuditEventType.USER_REGISTER
                elif request.url.path.endswith("/logout"):
                    event_type = AuditEventType.USER_LOGOUT
            
            # Determine event level based on response
            if response.status_code >= 500:
                event_level = AuditLogLevel.ERROR
            elif response.status_code >= 400:
                event_level = AuditLogLevel.WARNING
            else:
                event_level = AuditLogLevel.INFO
            
            self.audit_logger.log_event(
                db=db,
                event_type=event_type,
                event_category="request",
                request=request,
                user_id=user_info.get("user_id"),
                user_email=user_info.get("user_email"),
                user_role=user_info.get("user_role"),
                event_description=f"Request completed: {request.method} {request.url.path}",
                success=success,
                metadata=metadata,
                status_code=response.status_code,
                response_time_ms=processing_time_ms,
                event_level=event_level
            )
            
        except Exception as e:
            print(f"Audit logging error in request complete: {e}")
    
    def _log_request_error(self,
                          db: Session,
                          request: Request,
                          user_info: Dict[str, Any],
                          error_message: str,
                          processing_time_ms: int,
                          request_id: str):
        """
        Log request errors
        """
        try:
            metadata = {
                "request_id": request_id,
                "request_error": True,
                "processing_time_ms": processing_time_ms,
            }
            
            self.audit_logger.log_event(
                db=db,
                event_type=AuditEventType.SYSTEM_ERROR,
                event_category="error",
                request=request,
                user_id=user_info.get("user_id"),
                user_email=user_info.get("user_email"),
                user_role=user_info.get("user_role"),
                event_description=f"Request error: {request.method} {request.url.path}",
                success=False,
                error_message=error_message,
                metadata=metadata,
                event_level=AuditLogLevel.ERROR
            )
            
        except Exception as e:
            print(f"Audit logging error in request error: {e}")
    
    def _check_security_events(self,
                              db: Session,
                              request: Request,
                              response: Response,
                              user_info: Dict[str, Any],
                              processing_time_ms: int):
        """
        Check for security events that need special attention
        """
        try:
            # Check for failed authentication attempts
            if ("/api/auth/login" in request.url.path and 
                response.status_code == 401):
                
                # Get recent failed attempts from this IP
                ip_address = self._get_client_ip(request)
                recent_failures = self.audit_logger.get_failed_authentication_attempts(
                    db, hours=1, ip_address=ip_address
                )
                
                if len(recent_failures) >= 5:  # Brute force threshold
                    self.audit_logger.log_security_event(
                        db=db,
                        event_type=AuditEventType.BRUTE_FORCE_ATTEMPT,
                        request=request,
                        event_description=f"Potential brute force attack from {ip_address}",
                        threat_indicators=["multiple_failed_logins", "brute_force_pattern"],
                        additional_data={
                            "failed_attempts_count": len(recent_failures),
                            "time_window_hours": 1
                        }
                    )
            
            # Check for slow requests (potential DoS)
            if processing_time_ms > 10000:  # 10 seconds
                self.audit_logger.log_security_event(
                    db=db,
                    event_type=AuditEventType.SUSPICIOUS_ACTIVITY,
                    request=request,
                    event_description=f"Unusually slow request: {processing_time_ms}ms",
                    threat_indicators=["slow_response", "potential_dos"],
                    additional_data={
                        "processing_time_ms": processing_time_ms,
                        "threshold_ms": 10000
                    }
                )
            
            # Check for suspicious user agents
            user_agent = request.headers.get("user-agent", "")
            suspicious_agents = ["bot", "crawler", "spider", "scraper"]
            if any(agent in user_agent.lower() for agent in suspicious_agents):
                if not request.url.path.startswith("/docs"):  # Allow docs access
                    self.audit_logger.log_security_event(
                        db=db,
                        event_type=AuditEventType.SUSPICIOUS_ACTIVITY,
                        request=request,
                        event_description=f"Suspicious user agent detected",
                        threat_indicators=["suspicious_user_agent"],
                        additional_data={
                            "user_agent": user_agent,
                            "endpoint": request.url.path
                        }
                    )
            
        except Exception as e:
            print(f"Security event check error: {e}")
    
    def _get_event_type_for_endpoint(self, path: str, method: str) -> AuditEventType:
        """
        Determine the appropriate audit event type based on endpoint and method
        """
        # Authentication endpoints
        if "/api/auth/login" in path:
            return AuditEventType.USER_LOGIN
        elif "/api/auth/register" in path:
            return AuditEventType.USER_REGISTER
        elif "/api/auth/logout" in path:
            return AuditEventType.USER_LOGOUT
        elif "/api/auth/" in path:
            return AuditEventType.ACCESS_GRANTED
        
        # AI endpoints
        elif "/api/ai/" in path:
            return AuditEventType.AI_PROMPT_SUBMITTED
        
        # Profile endpoints
        elif "/api/user/" in path:
            if method == "GET":
                return AuditEventType.PROFILE_VIEWED
            else:
                return AuditEventType.PROFILE_UPDATED
        
        # Admin endpoints
        elif "/api/admin/" in path:
            return AuditEventType.ADMIN_ACTION
        
        # Default
        else:
            return AuditEventType.ACCESS_GRANTED
    
    def _get_client_ip(self, request: Request) -> str:
        """
        Extract client IP address from request headers
        """
        # Check common proxy headers
        forwarded_for = request.headers.get("x-forwarded-for")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        
        real_ip = request.headers.get("x-real-ip")
        if real_ip:
            return real_ip
        
        # Fallback to direct client IP
        return request.client.host if request.client else "unknown"
