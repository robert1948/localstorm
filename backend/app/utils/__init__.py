"""
CapeAI Utilities Package

Comprehensive utility functions for enterprise AI platform:
- Security and encryption utilities
- Input validation and sanitization  
- Redis caching and session management
- Email notifications and alerts
- File handling and processing
- General helper functions
"""

from app.utils.security import (
    hash_password, 
    verify_password, 
    create_access_token,
    verify_token,
    encrypt_data,
    decrypt_data,
    sanitize_input,
    detect_pii
)

from app.utils.validation import (
    validate_email,
    validate_password_strength,
    validate_api_key,
    validate_json_structure,
    sanitize_html,
    validate_user_input
)

from app.utils.caching import (
    get_redis_client,
    cache_set,
    cache_get,
    cache_delete,
    cache_exists,
    cache_expire,
    get_cached_or_compute
)

from app.utils.email import (
    send_email,
    send_notification,
    send_alert,
    format_email_template,
    EmailService
)

from app.utils.file_utils import (
    save_uploaded_file,
    delete_file,
    get_file_info,
    validate_file_type,
    process_audio_file,
    FileManager
)

from app.utils.helpers import (
    generate_uuid,
    format_datetime,
    parse_datetime,
    calculate_similarity,
    extract_keywords,
    rate_limit_key,
    get_client_ip,
    format_response
)

# Utility categories for organized access
SECURITY_UTILS = {
    "hash_password": hash_password,
    "verify_password": verify_password,
    "create_access_token": create_access_token,
    "verify_token": verify_token,
    "encrypt_data": encrypt_data,
    "decrypt_data": decrypt_data,
    "sanitize_input": sanitize_input,
    "detect_pii": detect_pii
}

VALIDATION_UTILS = {
    "validate_email": validate_email,
    "validate_password_strength": validate_password_strength,
    "validate_api_key": validate_api_key,
    "validate_json_structure": validate_json_structure,
    "sanitize_html": sanitize_html,
    "validate_user_input": validate_user_input
}

CACHING_UTILS = {
    "get_redis_client": get_redis_client,
    "cache_set": cache_set,
    "cache_get": cache_get,
    "cache_delete": cache_delete,
    "cache_exists": cache_exists,
    "cache_expire": cache_expire,
    "get_cached_or_compute": get_cached_or_compute
}

EMAIL_UTILS = {
    "send_email": send_email,
    "send_notification": send_notification,
    "send_alert": send_alert,
    "format_email_template": format_email_template,
    "EmailService": EmailService
}

FILE_UTILS = {
    "save_uploaded_file": save_uploaded_file,
    "delete_file": delete_file,
    "get_file_info": get_file_info,
    "validate_file_type": validate_file_type,
    "process_audio_file": process_audio_file,
    "FileManager": FileManager
}

HELPER_UTILS = {
    "generate_uuid": generate_uuid,
    "format_datetime": format_datetime,
    "parse_datetime": parse_datetime,
    "calculate_similarity": calculate_similarity,
    "extract_keywords": extract_keywords,
    "rate_limit_key": rate_limit_key,
    "get_client_ip": get_client_ip,
    "format_response": format_response
}

# All utilities for comprehensive access
ALL_UTILS = {
    **SECURITY_UTILS,
    **VALIDATION_UTILS,
    **CACHING_UTILS,
    **EMAIL_UTILS,
    **FILE_UTILS,
    **HELPER_UTILS
}

# Utility helper functions
def get_util(util_name: str):
    """Get utility function by name."""
    if util_name in ALL_UTILS:
        return ALL_UTILS[util_name]
    raise ValueError(f"Utility '{util_name}' not found")

def get_utils_by_category(category: str) -> dict:
    """
    Get all utilities in a specific category.
    
    Args:
        category: One of 'security', 'validation', 'caching', 'email', 'file', 'helper'
        
    Returns:
        Dictionary of utility functions in the category
    """
    category_map = {
        "security": SECURITY_UTILS,
        "validation": VALIDATION_UTILS,
        "caching": CACHING_UTILS,
        "email": EMAIL_UTILS,
        "file": FILE_UTILS,
        "helper": HELPER_UTILS
    }
    
    if category not in category_map:
        raise ValueError(f"Category '{category}' not found. Available: {list(category_map.keys())}")
    
    return category_map[category]

def list_available_utils() -> dict:
    """List all available utilities organized by category."""
    return {
        "security": list(SECURITY_UTILS.keys()),
        "validation": list(VALIDATION_UTILS.keys()),
        "caching": list(CACHING_UTILS.keys()),
        "email": list(EMAIL_UTILS.keys()),
        "file": list(FILE_UTILS.keys()),
        "helper": list(HELPER_UTILS.keys()),
        "total_count": len(ALL_UTILS)
    }

