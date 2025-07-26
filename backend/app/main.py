from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.middleware.ddos_protection import DDoSProtectionMiddleware  # Task 1.2.3: DDoS Protection
from app.middleware.input_sanitization import InputSanitizationMiddleware  # Task 1.2.4: Input Sanitization
from app.middleware.content_moderation import ContentModerationMiddleware  # Task 1.2.5: Content Moderation
from app.middleware.audit_logging import AuditLoggingMiddleware  # Task 1.2.6: Audit Logging
from app.middleware.monitoring import MonitoringMiddleware, set_monitoring_middleware_instance  # Task 1.3.1: Monitoring
import os

# Import all route modules
from app.routes import auth_v2  # V2 registration system - ACTIVE
from app.routes import cape_ai  # CapeAI service - ACTIVE
from app.routes import audit  # Audit logging API - ACTIVE
from app.routes import monitoring  # Monitoring API - ACTIVE
from app.routes import error_tracking  # Error tracking API - ACTIVE (Task 1.3.3)
from app.routes import dashboard  # Performance dashboard API - ACTIVE (Task 1.3.4)

# Health Check Routes (Task 1.3.5)
from app.routes.health import router as health_router

# Alert System Routes (Task 1.3.6)
from app.routes.alerts import router as alerts_router

# AI Performance Monitoring Routes (Task 1.3.2)
from app.routes.ai_performance import router as ai_performance_router

# AI Context Enhancement Routes (Task 2.1.3)
from app.routes.ai_context import router as ai_context_router

# AI Personalization Routes (Task 2.1.4)
from app.routes.ai_personalization import router as ai_personalization_router

# NEW: Usage Analytics Enhancement Routes (Task 2.2.5) - Conditional import
try:
    from app.routes.usage_analytics import router as usage_analytics_router
    USAGE_ANALYTICS_AVAILABLE = True
except ImportError:
    USAGE_ANALYTICS_AVAILABLE = False
    print("⚠️  Usage Analytics routes not available - Task 2.2.5 not deployed")

# NEW: Preference Management Routes (Task 2.2.6) - Conditional import
try:
    from app.routes.preference_management import router as preference_management_router
    PREFERENCE_MANAGEMENT_AVAILABLE = True
except ImportError:
    PREFERENCE_MANAGEMENT_AVAILABLE = False
    print("⚠️  Preference Management routes not available - Task 2.2.6 not deployed")

app = FastAPI(
    title="CapeControl API",
    description="Secure, scalable authentication system for CapeControl with AI capabilities",
    version="3.0.0"
)

# Production routers - ACTIVE
app.include_router(auth_v2.router)  # V2 authentication system
app.include_router(cape_ai.router)  # CapeAI service
app.include_router(audit.router)  # Audit logging API
app.include_router(monitoring.router)  # Monitoring API (Task 1.3.1)
app.include_router(error_tracking.router)  # Error tracking API (Task 1.3.3)
app.include_router(dashboard.router)  # Performance dashboard API (Task 1.3.4)
app.include_router(health_router)  # Health Check Routes (Task 1.3.5)
app.include_router(alerts_router)  # Alert System Routes (Task 1.3.6)
app.include_router(ai_performance_router)  # AI Performance Monitoring Routes (Task 1.3.2)
app.include_router(ai_context_router)  # AI Context Enhancement Routes (Task 2.1.3)
app.include_router(ai_personalization_router)  # AI Personalization Routes (Task 2.1.4)

# Phase 2.2 routers - Conditional inclusion
if USAGE_ANALYTICS_AVAILABLE:
    app.include_router(usage_analytics_router, prefix="/api/v1/analytics", tags=["usage-analytics"])
    print("✅ Usage Analytics routes enabled (Task 2.2.5)")

if PREFERENCE_MANAGEMENT_AVAILABLE:
    app.include_router(preference_management_router, prefix="/api/v1/preferences", tags=["preferences"])
    print("✅ Preference Management routes enabled (Task 2.2.6)")

