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
        return pd.read_parquet(CACHE_PATH)
        
    print(f"Downloading dataset {DATASET_ID} from Hugging Face...")
    ds = load_dataset(DATASET_ID)
    
    # Handle datasets that might not use 'train' split by default
    if 'train' in ds:
        df = ds['train'].to_pandas()
    else:
        df = list(ds.values())[0].to_pandas()
        
    print(f"Saving dataset to cache: {CACHE_PATH}")
    df.to_parquet(CACHE_PATH, index=False)
    
    return df
