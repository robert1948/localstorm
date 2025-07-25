"""
Content Moderation Middleware - Task 1.2.5
==========================================

FastAPI middleware for automatic content moderation across API endpoints.
Integrates with existing security middleware stack for comprehensive protection.
"""

from fastapi import Request, Response, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import json
import time
import logging
from typing import Dict, Any, List, Optional
import asyncio

from app.utils.content_moderation import (
    ContentModerator, 
    ModerationLevel, 
    ModerationResult,
    moderate_ai_response,
    moderate_user_content
)

logger = logging.getLogger(__name__)

class ContentModerationMiddleware(BaseHTTPMiddleware):
    """
    Middleware for automatic content moderation of API requests and responses
    
    Features:
    - User input moderation
    - AI response filtering  
    - Context-aware moderation levels
    - Performance monitoring
    - Audit logging
    """
    
    def __init__(self, app, config: Optional[Dict[str, Any]] = None):
        super().__init__(app)
        self.moderator = ContentModerator()
        self.config = config or {}
        self.enabled = self.config.get("enabled", True)
        self.stats = {
            "requests_processed": 0,
            "content_moderated": 0,
            "content_blocked": 0,
            "average_processing_time": 0.0
        }
        
        # Endpoint-specific configurations
        self.endpoint_configs = {
            "/api/ai/prompt": {
                "moderation_level": ModerationLevel.STANDARD,
                "moderate_input": True,
                "moderate_output": True,
                "max_content_length": 8000,
                "require_disclaimers": True
            },
            "/api/ai/conversation": {
                "moderation_level": ModerationLevel.STANDARD,
                "moderate_input": False,
                "moderate_output": True,
                "max_content_length": 10000
            },
            "/api/users/profile": {
                "moderation_level": ModerationLevel.PERMISSIVE,
                "moderate_input": True,
                "moderate_output": False,
                "max_content_length": 2000
            },
            "/api/feedback": {
                "moderation_level": ModerationLevel.STRICT,
                "moderate_input": True,
                "moderate_output": False,
                "max_content_length": 1000
            }
        }
    
    async def dispatch(self, request: Request, call_next) -> Response:
        """Main middleware dispatch method"""
        
        if not self.enabled:
            return await call_next(request)
        
        start_time = time.time()
        
        try:
            # Get endpoint configuration
            endpoint_config = self._get_endpoint_config(request.url.path)
            
            # Skip moderation for non-configured endpoints
            if not endpoint_config:
                return await call_next(request)
            
            # Moderate request content if configured
            if endpoint_config.get("moderate_input", False):
                moderated_request = await self._moderate_request(request, endpoint_config)
                if moderated_request != request:
                    request = moderated_request
            
            # Process the request
            response = await call_next(request)
            
            # Moderate response content if configured  
            if endpoint_config.get("moderate_output", False):
                response = await self._moderate_response(response, endpoint_config, request)
            
            # Update statistics
            processing_time = time.time() - start_time
            self._update_stats(processing_time)
            
            return response
            
        except HTTPException:
            # Re-raise HTTP exceptions (like blocked content)
            raise
        except Exception as e:
            logger.error(f"Content moderation middleware error: {str(e)}")
            # Continue processing on middleware errors
            return await call_next(request)
    
    def _get_endpoint_config(self, path: str) -> Optional[Dict[str, Any]]:
        """Get configuration for specific endpoint"""
        
        # Exact match first
        if path in self.endpoint_configs:
            return self.endpoint_configs[path]
        
        # Pattern matching for dynamic routes
        for pattern, config in self.endpoint_configs.items():
            if self._path_matches_pattern(path, pattern):
                return config
        
        return None
    
    def _path_matches_pattern(self, path: str, pattern: str) -> bool:
        """Check if path matches configuration pattern"""
        
        # Simple pattern matching for now
        # Could be enhanced with regex patterns
        if pattern.endswith("*"):
            return path.startswith(pattern[:-1])
        
        # Path parameters (e.g., /api/ai/conversation/{session_id})
        if "{" in pattern and "}" in pattern:
            pattern_parts = pattern.split("/")
            path_parts = path.split("/")
            
            if len(pattern_parts) != len(path_parts):
                return False
            
            for pattern_part, path_part in zip(pattern_parts, path_parts):
                if not (pattern_part == path_part or 
                       (pattern_part.startswith("{") and pattern_part.endswith("}"))):
                    return False
            return True
        
        return False
    
    async def _moderate_request(self, request: Request, config: Dict[str, Any]) -> Request:
        """Moderate incoming request content"""
        
        try:
            # Only moderate POST/PUT/PATCH requests with JSON bodies
            if request.method not in ["POST", "PUT", "PATCH"]:
                return request
            
            content_type = request.headers.get("content-type", "")
            if "application/json" not in content_type:
                return request
            
            # Read and parse request body
            body = await request.body()
            if not body:
                return request
            
            try:
                data = json.loads(body)
            except json.JSONDecodeError:
                return request
            
            # Moderate text fields in request
            moderated_data = await self._moderate_json_data(
                data, 
                config,
                content_type="user_input"
            )
            
            # Create new request with moderated content
            if moderated_data != data:
                new_body = json.dumps(moderated_data).encode('utf-8')
                
                # Create a new request object with moderated body
                # Note: This is a simplified approach. In production, you might need 
                # more sophisticated request reconstruction
                request._body = new_body
                request.headers.__dict__["_list"] = [
                    (k.encode(), v.encode()) if k.lower() != "content-length" 
                    else (k.encode(), str(len(new_body)).encode())
                    for k, v in request.headers.items()
                ]
            
            return request
            
        except Exception as e:
            logger.error(f"Request moderation error: {str(e)}")
            return request
    
    async def _moderate_response(
        self, 
        response: Response, 
        config: Dict[str, Any],
        request: Request
    ) -> Response:
        """Moderate outgoing response content"""
        
        try:
            # Only moderate JSON responses
            content_type = response.headers.get("content-type", "")
            if "application/json" not in content_type:
                return response
            
            # Read response body
            if hasattr(response, 'body'):
                body = response.body
            else:
                # For streaming responses, we need different handling
                return response
            
            if not body:
                return response
            
            try:
                data = json.loads(body)
            except json.JSONDecodeError:
                return response
            
            # Moderate response content
            moderated_data = await self._moderate_json_data(
                data,
                config, 
                content_type="ai_response",
                request_context=self._extract_request_context(request)
            )
            
            # Create new response with moderated content
            if moderated_data != data:
                new_body = json.dumps(moderated_data).encode('utf-8')
                
                return JSONResponse(
                    content=moderated_data,
                    status_code=response.status_code,
                    headers=dict(response.headers)
                )
            
            return response
            
        except Exception as e:
            logger.error(f"Response moderation error: {str(e)}")
            return response
    
    async def _moderate_json_data(
        self, 
        data: Any, 
        config: Dict[str, Any],
        content_type: str = "user_input",
        request_context: Optional[Dict[str, Any]] = None
    ) -> Any:
        """Recursively moderate text content in JSON data"""
        
        if isinstance(data, dict):
            moderated_dict = {}
            for key, value in data.items():
                moderated_dict[key] = await self._moderate_json_data(
                    value, config, content_type, request_context
                )
            return moderated_dict
        
        elif isinstance(data, list):
            return [
                await self._moderate_json_data(item, config, content_type, request_context)
                for item in data
            ]
        
        elif isinstance(data, str) and self._should_moderate_field(data, config):
            return await self._moderate_text_field(data, config, content_type, request_context)
        
        else:
            return data
    
    def _should_moderate_field(self, text: str, config: Dict[str, Any]) -> bool:
        """Determine if text field should be moderated"""
        
        # Skip very short text
        if len(text) < 10:
            return False
        
        # Check max length
        max_length = config.get("max_content_length", 10000)
        if len(text) > max_length:
            return True  # Definitely moderate long content
        
        # Skip URLs, emails, and other structured data
        structured_patterns = [
            r'^https?://',
            r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
            r'^\d{4}-\d{2}-\d{2}',  # Dates
            r'^[A-Z0-9]{8,}$'       # IDs/tokens
        ]
        
        import re
        for pattern in structured_patterns:
            if re.match(pattern, text):
                return False
        
        return True
    
    async def _moderate_text_field(
        self, 
        text: str, 
        config: Dict[str, Any],
        content_type: str,
        request_context: Optional[Dict[str, Any]]
    ) -> str:
        """Moderate individual text field"""
        
        moderation_level = config.get("moderation_level", ModerationLevel.STANDARD)
        
        try:
            if content_type == "ai_response":
                result = moderate_ai_response(text, request_context, moderation_level)
            else:
                result = moderate_user_content(text, content_type, moderation_level)
            
            # Update stats
            self.stats["content_moderated"] += 1
            if not result.is_safe:
                self.stats["content_blocked"] += 1
            
            # Log moderation actions
            if result.violations:
                logger.info(
                    f"Content moderated: type={content_type}, "
                    f"violations={[v.value for v in result.violations]}, "
                    f"action={result.suggested_action}"
                )
            
            # Handle blocked content
            if result.suggested_action == "block":
                raise HTTPException(
                    status_code=400,
                    detail={
                        "error": "Content moderation violation",
                        "message": result.moderated_content,
                        "violations": [v.value for v in result.violations],
                        "moderation_id": result.metadata.get("processing_timestamp")
                    }
                )
            
            return result.moderated_content
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Text field moderation error: {str(e)}")
            return text  # Return original text on error
    
    def _extract_request_context(self, request: Request) -> Dict[str, Any]:
        """Extract context information from request"""
        
        return {
            "endpoint": request.url.path,
            "method": request.method,
            "user_agent": request.headers.get("user-agent", ""),
            "timestamp": time.time(),
            "client_ip": request.client.host if request.client else None
        }
    
    def _update_stats(self, processing_time: float):
        """Update middleware statistics"""
        
        self.stats["requests_processed"] += 1
        
        # Update average processing time
        current_avg = self.stats["average_processing_time"]
        request_count = self.stats["requests_processed"]
        
        self.stats["average_processing_time"] = (
            (current_avg * (request_count - 1) + processing_time) / request_count
        )
    
    def get_stats(self) -> Dict[str, Any]:
        """Get middleware statistics"""
        return {
            **self.stats,
            "moderation_enabled": self.enabled,
            "configured_endpoints": list(self.endpoint_configs.keys()),
            "moderator_stats": self.moderator.get_moderation_stats()
        }

# Configuration presets for different environments
MODERATION_CONFIGS = {
    "development": {
        "enabled": True,
        "log_level": "DEBUG",
        "default_moderation_level": ModerationLevel.PERMISSIVE.value
    },
    
    "staging": {
        "enabled": True,
        "log_level": "INFO", 
        "default_moderation_level": ModerationLevel.STANDARD.value
    },
    
    "production": {
        "enabled": True,
        "log_level": "WARNING",
        "default_moderation_level": ModerationLevel.STRICT.value
    }
}