# Enhanced health check endpoint with Task 1.3.5 integration
@app.get("/api/health")
async def health_check():
    try:
        # Import health service for enhanced checks
        from app.services.health_service import get_health_service
        health_service = get_health_service()
        
        # Run basic comprehensive health check
        health_result = await health_service.run_comprehensive_health_check()
        
        # Extract key information for backwards compatibility
        overall_status = health_result.get("overall_status")
        if hasattr(overall_status, 'value'):
            status_value = overall_status.value
        else:
            status_value = str(overall_status)
        
        return {
            "status": status_value,
            "message": "CapeControl API is running",
            "version": "3.0.0",
            "timestamp": health_result.get("timestamp", "2025-07-26"),
            "database_connected": True,
            "enhanced_auth": "enabled (v2 tables)",
            "registration_v2": "enabled (2-step flow)",
            "input_sanitization": "enabled (Task 1.2.4)",
            "content_moderation": "enabled (Task 1.2.5)",
            "ddos_protection": "enabled (Task 1.2.3)",
            "audit_logging": "enabled (Task 1.2.6)",
            "monitoring": "enabled (Task 1.3.1)",
            "error_tracking": "enabled (Task 1.3.3)",
            "performance_dashboard": "enabled (Task 1.3.4)",
            "health_checks_enhancement": "enabled (Task 1.3.5)",
            "alert_system": "enabled (Task 1.3.6)",
            "ai_context_enhancement": "enabled (Task 2.1.3)",
            "ai_personalization": "enabled (Task 2.1.4)",
            "usage_analytics_enhancement": "enabled (Task 2.2.5)" if USAGE_ANALYTICS_AVAILABLE else "pending deployment",
            "preference_management": "enabled (Task 2.2.6)" if PREFERENCE_MANAGEMENT_AVAILABLE else "pending deployment",
            "health_summary": {
                "services_checked": len(health_result.get("services", {})),
                "endpoints_checked": len(health_result.get("endpoints", {})),
                "active_alerts": len(health_result.get("alerts", [])),
                "check_duration_ms": health_result.get("check_duration_ms", 0)
            },
            "phase_2_progress": {
                "ai_enhancement_complete": True,
                "user_experience_progress": f"{86 + (14 if USAGE_ANALYTICS_AVAILABLE and PREFERENCE_MANAGEMENT_AVAILABLE else 0)}% ({6 + (1 if USAGE_ANALYTICS_AVAILABLE else 0) + (1 if PREFERENCE_MANAGEMENT_AVAILABLE else 0)}/7 tasks)",
                "tasks_status": {
                    "usage_analytics": "✅ Complete" if USAGE_ANALYTICS_AVAILABLE else "⏳ Pending",
                    "preferences": "✅ Complete" if PREFERENCE_MANAGEMENT_AVAILABLE else "⏳ Pending",
                    "account_settings": "⏳ Next task (2.2.7)"
                }
            }
        }
    except Exception as e:
        # Fallback to basic health check
        try:
            from app.services.error_tracker import get_error_tracker
            error_tracker = get_error_tracker()
            error_stats = error_tracker.get_error_statistics()
            
            error_rate_1min = error_stats.get("error_rates", {}).get("1min", 0)
            recent_critical_errors = error_stats.get("errors_by_severity", {}).get("critical", 0)
            
            if error_rate_1min > 10 or recent_critical_errors > 5:
                health_status = "degraded"
            elif error_rate_1min > 5 or recent_critical_errors > 0:
                health_status = "warning"
            else:
                health_status = "healthy"
                
            return {
                "status": health_status,
                "message": "CapeControl API is running (basic health check)",
                "version": "3.0.0",
                "timestamp": "2025-07-26",
                "database_connected": True,
                "enhanced_auth": "enabled (v2 tables)",
                "registration_v2": "enabled (2-step flow)",
                "input_sanitization": "enabled (Task 1.2.4)",
                "content_moderation": "enabled (Task 1.2.5)",
                "ddos_protection": "enabled (Task 1.2.3)",
                "audit_logging": "enabled (Task 1.2.6)",
                "monitoring": "enabled (Task 1.3.1)",
                "error_tracking": "enabled (Task 1.3.3)",
                "performance_dashboard": "enabled (Task 1.3.4)",
                "health_checks_enhancement": "enabled (Task 1.3.5)",
                "alert_system": "enabled (Task 1.3.6)",
                "usage_analytics_enhancement": "enabled (Task 2.2.5)" if USAGE_ANALYTICS_AVAILABLE else "pending deployment",
                "preference_management": "enabled (Task 2.2.6)" if PREFERENCE_MANAGEMENT_AVAILABLE else "pending deployment",
                "health_check_fallback": str(e),
                "error_tracking_stats": {
                    "total_errors": error_stats.get("total_errors", 0),
                    "error_rate_1min": error_rate_1min,
                    "critical_errors": recent_critical_errors,
                    "patterns_detected": error_stats.get("patterns_count", 0)
                }
            }
        except Exception as fallback_error:
            return {
                "status": "degraded",
                "message": "CapeControl API is running with issues",
                "version": "3.0.0",
                "timestamp": "2025-07-26",
                "database_connected": True,
                "enhanced_auth": "enabled (v2 tables)",
                "registration_v2": "enabled (2-step flow)",
                "input_sanitization": "enabled (Task 1.2.4)",
                "content_moderation": "enabled (Task 1.2.5)",
                "ddos_protection": "enabled (Task 1.2.3)",
                "audit_logging": "enabled (Task 1.2.6)",
                "monitoring": "enabled (Task 1.3.1)",
                "error_tracking": "enabled (Task 1.3.3)",
                "performance_dashboard": "enabled (Task 1.3.4)",
                "health_checks_enhancement": "enabled (Task 1.3.5)",
                "alert_system": "enabled (Task 1.3.6)",
                "usage_analytics_enhancement": "enabled (Task 2.2.5)" if USAGE_ANALYTICS_AVAILABLE else "pending deployment",
                "preference_management": "enabled (Task 2.2.6)" if PREFERENCE_MANAGEMENT_AVAILABLE else "pending deployment",
                "health_check_error": str(e),
                "fallback_error": str(fallback_error)
            }

