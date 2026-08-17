import sys
from src.config import DATASET_ID, LLM_MODEL, CACHE_DIR
from src.data.loader import load_zomato_dataset
from src.data.schema import apply_schema
from src.data.preprocess import preprocess_data

def load_dataset_summary():
    """Phase 2 execution function: Load, clean, and summarize data."""
    print("Loading dataset...")
    df_raw = load_zomato_dataset()
    print(f"Raw shape: {df_raw.shape}")
    
    print("Applying schema mapping...")
    df_mapped = apply_schema(df_raw)
    
    print("Preprocessing data...")
    df_clean = preprocess_data(df_mapped)
    print(f"Cleaned shape: {df_clean.shape}")
    
    thresholds = df_clean.attrs.get('budget_thresholds', {})
    print(f"Derived budget thresholds: Low <= {thresholds.get('low')}, Medium <= {thresholds.get('medium')}")
    
    print("\nSample Data:")
    print(df_clean[['restaurant_name', 'location', 'cuisine', 'cost', 'rating', 'budget_band']].head(3))
    print("-" * 50)
    return df_clean

def main():
    print("=" * 50)
    print(" AI-Powered Restaurant Recommendation System")
    print("=" * 50)
    print(f"Dataset      : {DATASET_ID}")
    print(f"LLM Model    : {LLM_MODEL}")
    print(f"Cache Dir    : {CACHE_DIR}")
    print("-" * 50)
    
    # Phase 2 Ingestion
    df_clean = load_dataset_summary()
    
    print("System booted and data ingested successfully.")
    print("=" * 50)

    # Phase 3 User Input
    from src.input.cli import collect_preferences_cli
    print("\n" + "=" * 50)
    print(" Phase 3: User Input")
    print("=" * 50)
    prefs = collect_preferences_cli()
    if prefs:
        print("\nPreferences collected successfully:")
        print(prefs.model_dump_json(indent=2))
    else:
        print("\nFailed to collect valid preferences. Exiting.")
        sys.exit(1)

    # Phase 4 & 5 Integration & Recommendation
    from src.config import MAX_CANDIDATES
    from src.integration.filter import filter_restaurants
    from src.recommendation.engine import recommend
    import json
    
    print("\n" + "=" * 50)
    print(" Phase 4 & 5: Recommendation Engine")
    print("=" * 50)
    
    candidates_df, metrics = filter_restaurants(
        df=df_clean,
        location=prefs.location,
        cuisine=prefs.cuisine,
        budget=prefs.budget,
        min_rating=prefs.min_rating,
        max_candidates=MAX_CANDIDATES
    )
    
    print("Filter metrics:")
    for k, v in metrics.items():
        print(f"  {k}: {v}")
        
    print(f"\nFetching recommendations from LLM for {len(candidates_df)} candidates...")
    
    result = recommend(prefs, candidates_df)
    
    print("\nFINAL RECOMMENDATIONS:")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
