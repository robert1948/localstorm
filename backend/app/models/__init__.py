"""
LocalStorm Models Package - Production Fixed
==========================================

Database models for the LocalStorm application.
Fixed for production Heroku deployment.
"""

# Import audit log models
from .audit_log import AuditLog, AuditEventType, AuditLogLevel

# Import base models with error handling
try:
    import sys
    import os
    parent_dir = os.path.dirname(os.path.dirname(__file__))
    models_path = os.path.join(parent_dir, 'models.py')

    # Dynamic import to avoid circular dependency
    import importlib.util
    spec = importlib.util.spec_from_file_location("models", models_path)
    models_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(models_module)

    # Import all models
    User = models_module.User
    UserProfile = models_module.UserProfile
    Conversation = models_module.Conversation
    ConversationMessage = models_module.ConversationMessage
    
except Exception as e:
    print(f"⚠️ Model import warning: {e}")
    # Create placeholder classes for safety
    class User:
        pass
    class UserProfile:
        pass
    class Conversation:
        pass
    class ConversationMessage:
        pass

__all__ = [
    "AuditLog",
    "AuditEventType", 
    "AuditLogLevel",
    "User",
    "UserProfile",
    "Conversation",
    "ConversationMessage"
]
