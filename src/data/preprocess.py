import numpy as np
import pandas as pd

def clean_rating(rating_str):
    """Convert '4.1/5' or '4.1' to 4.1. Handle 'NEW', '-', etc."""
    if pd.isna(rating_str):
        return np.nan
    rating_str = str(rating_str).strip()
    if rating_str in ['NEW', '-', '']:
        return np.nan
    try:
        return float(rating_str.split('/')[0])
    except Exception:
        return np.nan

def clean_cost(cost_str):
    """Convert '1,200' to 1200.0."""
    if pd.isna(cost_str):
        return np.nan
    cost_str = str(cost_str).strip().replace(',', '')
    try:
        return float(cost_str)
    except Exception:
        return np.nan

def clean_cuisine(cuisine_str):
    """Convert 'North Indian, Chinese' to 'north indian, chinese'."""
    if pd.isna(cuisine_str):
        return ""
    return str(cuisine_str).lower().strip()

def calculate_budget_bands(df: pd.DataFrame) -> dict:
    """
    Calculate dynamic budget thresholds based on percentiles.
    """
    valid_costs = df['cost'].dropna()
    low_thresh = valid_costs.quantile(0.33)
    med_thresh = valid_costs.quantile(0.67)
    
    return {
        "low": low_thresh,
        "medium": med_thresh,
        "high": float('inf')
    }

def assign_budget_band(cost: float, thresholds: dict) -> str:
    """Assign band based on cost."""
    if pd.isna(cost):
        return "unknown"
    if cost <= thresholds["low"]:
        return "low"
    elif cost <= thresholds["medium"]:
        return "medium"
    else:
        return "high"

def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply all preprocessing steps.
    """
    # 1. Drop critical nulls
    df_clean = df.dropna(subset=['restaurant_name', 'location']).copy()
    
    # 2. Normalize strings
    df_clean['restaurant_name'] = df_clean['restaurant_name'].astype(str).str.strip()
    df_clean['location'] = df_clean['location'].astype(str).str.strip()
    
    # 3. Parse numbers
    df_clean['rating'] = df_clean['rating'].apply(clean_rating)
    df_clean['cost'] = df_clean['cost'].apply(clean_cost)
    
    # 4. Clean cuisines
    df_clean['cuisine'] = df_clean['cuisine'].apply(clean_cuisine)
    
    # 5. Drop rows without valid cost as it's required for filtering
    df_clean = df_clean.dropna(subset=['cost']).copy()
    
    # 6. Derive budget bands
    thresholds = calculate_budget_bands(df_clean)
    df_clean['budget_band'] = df_clean['cost'].apply(lambda x: assign_budget_band(x, thresholds))
    df_clean.attrs['budget_thresholds'] = thresholds
    
    return df_clean
