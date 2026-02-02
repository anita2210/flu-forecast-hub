"""
Fetch CDC Flu Data Script
-------------------------
Run this script to download and save flu surveillance data.

Usage:
    python scripts/fetch_data.py
    python scripts/fetch_data.py --start-year 2018
"""

import sys
import os
import argparse

# Add backend/app to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend', 'app'))

from data_fetcher import CDCDataFetcher, fetch_sample_data


def main():
    parser = argparse.ArgumentParser(description='Fetch CDC flu surveillance data')
    parser.add_argument(
        '--start-year', 
        type=int, 
        default=2020,
        help='Start year for data collection (default: 2020)'
    )
    parser.add_argument(
        '--use-sample',
        action='store_true',
        help='Use sample data instead of fetching from CDC'
    )
    
    args = parser.parse_args()
    
    print("=" * 50)
    print("🦠 Flu Forecast Hub - Data Fetcher")
    print("=" * 50)
    
    fetcher = CDCDataFetcher()
    
    if args.use_sample:
        print("\n📊 Generating sample data...")
        df = fetch_sample_data()
    else:
        print(f"\n📡 Fetching CDC data from {args.start_year}...")
        try:
            df = fetcher.fetch_national_ili(start_year=args.start_year)
        except ConnectionError as e:
            print(f"⚠️  Could not connect to CDC: {e}")
            print("📊 Falling back to sample data...")
            df = fetch_sample_data()
    
    # Save data
    filepath = fetcher.save_to_csv(df)
    
    # Print summary
    print("\n" + "=" * 50)
    print("✅ Data Collection Complete!")
    print("=" * 50)
    print(f"\n📈 Summary:")
    print(f"   • Records: {len(df):,}")
    print(f"   • Years: {int(df['year'].min())} - {int(df['year'].max())}")
    print(f"   • Weeks per year: {df.groupby('year')['week'].count().mean():.0f}")
    print(f"\n📁 Saved to: {filepath}")
    
    print(f"\n📊 Data Preview:")
    print(df.head(10).to_string(index=False))
    
    print(f"\n📉 ILI Statistics:")
    print(f"   • Mean: {df['ili_percentage'].mean():.2f}%")
    print(f"   • Max:  {df['ili_percentage'].max():.2f}%")
    print(f"   • Min:  {df['ili_percentage'].min():.2f}%")


if __name__ == "__main__":
    main()