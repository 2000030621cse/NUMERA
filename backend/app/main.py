"""NUMERA API application entrypoint."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api.routes import decision, final_report, health, numerology
from app.core.config import CORS_ORIGINS, STATIC_DIR

app = FastAPI(
    title="NUMERA API",
    description="Personal Decision Intelligence platform API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(numerology.router)
app.include_router(decision.router)
app.include_router(final_report.router)

_static_dir = STATIC_DIR
_index_html = _static_dir / "index.html"
_serve_spa = _index_html.is_file()


if not _serve_spa:

    @app.get("/")
    def root() -> dict[str, str]:
        return {
            "name": "NUMERA API",
            "status": "ok",
            "phase": "day-1-foundation",
        }


if _serve_spa:
    assets_dir = _static_dir / "assets"
    if assets_dir.is_dir():
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

    @app.get("/")
    def spa_index() -> FileResponse:
        return FileResponse(_index_html)

    @app.get("/{full_path:path}")
    def spa_fallback(full_path: str) -> FileResponse:
        """Serve static files when present; otherwise SPA index (same-origin UI)."""
        # Do not turn missing API/docs paths into HTML — keep API semantics clear.
        if full_path == "health" or full_path.startswith(
            ("api/", "docs", "redoc", "openapi.json")
        ):
            raise HTTPException(status_code=404, detail="Not Found")

        candidate = _static_dir / full_path
        if full_path and candidate.is_file():
            return FileResponse(candidate)
        return FileResponse(_index_html)
