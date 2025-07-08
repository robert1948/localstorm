from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth
import os

app = FastAPI()

# Include routers
app.include_router(auth.router, prefix="/api")

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

# ✅ Serve SPA entry point (index.html)
@app.get("/{full_path:path}")
async def serve_spa(full_path: str, request: Request):
    return FileResponse(INDEX_HTML)
