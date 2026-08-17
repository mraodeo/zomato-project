import pandas as pd
import numpy as np
from src.data.schema import apply_schema
from src.data.preprocess import clean_rating, clean_cost, assign_budget_band, clean_cuisine, preprocess_data

def test_clean_rating():
    assert clean_rating('4.1/5') == 4.1
    assert clean_rating(' 3.8 /5 ') == 3.8
    assert clean_rating('4') == 4.0
    assert np.isnan(clean_rating('NEW'))
    assert np.isnan(clean_rating('-'))

def test_clean_cost():
    assert clean_cost('800') == 800.0
    assert clean_cost('1,200') == 1200.0
    assert clean_cost(' 1,500 ') == 1500.0
    assert np.isnan(clean_cost(np.nan))

def test_clean_cuisine():
    assert clean_cuisine('North Indian, Chinese') == 'north indian, chinese'
    assert clean_cuisine('  Cafe  ') == 'cafe'
    assert clean_cuisine(np.nan) == ''

def test_schema_mapping():
    raw_df = pd.DataFrame({
        'name': ['A'],
        'location': ['B'],
        'cuisines': ['C'],
        'approx_cost(for two people)': ['800'],
        'rate': ['4.1/5'],
        'votes': [100],
        'rest_type': ['Cafe'],
        'address': ['123 St']
    })
    mapped = apply_schema(raw_df)
    assert 'restaurant_name' in mapped.columns
    assert 'cost' in mapped.columns
    assert 'name' not in mapped.columns

def test_preprocess_data():
    raw_df = pd.DataFrame({
        'name': ['A', 'B', np.nan, 'D'],
        'location': ['Loc1', 'Loc2', 'Loc3', 'Loc4'],
        'cuisines': ['North Indian', 'Cafe', 'Chinese', 'Italian'],
        'approx_cost(for two people)': ['800', '1,200', '500', np.nan],
        'rate': ['4.1/5', 'NEW', '4.5/5', '3.8/5'],
        'votes': [100, 0, 50, 10]
    })
    mapped = apply_schema(raw_df)
    clean = preprocess_data(mapped)
    
    # Should drop row 3 (null name) and row 4 (null cost)
    assert len(clean) == 2
    
    # Check types and values
    assert clean.iloc[0]['cost'] == 800.0
    assert clean.iloc[1]['cost'] == 1200.0
    assert clean.iloc[0]['rating'] == 4.1
    assert np.isnan(clean.iloc[1]['rating']) # 'NEW'
    
    # Check budget bands
    assert 'budget_band' in clean.columns
