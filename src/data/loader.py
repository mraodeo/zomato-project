import os
import pandas as pd
from datasets import load_dataset
from src.config import DATASET_ID, CACHE_PATH

def load_zomato_dataset(force_download: bool = False) -> pd.DataFrame:
    """
    Load Zomato dataset from Hugging Face or local Parquet cache.
    """
    if not force_download and CACHE_PATH.exists():
        print(f"Loading data from cache: {CACHE_PATH}")
        # Only load the columns we actually use to prevent Out-Of-Memory (OOM) on Railway
        needed_cols = ["name", "location", "cuisines", "approx_cost(for two people)", "rate", "votes", "rest_type", "address"]
        try:
            return pd.read_parquet(CACHE_PATH, columns=needed_cols)
        except ValueError:
            # Fallback if the parquet is old and missing columns
            return pd.read_parquet(CACHE_PATH)
        
    print(f"Downloading dataset {DATASET_ID} from Hugging Face...")
    ds = load_dataset(DATASET_ID)
    
    # Handle datasets that might not use 'train' split by default
    if 'train' in ds:
        df = ds['train'].to_pandas()
    else:
        df = list(ds.values())[0].to_pandas()
        
    # Drop massive heavy columns to save memory and avoid OOM kills on Railway (500MB limit)
    heavy_columns = ['reviews_list', 'menu_item', 'dish_liked']
    df = df.drop(columns=[col for col in heavy_columns if col in df.columns], errors='ignore')
        
    print(f"Saving dataset to cache: {CACHE_PATH}")
    df.to_parquet(CACHE_PATH, index=False)
    
    return df