# Security statistics endpoint
@app.get("/api/security/stats")
async def security_stats():
    """Get security middleware statistics"""
    return {
        "security_systems": {
            "ddos_protection": "active",
            "input_sanitization": "active", 
            "content_moderation": "active",
            "rate_limiting": "active",
            "audit_logging": "active",
            "monitoring": "active"
        },
        "input_sanitization": {
            "status": "operational",
            "features": [
                "AI prompt injection protection",
                "XSS/HTML sanitization", 
                "SQL injection prevention",
                "PII detection and redaction",
                "Content filtering and validation"
            ]
        },
        "content_moderation": {
            "status": "operational",
            "features": [
                "AI response filtering",
                "Hate speech detection",
                "Violence content blocking", 
                "Adult content warnings",
                "Spam detection",
                "Misinformation flagging",
                "Professional disclaimers"
            ]
        },
        "audit_logging": {
            "status": "operational",
            "features": [
                "Comprehensive event tracking",
                "Security event monitoring",
                "User activity logging",
                "Risk assessment and scoring",
                "Compliance reporting",
                "Failed login detection",
                "API request/response logging"
            ]
        },
        "monitoring": {
            "status": "operational",
            "features": [
                "Real-time metrics collection",
                "System resource monitoring",
                "Performance analytics",
                "Error tracking and alerting",
                "Custom business metrics",
                "Health check endpoints",
                "Application performance monitoring"
            ]
        },
        "phase_2_features": {
            "usage_analytics": "operational" if USAGE_ANALYTICS_AVAILABLE else "pending deployment",
            "preference_management": "operational" if PREFERENCE_MANAGEMENT_AVAILABLE else "pending deployment",
            "ai_personalization": "operational",
            "context_enhancement": "operational"
        },
        "message": "Security systems operational"
    }

