# Application configuration from environment variables.

import os
from pathlib import Path


def _split_origins(raw: str) -> list[str]:
    return [origin.strip() for origin in raw.split(",") if origin.strip()]


GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

# Comma-separated list. Defaults preserve local Vite dev.
CORS_ORIGINS: list[str] = _split_origins(
    os.getenv(
        "CORS_ORIGINS",
        "http://localhost:5173,http://127.0.0.1:5173",
    )
)

# Built frontend assets (Vite dist). Populated in the Cloud Run image.
STATIC_DIR: Path = Path(
    os.getenv(
        "STATIC_DIR",
        str(Path(__file__).resolve().parent.parent.parent / "static"),
    )
)
