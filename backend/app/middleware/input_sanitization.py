"""
Input Sanitization Middleware
Enterprise-grade input validation and sanitization for security
"""

import re
import html
import json
import logging
from typing import Dict, Any, List, Optional, Union
from fastapi import Request, Response, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import bleach

logger = logging.getLogger(__name__)

class InputSanitizationMiddleware(BaseHTTPMiddleware):
    """
    Enterprise input sanitization middleware for security protection
    Handles XSS prevention, SQL injection protection, and input validation
    """
    
    def __init__(self, app, max_content_length: int = 10 * 1024 * 1024):  # 10MB default
        super().__init__(app)
        self.max_content_length = max_content_length
        
        # Define dangerous patterns
        self.sql_injection_patterns = [
            r'(\bunion\b.*\bselect\b)',
            r'(\bselect\b.*\bfrom\b)',
            r'(\binsert\b.*\binto\b)',
            r'(\bupdate\b.*\bset\b)',
            r'(\bdelete\b.*\bfrom\b)',
            r'(\bdrop\b.*\btable\b)',
            r'(\balter\b.*\btable\b)',
            r'(--|\#|\/\*)',
            r'(\bor\b.*=.*\bor\b)',
            r'(\band\b.*=.*\band\b)',
            r'(\'.*\bor\b.*\')',
            r'(\".*\bor\b.*\")',
        ]
        
        # XSS patterns
        self.xss_patterns = [
            r'<script[^>]*>.*?</script>',
            r'javascript:',
            r'vbscript:',
            r'on\w+\s*=',
            r'<iframe[^>]*>.*?</iframe>',
            r'<object[^>]*>.*?</object>',
            r'<embed[^>]*>.*?</embed>',
            r'<link[^>]*>',
            r'<meta[^>]*>',
        ]
        
        # Compile patterns for performance
        self.compiled_sql_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in self.sql_injection_patterns]
        self.compiled_xss_patterns = [re.compile(pattern, re.IGNORECASE | re.DOTALL) for pattern in self.xss_patterns]
        
        # Allowed HTML tags and attributes for bleach
        self.allowed_tags = ['p', 'br', 'strong', 'em', 'u', 'ol', 'ul', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']
        self.allowed_attributes = {
            '*': ['class', 'id'],
            'a': ['href', 'title'],
            'img': ['src', 'alt', 'width', 'height'],
        }
        
        logger.info("✅ InputSanitizationMiddleware initialized")
    
    async def dispatch(self, request: Request, call_next) -> Response:
        """Process request with comprehensive input sanitization"""
        
        try:
            # Check content length
            if hasattr(request, 'headers') and 'content-length' in request.headers:
                content_length = int(request.headers.get('content-length', 0))
                if content_length > self.max_content_length:
                    logger.warning(f"Request content too large: {content_length} bytes")
                    return JSONResponse(
                        status_code=413,
                        content={"error": "Request entity too large", "max_size": self.max_content_length}
                    )
            
            # Sanitize query parameters
            if request.query_params:
                sanitized_query = self._sanitize_query_params(dict(request.query_params))
                if not sanitized_query['is_safe']:
                    logger.warning(f"Malicious query parameters detected: {sanitized_query['threats']}")
                    return JSONResponse(
                        status_code=400,
                        content={
                            "error": "Invalid input detected",
                            "details": "Query parameters contain potentially malicious content",
                            "threats": sanitized_query['threats']
                        }
                    )
            
            # Sanitize request body for POST/PUT/PATCH requests
            if request.method in ['POST', 'PUT', 'PATCH']:
                try:
                    # Get content type
                    content_type = request.headers.get('content-type', '').lower()
                    
                    if 'application/json' in content_type:
                        # Read and sanitize JSON body
                        body = await request.body()
                        if body:
                            sanitized_body = await self._sanitize_json_body(body)
                            if not sanitized_body['is_safe']:
                                logger.warning(f"Malicious JSON body detected: {sanitized_body['threats']}")
                                return JSONResponse(
                                    status_code=400,
                                    content={
                                        "error": "Invalid input detected",
                                        "details": "Request body contains potentially malicious content",
                                        "threats": sanitized_body['threats']
                                    }
                                )
                    
                    elif 'application/x-www-form-urlencoded' in content_type:
                        # Handle form data
                        try:
                            form_data = await request.form()
                            sanitized_form = self._sanitize_form_data(dict(form_data))
                            if not sanitized_form['is_safe']:
                                logger.warning(f"Malicious form data detected: {sanitized_form['threats']}")
                                return JSONResponse(
                                    status_code=400,
                                    content={
                                        "error": "Invalid input detected",
                                        "details": "Form data contains potentially malicious content",
                                        "threats": sanitized_form['threats']
                                    }
                                )
                        except Exception as e:
                            logger.warning(f"Form data processing error: {e}")
                
                except Exception as e:
                    logger.error(f"Body sanitization error: {e}")
                    # Continue processing if sanitization fails
                    pass
            
            # Process the request
            response = await call_next(request)
            
            # Add security headers
            response.headers["X-Content-Type-Options"] = "nosniff"
            response.headers["X-Frame-Options"] = "DENY"
            response.headers["X-XSS-Protection"] = "1; mode=block"
            response.headers["Content-Security-Policy"] = "default-src 'self'; img-src 'self' https://lightning-s3.s3.amazonaws.com https://lightning-s3.s3.us-east-1.amazonaws.com; manifest-src 'self'"
            
            return response
            
        except Exception as e:
            logger.error(f"Input sanitization middleware error: {e}")
            return JSONResponse(
                status_code=500,
                content={"error": "Internal server error", "details": "Input processing failed"}
            )
    
    def _sanitize_query_params(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Sanitize query parameters"""
        threats = []
        
        for key, value in params.items():
            str_value = str(value)
            
            # Check for SQL injection
            if self._detect_sql_injection(str_value):
                threats.append(f"SQL injection in query param '{key}'")
            
            # Check for XSS
            if self._detect_xss(str_value):
                threats.append(f"XSS attempt in query param '{key}'")
            
            # Check for path traversal
            if self._detect_path_traversal(str_value):
                threats.append(f"Path traversal in query param '{key}'")
        
        return {
            'is_safe': len(threats) == 0,
            'threats': threats
        }
    
    async def _sanitize_json_body(self, body: bytes) -> Dict[str, Any]:
        """Sanitize JSON request body"""
        threats = []
        
        try:
            # Parse JSON
            json_data = json.loads(body.decode('utf-8'))
            
            # Recursively check JSON values
            threats.extend(self._check_json_recursively(json_data, "body"))
            
        except json.JSONDecodeError:
            # Not valid JSON, treat as string
            body_str = body.decode('utf-8', errors='ignore')
            if self._detect_sql_injection(body_str):
                threats.append("SQL injection in request body")
            if self._detect_xss(body_str):
                threats.append("XSS attempt in request body")
        except Exception as e:
            logger.warning(f"JSON sanitization error: {e}")
        
        return {
            'is_safe': len(threats) == 0,
            'threats': threats
        }
    
    def _sanitize_form_data(self, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """Sanitize form data"""
        threats = []
        
        for key, value in form_data.items():
            str_value = str(value)
            
            # Check for SQL injection
            if self._detect_sql_injection(str_value):
                threats.append(f"SQL injection in form field '{key}'")
            
            # Check for XSS
            if self._detect_xss(str_value):
                threats.append(f"XSS attempt in form field '{key}'")
            
            # Check for path traversal
            if self._detect_path_traversal(str_value):
                threats.append(f"Path traversal in form field '{key}'")
        
        return {
            'is_safe': len(threats) == 0,
            'threats': threats
        }
    
    def _check_json_recursively(self, data: Any, path: str) -> List[str]:
        """Recursively check JSON data for threats"""
        threats = []
        
        if isinstance(data, dict):
            for key, value in data.items():
                current_path = f"{path}.{key}"
                threats.extend(self._check_json_recursively(value, current_path))
        
        elif isinstance(data, list):
            for i, item in enumerate(data):
                current_path = f"{path}[{i}]"
                threats.extend(self._check_json_recursively(item, current_path))
        
        elif isinstance(data, str):
            # Check string values
            if self._detect_sql_injection(data):
                threats.append(f"SQL injection in {path}")
            if self._detect_xss(data):
                threats.append(f"XSS attempt in {path}")
            if self._detect_path_traversal(data):
                threats.append(f"Path traversal in {path}")
        
        return threats
    
    def _detect_sql_injection(self, text: str) -> bool:
        """Detect SQL injection patterns"""
        for pattern in self.compiled_sql_patterns:
            if pattern.search(text):
                return True
        return False
    
    def _detect_xss(self, text: str) -> bool:
        """Detect XSS patterns"""
        for pattern in self.compiled_xss_patterns:
            if pattern.search(text):
                return True
        return False
    
    def _detect_path_traversal(self, text: str) -> bool:
        """Detect path traversal attempts"""
        dangerous_patterns = ['../', '..\\', '%2e%2e%2f', '%2e%2e%5c', '....//']
        text_lower = text.lower()
        return any(pattern in text_lower for pattern in dangerous_patterns)
    
    def sanitize_html(self, text: str) -> str:
        """Sanitize HTML content using bleach"""
        try:
            return bleach.clean(text, tags=self.allowed_tags, attributes=self.allowed_attributes)
        except Exception as e:
            logger.warning(f"HTML sanitization error: {e}")
            return html.escape(text)
    
    def sanitize_string(self, text: str) -> str:
        """Basic string sanitization"""
        if not isinstance(text, str):
            return str(text)
        
        # HTML escape
        text = html.escape(text)
        
        # Remove null bytes
        text = text.replace('\x00', '')
        
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text

# Export the middleware
__all__ = ["InputSanitizationMiddleware"]