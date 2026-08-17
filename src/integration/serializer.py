import pandas as pd
import json

def serialize_candidates(df: pd.DataFrame) -> str:
    """
    Convert candidates DataFrame to a compact JSON string to keep token footprint small.
    """
    if df.empty:
        return "[]"
    
    # Select columns to include
    cols = ['restaurant_name', 'location', 'cuisine', 'rating', 'cost', 'budget_band']
    
    # Keep only available columns
    available_cols = [c for c in cols if c in df.columns]
    
    records = df[available_cols].to_dict(orient='records')
    return json.dumps(records, indent=2)
