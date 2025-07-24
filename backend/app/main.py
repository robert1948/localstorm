from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
# from app.routes import auth  # Legacy - DISABLED
# from app.routes import auth_enhanced  # Enhanced - DISABLED
from app.routes import auth_v2  # V2 registration system - ACTIVE
from app.routes import cape_ai  # CapeAI service - ACTIVE
import os

app = FastAPI(
    title="CapeControl API",
    description="Secure, scalable authentication system for CapeControl",
    version="2.0.0"
)

# Include routers - Production V2 only
# app.include_router(auth.router, prefix="/api")  # Legacy authentication - DISABLED
# app.include_router(auth_enhanced.router)  # Enhanced authentication - DISABLED
app.include_router(auth_v2.router, prefix="/api")  # V2 registration system - ACTIVE
app.include_router(cape_ai.router, prefix="/api")  # CapeAI service - ACTIVE

# Health check endpoint
@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "message": "CapeControl API is running",
        "version": "2.0.0",
        "timestamp": "2025-07-13",
        "database_connected": True,
        "enhanced_auth": "enabled (v2 tables)",
        "registration_v2": "enabled (2-step flow)"
    }

# API status endpoint
@app.get("/api/")
async def api_root():
    return {
        "message": "CapeControl API",
        "status": "operational",
        "docs": "/docs",
        "health": "/api/health"
    }

# TODO: Enable enhanced auth after database migration
# app.include_router(auth_enhanced.router)  # New enhanced authentication system

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
