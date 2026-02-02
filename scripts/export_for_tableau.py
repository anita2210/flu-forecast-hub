"""
Export Data for Tableau
-----------------------
Creates clean CSV files optimized for Tableau dashboards.

Outputs:
- ili_historical.csv: Historical ILI data with dates
- ili_forecast.csv: Future predictions
- ili_seasonal.csv: Aggregated seasonal patterns
"""

import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Setup paths
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'backend', 'app'))

from data_fetcher import fetch_sample_data
from forecaster import FluForecaster

def create_date_from_week(year, week):
    """Convert year and week to actual date."""
    try:
        # First day of the week
        date = datetime.strptime(f'{int(year)}-W{int(week):02d}-1', '%Y-W%W-%w')
        return date
    except:
        return None

def export_historical_data(df: pd.DataFrame, output_path: str):
    """Export historical data with proper date formatting."""
    
    export_df = df.copy()
    
    # Create date column
    export_df['date'] = export_df.apply(
        lambda row: create_date_from_week(row['year'], row['week']), 
        axis=1
    )
    
    # Add useful columns for Tableau
    export_df['month'] = export_df['date'].dt.month
    export_df['month_name'] = export_df['date'].dt.strftime('%B')
    export_df['quarter'] = export_df['date'].dt.quarter
    export_df['day_of_year'] = export_df['date'].dt.dayofyear
    
    # Season classification
    def get_season(month):
        if month in [12, 1, 2]:
            return 'Winter'
        elif month in [3, 4, 5]:
            return 'Spring'
        elif month in [6, 7, 8]:
            return 'Summer'
        else:
            return 'Fall'
    
    export_df['season'] = export_df['month'].apply(get_season)
    
    # Flu severity classification
    def get_severity(ili):
        if ili < 2:
            return 'Low'
        elif ili < 4:
            return 'Moderate'
        elif ili < 6:
            return 'High'
        else:
            return 'Very High'
    
    export_df['severity'] = export_df['ili_percentage'].apply(get_severity)
    
    # Save
    export_df.to_csv(output_path, index=False)
    print(f" Historical data saved: {output_path}")
    print(f"   Rows: {len(export_df)}, Columns: {len(export_df.columns)}")
    
    return export_df

def export_forecast_data(df: pd.DataFrame, output_path: str, weeks: int = 12):
    """Export forecast predictions."""
    
    # Fit model on all data
    forecaster = FluForecaster()
    full_data = pd.Series(df['ili_percentage'].values)
    forecaster.fit_arima(full_data)
    
    # Generate forecast
    predictions = forecaster.predict(steps=weeks)
    
    # Create future dates
    last_year = int(df['year'].max())
    last_week = int(df['week'].max())
    
    forecast_data = []
    for i, pred in enumerate(predictions, 1):
        future_week = last_week + i
        future_year = last_year
        
        if future_week > 52:
            future_week = future_week - 52
            future_year = last_year + 1
        
        date = create_date_from_week(future_year, future_week)
        
        forecast_data.append({
            'year': future_year,
            'week': future_week,
            'date': date,
            'ili_percentage': round(pred, 2),
            'type': 'Forecast',
            'confidence_low': round(max(0, pred - 1.5), 2),
            'confidence_high': round(pred + 1.5, 2)
        })
    
    forecast_df = pd.DataFrame(forecast_data)
    forecast_df.to_csv(output_path, index=False)
    print(f" Forecast data saved: {output_path}")
    print(f"   Weeks forecasted: {weeks}")
    
    return forecast_df

def export_seasonal_summary(df: pd.DataFrame, output_path: str):
    """Export seasonal aggregated data."""
    
    # Add season
    def get_season(week):
        if week <= 10 or week >= 48:
            return 'Winter (Flu Season)'
        elif 11 <= week <= 22:
            return 'Spring'
        elif 23 <= week <= 35:
            return 'Summer'
        else:
            return 'Fall'
    
    df = df.copy()
    df['season'] = df['week'].apply(get_season)
    
    # Aggregate by year and season
    seasonal = df.groupby(['year', 'season']).agg({
        'ili_percentage': ['mean', 'max', 'min', 'std']
    }).round(2)
    
    seasonal.columns = ['avg_ili', 'max_ili', 'min_ili', 'std_ili']
    seasonal = seasonal.reset_index()
    
    seasonal.to_csv(output_path, index=False)
    print(f" Seasonal summary saved: {output_path}")
    
    return seasonal

def export_weekly_averages(df: pd.DataFrame, output_path: str):
    """Export weekly averages across all years."""
    
    weekly = df.groupby('week').agg({
        'ili_percentage': ['mean', 'std', 'min', 'max']
    }).round(2)
    
    weekly.columns = ['avg_ili', 'std_ili', 'min_ili', 'max_ili']
    weekly = weekly.reset_index()
    
    # Add week labels
    weekly['week_label'] = weekly['week'].apply(lambda w: f'Week {w}')
    
    weekly.to_csv(output_path, index=False)
    print(f" Weekly averages saved: {output_path}")
    
    return weekly


def main():
    print(" Exporting Data for Tableau")
    
    
    # Create tableau export folder
    tableau_dir = os.path.join(PROJECT_ROOT, 'tableau', 'data')
    os.makedirs(tableau_dir, exist_ok=True)
    
    # Load data
    
    df = fetch_sample_data()
    
    # Export files
    print("\n Exporting files...")
    
    export_historical_data(
        df, 
        os.path.join(tableau_dir, 'ili_historical.csv')
    )
    
    export_forecast_data(
        df, 
        os.path.join(tableau_dir, 'ili_forecast.csv'),
        weeks=12
    )
    
    export_seasonal_summary(
        df, 
        os.path.join(tableau_dir, 'ili_seasonal.csv')
    )
    
    export_weekly_averages(
        df, 
        os.path.join(tableau_dir, 'ili_weekly_avg.csv')
    )
    
    
    print(f" Files saved to: {tableau_dir}")
    
 

if __name__ == "__main__":
    main()