import pandas as pd

# Map raw dataset columns to our internal logical columns
COLUMN_MAPPING = {
    "name": "restaurant_name",
    "location": "location",
    "cuisines": "cuisine",
    "approx_cost(for two people)": "cost",
    "rate": "rating",
    "votes": "votes",
    "rest_type": "rest_type",
    "address": "address"
}

REQUIRED_COLUMNS = ["restaurant_name", "location", "cuisine", "cost", "rating"]

def apply_schema(df: pd.DataFrame) -> pd.DataFrame:
    """Rename columns defensively based on COLUMN_MAPPING."""
    rename_dict = {
        raw_col: logical_col 
        for raw_col, logical_col in COLUMN_MAPPING.items() 
        if raw_col in df.columns
    }
    
    df_mapped = df.rename(columns=rename_dict)
    
    missing = [col for col in REQUIRED_COLUMNS if col not in df_mapped.columns]
    if missing:
        raise ValueError(f"Missing required logical columns after mapping: {missing}")
        
    return df_mapped
