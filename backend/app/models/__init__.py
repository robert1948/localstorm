"""
LocalStorm Models Package
========================

Database models for the LocalStorm application.
"""

from .audit_log import AuditLog, AuditEventType, AuditLogLevel

# Import User directly from models.py to avoid circular imports
import sys
import os
parent_dir = os.path.dirname(os.path.dirname(__file__))
models_path = os.path.join(parent_dir, 'models.py')

# Dynamic import to avoid circular dependency
import importlib.util
spec = importlib.util.spec_from_file_location("models", models_path)
models_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(models_module)
User = models_module.User

__all__ = [
    "AuditLog",
    "AuditEventType", 
    "AuditLogLevel",
    "User"
]
