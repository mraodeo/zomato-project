from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

from src.config import MAX_CANDIDATES
from src.input.preferences import UserPreferences
from src.integration.filter import filter_restaurants
from src.recommendation.engine import recommend
from src.main import load_dataset_summary

import os

app = FastAPI(title="Stitch Tablemate AI Recommendation Engine API")

# Configure CORS for Next.js frontend
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=allowed_origins != ["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variable to hold the cached dataset
df_global = None

@app.on_event("startup")
async def startup_event():
    """Load dataset on API startup."""
    global df_global
    print("API Startup: Loading dataset...")
    df_global = load_dataset_summary()
    print("API Startup: Dataset loaded successfully.")

@app.post("/api/v1/recommendations")
async def get_recommendations(prefs: UserPreferences):
    """
    Get AI-powered restaurant recommendations based on user preferences.
    """
    global df_global
    if df_global is None:
        raise HTTPException(status_code=503, detail="Dataset is still loading or failed to load.")
    
    candidates_df, metrics = filter_restaurants(
        df=df_global,
        location=prefs.location,
        cuisine=prefs.cuisine,
        budget=prefs.budget,
        min_rating=prefs.min_rating,
        max_candidates=MAX_CANDIDATES
    )
    
    if candidates_df.empty:
        # Fallback empty response
        from src.integration.prompt_builder import get_empty_set_response
        return get_empty_set_response()

    try:
        result = recommend(prefs, candidates_df)
        return result
    except Exception as e:
        print(f"Recommendation generation failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate recommendations.")

@app.get("/health")
async def health_check():
    return {"status": "ok", "dataset_loaded": df_global is not None}
