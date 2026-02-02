"""
Data Fetcher Module
-------------------
Fetches real flu surveillance data from CDC FluView API.

Learning Points:
- Working with real government APIs
- Handling JSON responses
- Data validation and cleaning
"""

import requests
import pandas as pd
from typing import Optional
from datetime import datetime
import os


class CDCDataFetcher:
    """
    Fetches Influenza-Like Illness (ILI) data from CDC FluView.
    
    CDC FluView provides weekly surveillance data including:
    - ILI percentage (% of visits for flu-like symptoms)
    - Number of providers reporting
    - Regional and state-level breakdowns
    """
    
    # CDC FluView API endpoint
    BASE_URL = "https://www.cdc.gov/flu/weekly/weeklyarchives2023-2024/data"
    
    # ILINet National Data API
    ILINET_URL = "https://gis.cdc.gov/grasp/flu2/PostPhase02DataDownload"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'FluForecastHub/1.0 (Educational Project)',
            'Accept': 'application/json'
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
            DataFrame with flu surveillance data
            
        Raises:
            ConnectionError: If CDC API is unreachable
            ValueError: If data format is unexpected
        """
        if end_year is None:
            end_year = datetime.now().year
            
        # Validate inputs
        if start_year > end_year:
            raise ValueError("start_year cannot be greater than end_year")
        if start_year < 1997:
            raise ValueError("CDC ILI data only available from 1997 onwards")
        
        try:
            # Fetch from CDC API
            data = self._fetch_ilinet_data(start_year, end_year)
            return self._validate_and_clean(data)
        except requests.RequestException as e:
            raise ConnectionError(f"Failed to fetch CDC data: {e}")
    
    def _fetch_ilinet_data(self, start_year: int, end_year: int) -> pd.DataFrame:
        """
        Fetch ILINet data from CDC.
        
        Uses the WHO/NREVSS surveillance data endpoint.
        """
        # CDC provides data through multiple endpoints
        # We'll use a reliable CSV-based approach
        
        all_data = []
        
        for year in range(start_year, end_year + 1):
            # CDC uses flu seasons (e.g., 2023-2024)
            # Season starts around week 40 of first year
            season = f"{year}-{str(year+1)[2:]}"
            
            try:
                # Try fetching from CDC's direct data endpoint
                url = f"https://www.cdc.gov/flu/weekly/weeklyarchives{year}-{year+1}/data/ILINet.csv"
                response = self.session.get(url, timeout=30)
                
                if response.status_code == 200:
                    from io import StringIO
                    df = pd.read_csv(StringIO(response.text), skiprows=1)
                    df['season'] = season
                    all_data.append(df)
            except Exception:
                # If direct endpoint fails, continue to next year
                continue
        
        if all_data:
            return pd.concat(all_data, ignore_index=True)
        else:
            # Fallback to sample data if API unavailable
            print("Note: Using sample data (CDC API unavailable)")
            return fetch_sample_data()
    
    def _validate_and_clean(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Validate and clean the fetched data.
        """
        required_cols = ['year', 'week', 'ili_percentage']
        
        # Standardize column names (CDC uses various formats)
        df.columns = df.columns.str.lower().str.strip()
        df.columns = df.columns.str.replace(' ', '_')
        df.columns = df.columns.str.replace('%', 'percentage')
        
        # Map CDC column names to our standard names
        column_mapping = {
            'weighted_ili': 'ili_percentage',
            'wili': 'ili_percentage',
            '%_weighted_ili': 'ili_percentage',
            'ilitotal': 'total_ili',
            'total_patients': 'total_patients',
            'num._of_providers': 'num_providers',
            'number_of_providers': 'num_providers'
        }
        
        df = df.rename(columns=column_mapping)
        
        # Check for required columns
        for col in required_cols:
            if col not in df.columns:
                raise ValueError(f"Missing required column: {col}")
        
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
    
    def save_to_csv(self, df: pd.DataFrame, filename: str = "ili_national.csv") -> str:
        """
        Save DataFrame to CSV in data/raw/ folder.
        
        Args:
            df: DataFrame to save
            filename: Name of the file
            
        Returns:
            Full path to saved file
        """
        # Get project root (go up from backend/app)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        raw_data_path = os.path.join(project_root, 'data', 'raw')
        
        # Ensure directory exists
        os.makedirs(raw_data_path, exist_ok=True)
        
        # Full file path
        filepath = os.path.join(raw_data_path, filename)
        
        # Save with timestamp
        df.to_csv(filepath, index=False)
        print(f"Data saved to: {filepath}")
        
        return filepath


def fetch_sample_data() -> pd.DataFrame:
    """
    Generate sample data for testing and development.
    Mimics real CDC data structure.
    """
    import numpy as np
    
    np.random.seed(42)
    
    years = range(2020, 2026)
    weeks = range(1, 53)
    regions = ['National']
    
    data = []
    for year in years:
        for week in weeks:
            # Simulate seasonal flu pattern
            # Peak: weeks 1-10 (Jan-Mar) and 48-52 (Dec)
            # Low: weeks 20-35 (May-Aug)
            
            if week <= 10 or week >= 48:
                # Winter peak
                base_ili = np.random.uniform(3.5, 7.5)
            elif 20 <= week <= 35:
                # Summer low
                base_ili = np.random.uniform(0.8, 2.0)
            else:
                # Shoulder seasons
                base_ili = np.random.uniform(1.5, 4.0)
            
            # Add year-over-year variation
            year_factor = 1 + (year - 2020) * 0.05 * np.random.choice([-1, 1])
            
            data.append({
                'year': year,
                'week': week,
                'region': 'National',
                'ili_percentage': round(base_ili * year_factor, 2),
                'num_providers': np.random.randint(2000, 3500),
                'total_patients': np.random.randint(50000, 120000),
                'total_ili': np.random.randint(1000, 8000)
            })
    
    return pd.DataFrame(data)


def fetch_and_save_data(start_year: int = 2020) -> pd.DataFrame:
    """
    Convenience function to fetch and save CDC data.
    
    Usage:
        from data_fetcher import fetch_and_save_data
        df = fetch_and_save_data(2020)
    """
    fetcher = CDCDataFetcher()
    
    try:
        df = fetcher.fetch_national_ili(start_year=start_year)
    except ConnectionError:
        print("Could not connect to CDC. Using sample data.")
        df = fetch_sample_data()
    
    fetcher.save_to_csv(df)
    return df


if __name__ == "__main__":
    # Run this file directly to fetch and save data
    print("Fetching CDC flu data...")
    df = fetch_and_save_data()
    print(f"\nFetched {len(df)} records")
    print(f"\nData preview:")
    print(df.head(10))
    print(f"\nYears covered: {df['year'].min()} - {df['year'].max()}")