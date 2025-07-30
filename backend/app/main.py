from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

# Import only EXISTING middleware
from app.middleware.input_sanitization import InputSanitizationMiddleware
from app.middleware.content_moderation import ContentModerationMiddleware
from app.middleware.monitoring import MonitoringMiddleware, set_monitoring_middleware_instance
import os

from app.routes import auth_v2, cape_ai, audit, monitoring, error_tracking, dashboard
from app.routes.health import router as health_router
from app.routes.alerts import router as alerts_router
from app.routes.ai_performance import router as ai_performance_router
from app.routes.ai_context import router as ai_context_router
from app.routes.ai_personalization import router as ai_personalization_router

# Optional routes with graceful fallbacks
try:
    from app.routes.usage_analytics import router as usage_analytics_router
    USAGE_ANALYTICS_AVAILABLE = True
except ImportError:
    USAGE_ANALYTICS_AVAILABLE = False
    print("⚠️  Usage Analytics routes not available - Task 2.2.5 not deployed")

try:
    from app.routes.preference_management import router as preference_management_router
    PREFERENCE_MANAGEMENT_AVAILABLE = True
except ImportError:
    PREFERENCE_MANAGEMENT_AVAILABLE = False
    print("⚠️  Preference Management routes not available - Task 2.2.6 not deployed")

# Optional middleware with graceful fallbacks
DDOS_PROTECTION_AVAILABLE = False
AUDIT_LOGGING_AVAILABLE = False

try:
    from app.middleware.ddos_protection import DDoSProtectionMiddleware
    DDOS_PROTECTION_AVAILABLE = True
    print("✅ DDoS Protection middleware available")
except ImportError:
    print("⚠️  DDoS Protection middleware not available")

try:
    from app.middleware.audit_logging import AuditLoggingMiddleware
    AUDIT_LOGGING_AVAILABLE = True
    print("✅ Audit Logging middleware available")
except ImportError:
    print("⚠️  Audit Logging middleware not available")

app = FastAPI(
    title="CapeControl API",
    description="Secure, scalable authentication system for CapeControl with AI capabilities",
    version="3.0.0"
)

# Include routers
app.include_router(auth_v2.router)
app.include_router(cape_ai.router)
app.include_router(audit.router)
app.include_router(monitoring.router)
app.include_router(error_tracking.router)
app.include_router(dashboard.router)
app.include_router(health_router)
app.include_router(alerts_router)
app.include_router(ai_performance_router)
app.include_router(ai_context_router)
app.include_router(ai_personalization_router)

if USAGE_ANALYTICS_AVAILABLE:
    app.include_router(usage_analytics_router, prefix="/api/v1/analytics", tags=["usage-analytics"])
    print("✅ Usage Analytics routes enabled (Task 2.2.5)")

if PREFERENCE_MANAGEMENT_AVAILABLE:
    app.include_router(preference_management_router, prefix="/api/v1/preferences", tags=["preferences"])
    print("✅ Preference Management routes enabled (Task 2.2.6)")

# Initialize monitoring middleware (REQUIRED)
monitoring_middleware = MonitoringMiddleware(app)
set_monitoring_middleware_instance(monitoring_middleware)

# Add middleware in correct order (reverse order of execution)
# CORS should be last (executed first)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add EXISTING middleware with error handling
try:
    app.add_middleware(ContentModerationMiddleware, strict_mode=False)
    print("✅ ContentModerationMiddleware added successfully")
except Exception as e:
    print(f"❌ Failed to add ContentModerationMiddleware: {e}")

try:
    app.add_middleware(InputSanitizationMiddleware, max_content_length=10*1024*1024)
    print("✅ InputSanitizationMiddleware added successfully")
except Exception as e:
    print(f"❌ Failed to add InputSanitizationMiddleware: {e}")

# Add OPTIONAL middleware only if available
if AUDIT_LOGGING_AVAILABLE:
    try:
        app.add_middleware(AuditLoggingMiddleware)
        print("✅ AuditLoggingMiddleware added successfully")
    except Exception as e:
        print(f"❌ Failed to add AuditLoggingMiddleware: {e}")

