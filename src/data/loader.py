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
    
    # Drop massive heavy columns before converting to pandas to completely avoid OOM
    heavy_columns = ['reviews_list', 'menu_item', 'dish_liked']
    
    if 'train' in ds:
        dataset_split = ds['train']
    else:
        dataset_split = list(ds.values())[0]
        
    cols_to_remove = [col for col in heavy_columns if col in dataset_split.column_names]
    dataset_split = dataset_split.remove_columns(cols_to_remove)
    
    df = dataset_split.to_pandas()
        
    print(f"Saving dataset to cache: {CACHE_PATH}")
    df.to_parquet(CACHE_PATH, index=False)
    
    return df
