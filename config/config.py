import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
ASSETS_DIR = BASE_DIR / "assets"
REPORTS_DIR = BASE_DIR / "reports_output"
os.makedirs(REPORTS_DIR, exist_ok=True)

MODELS_DIR = BASE_DIR / "models" / "artifacts"
os.makedirs(MODELS_DIR, exist_ok=True)

RANDOM_SEED = 42

# Read database URL from environment, fallback to SQLite for development
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'retention.db'}")