if DDOS_PROTECTION_AVAILABLE:
    try:
        app.add_middleware(DDoSProtectionMiddleware)
        print("✅ DDoSProtectionMiddleware added successfully")
    except Exception as e:
        print(f"❌ Failed to add DDoSProtectionMiddleware: {e}")

# Static files configuration with Heroku-compatible fallbacks
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIST = os.path.join(BASE_DIR, "static")
INDEX_HTML = os.path.join(FRONTEND_DIST, "index.html")

# Create missing static files for Heroku deployment
if not os.path.exists(INDEX_HTML):
    print(f"⚠️  Frontend build not found: {INDEX_HTML}")
    print("ℹ️  Creating minimal index.html for Heroku deployment")
    os.makedirs(FRONTEND_DIST, exist_ok=True)
    with open(INDEX_HTML, 'w') as f:
        f.write("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CapeControl API</title>
</head>
<body>
    <h1>CapeControl API</h1>
    <p>API is running successfully!</p>
    <p><a href="/docs">View API Documentation</a></p>
    <p><a href="/health">Health Check</a></p>
</body>
</html>""")

# Ensure static directories exist
os.makedirs(os.path.join(FRONTEND_DIST, "assets"), exist_ok=True)
os.makedirs(os.path.join(FRONTEND_DIST, "static"), exist_ok=True)

# Mount static files with error handling
try:
    app.mount("/assets", StaticFiles(directory=os.path.join(FRONTEND_DIST, "assets")), name="assets")
    app.mount("/static", StaticFiles(directory=os.path.join(FRONTEND_DIST, "static")), name="static")
    print("✅ Static file directories mounted successfully")
except Exception as e:
    print(f"❌ Failed to mount static directories: {e}")

@app.get("/robots.txt")
async def robots_txt():
    try:
        return FileResponse(os.path.join(FRONTEND_DIST, "robots.txt"), media_type="text/plain")
    except:
        return "User-agent: *\nDisallow: /api/\nAllow: /"

@app.get("/sitemap.xml")
async def sitemap_xml():
    try:
        return FileResponse(os.path.join(FRONTEND_DIST, "sitemap.xml"), media_type="application/xml")
    except:
        return '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"></urlset>'

@app.get("/site.webmanifest")
async def site_webmanifest():
    try:
        return FileResponse(os.path.join(FRONTEND_DIST, "site.webmanifest"), media_type="application/manifest+json")
    except:
        return {"name": "CapeControl API", "short_name": "CapeControl", "start_url": "/"}

@app.get("/favicon.ico")
async def favicon():
    try:
        return FileResponse(os.path.join(FRONTEND_DIST, "favicon.ico"), media_type="image/x-icon")
    except:
        from fastapi.responses import Response
        return Response("", media_type="image/x-icon")

@app.get("/apple-touch-icon.png")
async def apple_touch_icon():
    try:
        return FileResponse(os.path.join(FRONTEND_DIST, "apple-touch-icon.png"), media_type="image/png")
    except:
        from fastapi.responses import Response
        return Response("", media_type="image/png")

@app.get("/{full_path:path}")
async def serve_spa(full_path: str, request: Request):
    return FileResponse(INDEX_HTML)

@app.get("/")
async def root():
    return {
        "message": "CapeControl API is running successfully!",
        "version": "3.0.0",
        "docs": "/docs",
        "health": "/health",
        "middleware_status": {
            "monitoring": True,
            "input_sanitization": True,
            "content_moderation": True,
            "ddos_protection": DDOS_PROTECTION_AVAILABLE,
            "audit_logging": AUDIT_LOGGING_AVAILABLE
        },
        "routes_status": {
            "usage_analytics": USAGE_ANALYTICS_AVAILABLE,
            "preference_management": PREFERENCE_MANAGEMENT_AVAILABLE
        }
    }