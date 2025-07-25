"""
Input Sanitization Middleware for LocalStorm v3.0.0
===================================================

Middleware to automatically sanitize and validate inputs across all API endpoints.
Integrates with the input sanitization utility to provide comprehensive protection.

Features:
- Automatic input sanitization for all POST/PUT/PATCH requests
- AI prompt validation for CapeAI endpoints
- Request body sanitization with threat detection
- Logging of sanitization events
- Configurable sanitization levels per endpoint
"""

import json
import logging
from typing import Dict, Any, List, Optional
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from fastapi import HTTPException

from app.utils.input_sanitization import input_sanitizer, SanitizationLevel

logger = logging.getLogger(__name__)

class InputSanitizationMiddleware(BaseHTTPMiddleware):
    """
    Middleware for comprehensive input sanitization and validation
    """
    
    # Endpoint-specific sanitization configurations
    ENDPOINT_CONFIGS = {
        # AI endpoints require strict sanitization
        "/api/ai/prompt": {
            "level": SanitizationLevel.AI_PROMPT,
            "fields": {
                "message": {"field_type": "ai_prompt", "required": True},
                "context": {"field_type": "general_text", "required": False}
            },
            "strict_validation": True
        },
        "/api/ai/": {  # Prefix match for all AI endpoints
            "level": SanitizationLevel.AI_PROMPT,
            "fields": {
                "message": {"field_type": "ai_prompt"},
                "prompt": {"field_type": "ai_prompt"},
                "query": {"field_type": "search"}
            }
        },
        
        # Authentication endpoints
        "/api/auth/v2/register": {
            "level": SanitizationLevel.USER_DATA,
            "fields": {
                "firstName": {"field_type": "user_name", "required": True},
                "lastName": {"field_type": "user_name", "required": True},
                "email": {"field_type": "email", "required": True},
                "company": {"field_type": "general_text"},
                "website": {"field_type": "general_text"},
                "phone": {"field_type": "general_text"}
            }
        },
        "/api/auth/register": {
            "level": SanitizationLevel.USER_DATA,
            "fields": {
                "full_name": {"field_type": "user_name", "required": True},
                "email": {"field_type": "email", "required": True},
                "company_name": {"field_type": "general_text"}
            }
        },
        
        # Search endpoints
        "/api/search": {
            "level": SanitizationLevel.SEARCH,
            "fields": {
                "query": {"field_type": "search_query", "required": True},
                "filters": {"field_type": "general_text"}
            }
        },
        
        # Default configuration for other endpoints
        "default": {
            "level": SanitizationLevel.BASIC,
            "fields": {}
        }
    }
    
    def __init__(self, app, log_threats: bool = True, block_dangerous: bool = True):
        super().__init__(app)
        self.log_threats = log_threats
        self.block_dangerous = block_dangerous
        self.sanitization_stats = {
            "total_requests": 0,
            "sanitized_requests": 0,
            "threats_blocked": 0,
            "threats_detected": {}
        }
        
    async def dispatch(self, request: Request, call_next) -> Response:
        """Process request with input sanitization"""
        self.sanitization_stats["total_requests"] += 1
        
        # Only process requests with body content
        if request.method not in ["POST", "PUT", "PATCH", "DELETE"]:
            return await call_next(request)
            
        # Skip certain endpoints that don't need sanitization
        skip_paths = ["/api/health", "/api/metrics", "/docs", "/redoc", "/openapi.json"]
        if any(request.url.path.startswith(path) for path in skip_paths):
            return await call_next(request)
            
        try:
            # Get request body
            body = await request.body()
            if not body:
                return await call_next(request)
                
            # Parse JSON body
            try:
                request_data = json.loads(body)
            except json.JSONDecodeError:
                # Non-JSON body, skip sanitization
                return await call_next(request)
                
            # Get sanitization configuration for this endpoint
            config = self._get_endpoint_config(request.url.path)
            
            # Sanitize the request data
            sanitization_result = await self._sanitize_request_data(
                request_data, 
                config,
                request.url.path
            )
            
            # Check if request should be blocked
            if self.block_dangerous and not sanitization_result["is_safe"]:
                if sanitization_result["high_risk_threats"]:
                    logger.warning(
                        f"Blocking dangerous request to {request.url.path}: "
                        f"{sanitization_result['high_risk_threats']}"
                    )
                    return JSONResponse(
                        status_code=400,
                        content={
                            "error": "Input validation failed",
                            "message": "Request contains potentially dangerous content",
                            "threats_detected": len(sanitization_result["threats_detected"]),
                            "sanitization_id": sanitization_result["sanitization_id"]
                        }
                    )
            
            # Log sanitization if enabled
            if self.log_threats and sanitization_result["threats_detected"]:
                self._log_sanitization(request, sanitization_result)
                
            # Create new request with sanitized data
            sanitized_body = json.dumps(sanitization_result["sanitized_data"]).encode()
            
            # Create a new request with sanitized body
            sanitized_request = Request(
                scope={
                    **request.scope,
                    "headers": [
                        (name, value) for name, value in request.scope["headers"]
                        if name != b"content-length"
                    ] + [(b"content-length", str(len(sanitized_body)).encode())]
                }
            )
            
            # Replace the body
            sanitized_request._body = sanitized_body
            
            # Continue with sanitized request
            response = await call_next(sanitized_request)
            
            # Add sanitization headers if threats were detected
            if sanitization_result["threats_detected"]:
                response.headers["X-Input-Sanitized"] = "true"
                response.headers["X-Threats-Detected"] = str(len(sanitization_result["threats_detected"]))
                
            return response
            
        except Exception as e:
            logger.error(f"Error in input sanitization middleware: {str(e)}")
            # Continue without sanitization if there's an error
            return await call_next(request)
    
    def _get_endpoint_config(self, path: str) -> Dict[str, Any]:
        """Get sanitization configuration for endpoint"""
        # Exact match first
        if path in self.ENDPOINT_CONFIGS:
            return self.ENDPOINT_CONFIGS[path]
            
        # Prefix matching
        for endpoint_pattern, config in self.ENDPOINT_CONFIGS.items():
            if endpoint_pattern != "default" and path.startswith(endpoint_pattern):
                return config
                
        # Default configuration
        return self.ENDPOINT_CONFIGS["default"]
    
    async def _sanitize_request_data(
        self, 
        data: Dict[str, Any], 
        config: Dict[str, Any],
        endpoint_path: str
    ) -> Dict[str, Any]:
        """Sanitize request data based on configuration"""
        import uuid
        
        sanitization_id = str(uuid.uuid4())[:8]
        sanitized_data = {}
        all_threats = []
        high_risk_threats = []
        total_pii_found = []
        
        level = config.get("level", SanitizationLevel.BASIC)
        field_configs = config.get("fields", {})
        
        self.sanitization_stats["sanitized_requests"] += 1
        
        # Sanitize each field in the data
        for key, value in data.items():
            if isinstance(value, str):
                # Get field-specific configuration
                field_config = field_configs.get(key, {"field_type": "general_text"})
                field_type = field_config.get("field_type", "general_text")
                
                # Perform sanitization
                result = input_sanitizer.sanitize_input(
                    value,
                    level=level,
                    field_type=field_type,
                    preserve_formatting=False
                )
                
                sanitized_data[key] = result["sanitized"]
                
                # Collect threats
                if result["threats_detected"]:
                    field_threats = [f"{key}_{threat}" for threat in result["threats_detected"]]
                    all_threats.extend(field_threats)
                    
                    # Identify high-risk threats
                    high_risk_indicators = [
                        "prompt_injection", "xss_", "sql_injection", 
                        "system_command", "dangerous_html"
                    ]
                    
                    for threat in result["threats_detected"]:
                        if any(indicator in threat for indicator in high_risk_indicators):
                            high_risk_threats.extend([f"{key}_{threat}"])
                            
                # Collect PII findings
                if result["pii_found"]:
                    total_pii_found.extend([f"{key}_{pii}" for pii in result["pii_found"]])
                    
            elif isinstance(value, dict):
                # Recursively sanitize nested objects
                nested_result = await self._sanitize_request_data(
                    value, 
                    {"level": level, "fields": {}},
                    endpoint_path
                )
                sanitized_data[key] = nested_result["sanitized_data"]
                all_threats.extend([f"{key}.{threat}" for threat in nested_result["threats_detected"]])
                high_risk_threats.extend([f"{key}.{threat}" for threat in nested_result["high_risk_threats"]])
                
            elif isinstance(value, list):
                # Sanitize list items
                sanitized_list = []
                for i, item in enumerate(value):
                    if isinstance(item, str):
                        result = input_sanitizer.sanitize_input(
                            item,
                            level=level,
                            field_type="general_text"
                        )
                        sanitized_list.append(result["sanitized"])
                        if result["threats_detected"]:
                            all_threats.extend([f"{key}[{i}]_{threat}" for threat in result["threats_detected"]])
                    else:
                        sanitized_list.append(item)
                        
                sanitized_data[key] = sanitized_list
                
            else:
                # Non-string values pass through unchanged
                sanitized_data[key] = value
        
        # Special handling for AI prompt endpoints
        if endpoint_path.startswith("/api/ai/") and "message" in sanitized_data:
            ai_validation = input_sanitizer.validate_ai_prompt(
                sanitized_data["message"],
                sanitized_data.get("context", {})
            )
            
            # Update with AI-specific validation results
            if not ai_validation["is_ai_safe"]:
                all_threats.extend([f"ai_{threat}" for threat in ai_validation["additional_checks"]])
                high_risk_threats.extend([f"ai_{threat}" for threat in ai_validation["context_threats"]])
                
            # Update message with AI-validated version
            sanitized_data["message"] = ai_validation["sanitized"]
        
        # Update statistics
        for threat in all_threats:
            threat_type = threat.split('_')[0] if '_' in threat else threat
            self.sanitization_stats["threats_detected"][threat_type] = \
                self.sanitization_stats["threats_detected"].get(threat_type, 0) + 1
                
        if high_risk_threats:
            self.sanitization_stats["threats_blocked"] += 1
        
        return {
            "sanitized_data": sanitized_data,
            "threats_detected": all_threats,
            "high_risk_threats": high_risk_threats,
            "pii_found": total_pii_found,
            "is_safe": len(high_risk_threats) == 0,
            "sanitization_id": sanitization_id,
            "endpoint_path": endpoint_path,
            "sanitization_level": level.value
        }
    
    def _log_sanitization(self, request: Request, result: Dict[str, Any]):
        """Log sanitization events"""
        client_ip = request.client.host if request.client else "unknown"
        
        log_data = {
            "sanitization_id": result["sanitization_id"],
            "endpoint": result["endpoint_path"],
            "client_ip": client_ip,
            "threats_detected": len(result["threats_detected"]),
            "high_risk_threats": len(result["high_risk_threats"]),
            "pii_found": len(result["pii_found"]),
            "is_safe": result["is_safe"],
            "level": result["sanitization_level"]
        }
        
        if result["high_risk_threats"]:
            logger.warning(f"High-risk input detected: {json.dumps(log_data)}")
        else:
            logger.info(f"Input sanitized: {json.dumps(log_data)}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get sanitization statistics"""
        return {
            **self.sanitization_stats,
            "threat_detection_rate": (
                self.sanitization_stats["threats_blocked"] / 
                max(1, self.sanitization_stats["sanitized_requests"])
            ) * 100
        }
