"""
Configuration loader for environment variables and app settings.
"""

import os
from dotenv import load_dotenv

load_dotenv()  # Loads variables from .env if present

class Settings:
    QDRANT_HOST: str = os.getenv("QDRANT_HOST", "localhost")
    QDRANT_PORT: int = int(os.getenv("QDRANT_PORT", 6333))
    QDRANT_COLLECTION: str = os.getenv("QDRANT_COLLECTION", "frames")
    OUTPUT_DIR: str = os.getenv("OUTPUT_DIR", "output_frames")
    VECTOR_DIM: int = int(os.getenv("VECTOR_DIM", 256 * 3))
    ALLOWED_ORIGINS: list[str] = [
        origin.strip() for origin in os.getenv("ALLOWED_ORIGINS", "*").split(",")
    ]

settings = Settings()