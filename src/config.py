import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base directories
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
CACHE_DIR = DATA_DIR / "cache"

# Ensure cache directory exists
CACHE_DIR.mkdir(parents=True, exist_ok=True)

# Dataset Config
DATASET_ID = "ManikaSaini/zomato-restaurant-recommendation"
CACHE_PATH = CACHE_DIR / "restaurants_optimized_v2.parquet"

# LLM Config
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq")
LLM_MODEL = os.getenv("LLM_MODEL", "llama-3.3-70b-versatile")
LLM_API_KEY = os.getenv("LLM_API_KEY", "")
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.7"))

# Recommendation Config
DEFAULT_TOP_N = 5
MAX_CANDIDATES = 50

# Budget Thresholds (Placeholders - to be determined from data)
BUDGET_THRESHOLDS = {
    "low": 500,
    "medium": 1500,
    "high": float("inf")
}
