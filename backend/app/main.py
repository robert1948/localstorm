from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

# ✅ Point to Vite build output directly
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIST = os.path.join(BASE_DIR, "..", "..", "client", "dist")
INDEX_HTML = os.path.join(FRONTEND_DIST, "index.html")

if not os.path.exists(INDEX_HTML):
    raise RuntimeError(f"❌ Frontend build not found: {INDEX_HTML}\n"
                       "➡️  Run `npm run build` in the client directory first.")

# ✅ Serve all static files from Vite build
app.mount("/assets", StaticFiles(directory=os.path.join(FRONTEND_DIST, "assets")), name="assets")
app.mount("/static", StaticFiles(directory=os.path.join(FRONTEND_DIST, "static")), name="static")

# ✅ Serve the SPA entry point
@app.get("/{full_path:path}")
async def serve_spa(full_path: str, request: Request):
    return FileResponse(INDEX_HTML)
