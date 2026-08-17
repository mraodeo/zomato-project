from typing import Tuple, Dict
import pandas as pd

def filter_restaurants(
    df: pd.DataFrame, 
    location: str, 
    cuisine: str, 
    budget: str, 
    min_rating: float, 
    max_candidates: int
) -> Tuple[pd.DataFrame, Dict]:
    """
    Deterministically reduce the dataset to a candidate set based on preferences.
    Returns the filtered dataframe and a dictionary of metrics.
    """
    metrics = {"rows_total": len(df)}
    
    # Location filter
    mask_location = df['location'].str.contains(location, case=False, na=False)
    filtered = df[mask_location]
    metrics["after_location"] = len(filtered)
    
    # Cuisine filter
    mask_cuisine = filtered['cuisine'].str.contains(cuisine, case=False, na=False)
    filtered = filtered[mask_cuisine]
    metrics["after_cuisine"] = len(filtered)
    
    # Rating filter
    if min_rating > 0:
        mask_rating = filtered['rating'] >= min_rating
        filtered = filtered[mask_rating]
    metrics["after_rating"] = len(filtered)
        
    # Budget filter
    mask_budget = filtered['budget_band'] == budget
    filtered = filtered[mask_budget]
    metrics["after_budget"] = len(filtered)
    
    # Sort by rating descending
    filtered = filtered.sort_values(by='rating', ascending=False, na_position='last')
    
    # Deduplicate by restaurant name (keep highest rated, which is first after sort)
    filtered = filtered.drop_duplicates(subset=['restaurant_name'], keep='first')
    
    # Truncate to max_candidates
    final_candidates = filtered.head(max_candidates)
    metrics["after_truncate"] = len(final_candidates)
    
    return final_candidates, metrics