# Common utility combinations for frequent use cases
AUTHENTICATION_UTILS = {
    "hash_password": hash_password,
    "verify_password": verify_password,
    "create_access_token": create_access_token,
    "verify_token": verify_token,
    "validate_email": validate_email,
    "validate_password_strength": validate_password_strength
}

AI_PROCESSING_UTILS = {
    "sanitize_input": sanitize_input,
    "detect_pii": detect_pii,
    "validate_user_input": validate_user_input,
    "calculate_similarity": calculate_similarity,
    "extract_keywords": extract_keywords,
    "format_response": format_response
}

MONITORING_UTILS = {
    "generate_uuid": generate_uuid,
    "format_datetime": format_datetime,
    "parse_datetime": parse_datetime,
    "get_client_ip": get_client_ip,
    "rate_limit_key": rate_limit_key
}

VOICE_PROCESSING_UTILS = {
    "save_uploaded_file": save_uploaded_file,
    "validate_file_type": validate_file_type,
    "process_audio_file": process_audio_file,
    "get_file_info": get_file_info,
    "delete_file": delete_file
}

# Quick access patterns
def create_secure_session(user_data: dict) -> dict:
    """Create a secure user session with all necessary components."""
    from datetime import datetime, timedelta
    
    session_id = generate_uuid()
    access_token = create_access_token(user_data)
    
    session_data = {
        "session_id": session_id,
        "access_token": access_token,
        "user_id": user_data.get("user_id"),
        "created_at": format_datetime(datetime.utcnow()),
        "expires_at": format_datetime(datetime.utcnow() + timedelta(hours=24)),
        "ip_address": user_data.get("ip_address"),
        "user_agent": user_data.get("user_agent", "unknown")
    }
    
    # Cache session data
    cache_key = f"session:{session_id}"
    cache_set(cache_key, session_data, expire=86400)  # 24 hours
    
    return session_data

def validate_and_sanitize_ai_input(user_input: str, context: dict = None) -> dict:
    """Comprehensive validation and sanitization for AI inputs."""
    result = {
        "is_valid": True,
        "sanitized_input": user_input,
        "warnings": [],
        "blocked_content": [],
        "metadata": {}
    }
    
    # Basic validation
    if not validate_user_input(user_input):
        result["is_valid"] = False
        result["warnings"].append("Invalid input format")
        return result
    
    # Sanitize input
    sanitized = sanitize_input(user_input)
    result["sanitized_input"] = sanitized
    
    # PII detection
    pii_detected = detect_pii(user_input)
    if pii_detected:
        result["warnings"].append("PII detected and sanitized")
        result["blocked_content"].extend(pii_detected)
    
    # HTML sanitization
    html_sanitized = sanitize_html(user_input)
    if html_sanitized != user_input:
        result["warnings"].append("HTML content sanitized")
        result["sanitized_input"] = html_sanitized
    
    # Extract keywords for context
    keywords = extract_keywords(result["sanitized_input"])
    result["metadata"]["keywords"] = keywords
    result["metadata"]["length"] = len(result["sanitized_input"])
    result["metadata"]["processed_at"] = format_datetime(datetime.utcnow())
    
    return result

__all__ = [
    # Security utilities
    "hash_password", "verify_password", "create_access_token", "verify_token",
    "encrypt_data", "decrypt_data", "sanitize_input", "detect_pii",
    
    # Validation utilities
    "validate_email", "validate_password_strength", "validate_api_key",
    "validate_json_structure", "sanitize_html", "validate_user_input",
    
    # Caching utilities
    "get_redis_client", "cache_set", "cache_get", "cache_delete",
    "cache_exists", "cache_expire", "get_cached_or_compute",
    
    # Email utilities
    "send_email", "send_notification", "send_alert", 
    "format_email_template", "EmailService",
    
    # File utilities
    "save_uploaded_file", "delete_file", "get_file_info",
    "validate_file_type", "process_audio_file", "FileManager",
    
    # Helper utilities
    "generate_uuid", "format_datetime", "parse_datetime",
    "calculate_similarity", "extract_keywords", "rate_limit_key",
    "get_client_ip", "format_response",
    
    # Utility categories
    "SECURITY_UTILS", "VALIDATION_UTILS", "CACHING_UTILS",
    "EMAIL_UTILS", "FILE_UTILS", "HELPER_UTILS", "ALL_UTILS",
    
    # Utility combinations
    "AUTHENTICATION_UTILS", "AI_PROCESSING_UTILS", "MONITORING_UTILS", 
    "VOICE_PROCESSING_UTILS",
    
    # Utility management functions
    "get_util", "get_utils_by_category", "list_available_utils",
    
    # High-level utility functions
    "create_secure_session", "validate_and_sanitize_ai_input"
]