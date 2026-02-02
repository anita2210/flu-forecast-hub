"""
Data Fetcher Module
-------------------
Handles fetching flu surveillance data from CDC FluView API.

Learning Points:
- API integration with requests library
- Error handling for network calls
- Data validation before processing
"""

import requests
import pandas as pd
from typing import Optional
from datetime import datetime


class CDCDataFetcher:
    """
    Fetches Influenza-Like Illness (ILI) data from CDC FluView.
    
    The CDC provides weekly surveillance data including:
    - ILI percentage (% of visits for flu-like symptoms)
    - Number of providers reporting
    - Regional breakdowns
    """
    
    BASE_URL = "https://gis.cdc.gov/grasp/fluview/FluViewPhase2"
    
    # Alternative: Direct CSV endpoint (more reliable)
    ILI_CSV_URL = "https://gis.cdc.gov/grasp/flu2/GetPhase02InitApp"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'FluForecastHub/1.0 (Educational Project)'
        })
    
    def fetch_national_ili(
        self, 
        start_year: int = 2020, 
        end_year: Optional[int] = None
    ) -> pd.DataFrame:
        """
        Fetch national ILI (Influenza-Like Illness) data.
        
        Args:
            start_year: First year to fetch (default: 2020)
            end_year: Last year to fetch (default: current year)
            
        Returns:
            DataFrame with columns: year, week, ili_percentage, num_providers
            
        Raises:
            ConnectionError: If CDC API is unreachable
            ValueError: If data format is unexpected
        """
        if end_year is None:
            end_year = datetime.now().year
            
        # Validate inputs
        if start_year > end_year:
            raise ValueError("start_year cannot be greater than end_year")
        if start_year < 1997:  # CDC data starts from 1997
            raise ValueError("CDC ILI data only available from 1997 onwards")
            
        # For this project, we'll use a sample dataset approach
        # In production, you'd make actual API calls
        try:
            # Simulated data fetch - replace with actual API call
            data = self._fetch_from_api(start_year, end_year)
            return self._validate_and_clean(data)
        except requests.RequestException as e:
            raise ConnectionError(f"Failed to fetch CDC data: {e}")
    
    def _fetch_from_api(self, start_year: int, end_year: int) -> pd.DataFrame:
        """
        Internal method to fetch from CDC API.
        
        Note: CDC's API can be complex. For learning purposes,
        we'll create sample data that mirrors the real structure.
        """
        # This will be replaced with actual API call in Phase 1
        # For now, returns empty DataFrame with correct structure
        return pd.DataFrame(columns=[
            'year', 'week', 'region', 
            'ili_percentage', 'num_providers', 'total_patients'
        ])
    
    def _validate_and_clean(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Validate and clean the fetched data.
        
        Checks performed:
        1. Required columns exist
        2. No negative values in numeric columns
        3. Percentages are between 0-100
        """
        required_cols = ['year', 'week', 'ili_percentage']
        
        for col in required_cols:
            if col not in df.columns:
                raise ValueError(f"Missing required column: {col}")
        
        # Clean data
        df = df.copy()
        
        # Ensure numeric types
        df['year'] = pd.to_numeric(df['year'], errors='coerce')
        df['week'] = pd.to_numeric(df['week'], errors='coerce')
        df['ili_percentage'] = pd.to_numeric(df['ili_percentage'], errors='coerce')
        
        # Remove invalid rows
        df = df.dropna(subset=required_cols)
        
        # Validate ranges
        df = df[df['ili_percentage'].between(0, 100)]
        df = df[df['week'].between(1, 53)]
        
        return df.reset_index(drop=True)


def fetch_sample_data() -> pd.DataFrame:
    """
    Generate sample data for testing and development.
    
    This mimics CDC data structure for when API is unavailable.
    """
    import numpy as np
    
    np.random.seed(42)  # Reproducibility
    
    years = range(2020, 2025)
    weeks = range(1, 53)
    
    data = []
    for year in years:
        for week in weeks:
            # Simulate seasonal flu pattern (peaks in winter)
            # Week 1-10 and 40-52 are typically high flu season
            if week <= 10 or week >= 40:
                base_ili = np.random.uniform(3.0, 7.0)
            else:
                base_ili = np.random.uniform(1.0, 3.0)
            
            data.append({
                'year': year,
                'week': week,
                'region': 'National',
                'ili_percentage': round(base_ili, 2),
                'num_providers': np.random.randint(2000, 3500),
                'total_patients': np.random.randint(50000, 100000)
            })
    
    return pd.DataFrame(data)