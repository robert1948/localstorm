from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

# ✅ Absolute path to static build output (Docker copies frontend here)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
INDEX_HTML = os.path.join(STATIC_DIR, "index.html")
ASSETS_DIR = os.path.join(STATIC_DIR, "assets")

# ✅ Optional: Gracefully warn if frontend is missing (for local dev)
if not os.path.exists(INDEX_HTML):
    raise RuntimeError(f"❌ Missing frontend build: {INDEX_HTML}. Run `npm run build` in client/.")

# ✅ Mount static assets (e.g., JS/CSS/images)
if os.path.isdir(ASSETS_DIR):
    app.mount("/assets", StaticFiles(directory=ASSETS_DIR), name="assets")

# ✅ Serve React SPA for any path
@app.get("/{full_path:path}")
async def serve_spa(full_path: str, request: Request):
    return FileResponse(INDEX_HTML)
