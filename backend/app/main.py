from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

# ✅ Absolute paths to static build output
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
INDEX_HTML = os.path.join(STATIC_DIR, "index.html")
ASSETS_DIR = os.path.join(STATIC_DIR, "assets")

# ✅ Warn and explain if frontend build is missing (dev help)
if not os.path.exists(INDEX_HTML):
    raise RuntimeError(
        f"❌ Frontend build not found: {INDEX_HTML}\n"
        "➡️  Run `npm run build` in the client directory first."
    )

# ✅ Mount static files (e.g., CSS/JS)
if os.path.isdir(ASSETS_DIR):
    app.mount("/assets", StaticFiles(directory=ASSETS_DIR), name="assets")

# ✅ Catch-all route to serve SPA
@app.get("/{full_path:path}")
async def serve_spa(full_path: str, request: Request):
    return FileResponse(INDEX_HTML)
