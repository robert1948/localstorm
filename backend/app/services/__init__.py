"""
CapeAI Business Logic Services Package

Enterprise-grade service layer providing:
- Multi-provider AI integration with intelligent routing
- Advanced analytics and quality scoring
- Real-time monitoring and performance tracking
- User personalization and behavioral adaptation
- Comprehensive security and audit logging
"""

from app.services.cape_ai_service import CapeAIService
from app.services.auth_service import AuthService  
from app.services.user_service import UserService
from app.services.conversation_service import ConversationService
from app.services.monitoring_service import MonitoringService
from app.services.personalization_service import PersonalizationService
from app.services.template_service import TemplateService
from app.services.voice_service import VoiceService
from app.services.profile_service import ProfileService
from app.services.dashboard_service import DashboardService
from app.services.preference_service import PreferenceService
from app.services.analytics_service import AnalyticsService

# Service categories for organized access
CORE_SERVICES = {
    "auth": AuthService,
    "user": UserService,
    "conversation": ConversationService
}

AI_SERVICES = {
    "cape_ai": CapeAIService,
    "personalization": PersonalizationService,
    "template": TemplateService,
    "voice": VoiceService
}

ANALYTICS_SERVICES = {
    "monitoring": MonitoringService,
    "analytics": AnalyticsService
}

USER_SERVICES = {
    "profile": ProfileService,
    "dashboard": DashboardService,
    "preference": PreferenceService
}

# All services for dependency injection
ALL_SERVICES = {
    **CORE_SERVICES,
    **AI_SERVICES, 
    **ANALYTICS_SERVICES,
    **USER_SERVICES
}

# Service initialization helper
def get_service(service_name: str):
    """Get service instance by name for dependency injection."""
    if service_name in ALL_SERVICES:
        return ALL_SERVICES[service_name]()
    raise ValueError(f"Service '{service_name}' not found")

# Service dependency mapping for complex initialization
SERVICE_DEPENDENCIES = {
    "cape_ai": ["user", "conversation", "personalization", "analytics"],
    "analytics": ["monitoring"],
    "dashboard": ["user", "analytics", "personalization"],
    "conversation": ["user", "cape_ai"],
    "personalization": ["user", "analytics"]
}

def initialize_service_with_dependencies(service_name: str, db_session=None):
    """
    Initialize a service with its dependencies.
    
    Args:
        service_name: Name of the service to initialize
        db_session: Database session for services that need it
        
    Returns:
        Initialized service instance with dependencies
    """
    if service_name not in ALL_SERVICES:
        raise ValueError(f"Service '{service_name}' not found")
    
    service_class = ALL_SERVICES[service_name]
    
    # Get dependencies if they exist
    dependencies = SERVICE_DEPENDENCIES.get(service_name, [])
    dep_instances = {}
    
    for dep in dependencies:
        dep_instances[dep] = ALL_SERVICES[dep](db_session) if db_session else ALL_SERVICES[dep]()
    
    # Initialize service with dependencies
    if db_session:
        return service_class(db_session, **dep_instances)
    else:
        return service_class(**dep_instances)

# Service health check functions
def check_service_health(service_name: str) -> dict:
    """
    Check the health status of a specific service.
    
    Args:
        service_name: Name of the service to check
        
    Returns:
        Health status dictionary
    """
    try:
        service = get_service(service_name)
        if hasattr(service, 'health_check'):
            return service.health_check()
        else:
            return {"status": "healthy", "service": service_name, "message": "Service accessible"}
    except Exception as e:
        return {"status": "unhealthy", "service": service_name, "error": str(e)}

def check_all_services_health() -> dict:
    """Check health status of all services."""
    health_status = {
        "overall": "healthy",
        "services": {},
        "timestamp": None
    }
    
    from datetime import datetime
    health_status["timestamp"] = datetime.utcnow().isoformat()
    
    unhealthy_count = 0
    
    for service_name in ALL_SERVICES.keys():
        service_health = check_service_health(service_name)
        health_status["services"][service_name] = service_health
        
        if service_health["status"] != "healthy":
            unhealthy_count += 1
    
    # Set overall status based on individual service health
    if unhealthy_count == 0:
        health_status["overall"] = "healthy"
    elif unhealthy_count <= len(ALL_SERVICES) // 2:
        health_status["overall"] = "degraded"
    else:
        health_status["overall"] = "unhealthy"
    
    health_status["healthy_services"] = len(ALL_SERVICES) - unhealthy_count
    health_status["total_services"] = len(ALL_SERVICES)
    
    return health_status

__all__ = [
    # Individual services
    "CapeAIService", "AuthService", "UserService", "ConversationService",
    "MonitoringService", "PersonalizationService", "TemplateService",
    "VoiceService", "ProfileService", "DashboardService", 
    "PreferenceService", "AnalyticsService",
    
    # Service groups
    "CORE_SERVICES", "AI_SERVICES", "ANALYTICS_SERVICES", "USER_SERVICES",
    "ALL_SERVICES", "SERVICE_DEPENDENCIES",
    
    # Service utilities
    "get_service", "initialize_service_with_dependencies",
    "check_service_health", "check_all_services_health"
]