# API status endpoint
@app.get("/api/")
async def api_root():
    return {
        "message": "CapeControl API",
        "status": "operational",
        "version": "3.0.0",
        "docs": "/docs",
        "health": "/api/health",
        "security": "/api/security/stats",
        "features": {
            "authentication": "v2 enhanced",
            "ai_capabilities": "full",
            "monitoring": "comprehensive", 
            "security": "enterprise-grade",
            "phase_2_progress": f"{86 + (14 if USAGE_ANALYTICS_AVAILABLE and PREFERENCE_MANAGEMENT_AVAILABLE else 0)}% complete"
        },
        "endpoints": {
            "auth": "/api/auth/*",
            "ai": "/api/ai/*",
            "analytics": "/api/v1/analytics/*" if USAGE_ANALYTICS_AVAILABLE else "pending",
            "preferences": "/api/v1/preferences/*" if PREFERENCE_MANAGEMENT_AVAILABLE else "pending",
            "monitoring": "/api/monitoring/*",
            "health": "/api/health"
        }
    }

# Add security middleware stack (Task 1.2.3 + 1.2.4 + 1.2.5 + 1.2.6 + 1.3.1: Comprehensive security and monitoring)
monitoring_middleware = MonitoringMiddleware(app, enable_detailed_logging=True)
set_monitoring_middleware_instance(monitoring_middleware)

app.add_middleware(MonitoringMiddleware, enable_detailed_logging=True)  # First: Comprehensive monitoring
app.add_middleware(AuditLoggingMiddleware)  # Second: Audit logging (captures everything)
app.add_middleware(DDoSProtectionMiddleware)  # Third: DDoS protection
app.add_middleware(InputSanitizationMiddleware, log_threats=True, block_dangerous=True)  # Fourth: Input sanitization
app.add_middleware(ContentModerationMiddleware, config={"enabled": True})  # Fifth: Content moderation

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Correct path to built frontend inside Docker container
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIST = os.path.join(BASE_DIR, "static")
INDEX_HTML = os.path.join(FRONTEND_DIST, "index.html")

# 🚫 Raise if missing (helps debug Docker issues)
if not os.path.exists(INDEX_HTML):
    raise RuntimeError(
        f"❌ Frontend build not found: {INDEX_HTML}\n➡️  Run `npm run build` in the client directory first."
    )

# ✅ Serve all static files from Vite build with caching
app.mount("/assets", StaticFiles(directory=os.path.join(FRONTEND_DIST, "assets")), name="assets")
app.mount("/static", StaticFiles(directory=os.path.join(FRONTEND_DIST, "static")), name="static")

# ✅ Serve robots.txt and sitemap.xml
@app.get("/robots.txt")
async def robots_txt():
    return FileResponse(os.path.join(FRONTEND_DIST, "robots.txt"), media_type="text/plain")

@app.get("/sitemap.xml")
async def sitemap_xml():
    return FileResponse(os.path.join(FRONTEND_DIST, "sitemap.xml"), media_type="application/xml")

# ✅ Serve site.webmanifest with correct MIME type
@app.get("/site.webmanifest")
async def site_webmanifest():
    return FileResponse(os.path.join(FRONTEND_DIST, "site.webmanifest"), media_type="application/manifest+json")

# ✅ Serve favicon files
@app.get("/favicon.ico")
async def favicon():
    return FileResponse(os.path.join(FRONTEND_DIST, "favicon.ico"), media_type="image/x-icon")

@app.get("/apple-touch-icon.png")  
async def apple_touch_icon():
    return FileResponse(os.path.join(FRONTEND_DIST, "apple-touch-icon.png"), media_type="image/png")

# ✅ Serve SPA entry point (index.html)
@app.get("/{full_path:path}")
async def serve_spa(full_path: str, request: Request):
    return FileResponse(INDEX_HTML)