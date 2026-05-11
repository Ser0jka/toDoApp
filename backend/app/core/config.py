import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent
dotenv_path = BASE_DIR / ".env"
load_dotenv(dotenv_path=dotenv_path)


@dataclass(frozen=True)
class Settings:
    DATABASE_URL: str
    cors_allowed_origin: list[str]


def get_settings() -> Settings:
    db_url = os.getenv("DATABASE_URL")
    raw_origins = os.getenv("CORS_ALLOWED_ORIGIN", "")
    origins_list = [
        origin.strip() for origin in raw_origins.split(",") if origin.strip()
    ]
    if db_url is None:
        # Это поможет сразу понять, что .env не прочитался
        raise ValueError("DATABASE_URL is not set in environment variables")

    return Settings(DATABASE_URL=db_url, cors_allowed_origin=origins_list)
