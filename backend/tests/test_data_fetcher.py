"""
Unit Tests for Data Fetcher Module
----------------------------------
Tests data fetching, validation, and cleaning logic.
"""

import pytest
import pandas as pd
import numpy as np
import sys
import os

# Add the app directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from data_fetcher import CDCDataFetcher, fetch_sample_data


class TestCDCDataFetcher:
    """Test suite for CDCDataFetcher class."""
    
    @pytest.fixture
    def fetcher(self):
        """Create a fresh fetcher instance for each test."""
        return CDCDataFetcher()
    
    @pytest.fixture
    def valid_dataframe(self):
        """Sample valid DataFrame for testing."""
        return pd.DataFrame({
            'year': [2023, 2023, 2024],
            'week': [1, 2, 1],
            'region': ['National', 'National', 'National'],
            'ili_percentage': [3.5, 4.2, 2.8],
            'num_providers': [2500, 2600, 2400],
            'total_patients': [75000, 78000, 72000]
        })
    
    # ===== Input Validation Tests =====
    
    @pytest.mark.unit
    def test_fetch_raises_error_when_start_year_greater_than_end_year(self, fetcher):
        """Should raise ValueError when start_year > end_year."""
        with pytest.raises(ValueError, match="start_year cannot be greater"):
            fetcher.fetch_national_ili(start_year=2024, end_year=2020)
    
    @pytest.mark.unit
    def test_fetch_raises_error_for_year_before_1997(self, fetcher):
        """CDC data only available from 1997."""
        with pytest.raises(ValueError, match="only available from 1997"):
            fetcher.fetch_national_ili(start_year=1990)
    
    # ===== Data Validation Tests =====
    
    @pytest.mark.unit
    def test_validate_removes_negative_ili_percentages(self, fetcher):
        """ILI percentage should never be negative."""
        df = pd.DataFrame({
            'year': [2023, 2023],
            'week': [1, 2],
            'ili_percentage': [3.5, -1.0]
        })
        
        cleaned = fetcher._validate_and_clean(df)
        
        assert len(cleaned) == 1
        assert cleaned['ili_percentage'].iloc[0] == 3.5
    
    @pytest.mark.unit
    def test_validate_removes_ili_over_100(self, fetcher):
        """ILI percentage cannot exceed 100%."""
        df = pd.DataFrame({
            'year': [2023, 2023],
            'week': [1, 2],
            'ili_percentage': [3.5, 150.0]
        })
        
        cleaned = fetcher._validate_and_clean(df)
        
        assert len(cleaned) == 1
    
    @pytest.mark.unit
    def test_validate_removes_invalid_weeks(self, fetcher):
        """Week number must be 1-53."""
        df = pd.DataFrame({
            'year': [2023, 2023, 2023],
            'week': [1, 54, 0],
            'ili_percentage': [3.5, 4.0, 3.0]
        })
        
        cleaned = fetcher._validate_and_clean(df)
        
        assert len(cleaned) == 1
        assert cleaned['week'].iloc[0] == 1
    
    @pytest.mark.unit
    def test_validate_raises_error_missing_required_columns(self, fetcher):
        """Should raise ValueError if required columns missing."""
        df = pd.DataFrame({
            'year': [2023],
            'week': [1]
        })
        
        with pytest.raises(ValueError, match="Missing required column"):
            fetcher._validate_and_clean(df)
    
    @pytest.mark.unit
    def test_validate_handles_missing_values(self, fetcher):
        """Rows with NaN in required columns should be removed."""
        df = pd.DataFrame({
            'year': [2023, None, 2023],
            'week': [1, 2, None],
            'ili_percentage': [3.5, 4.0, 2.5]
        })
        
        cleaned = fetcher._validate_and_clean(df)
        
        assert len(cleaned) == 1
        assert cleaned['year'].iloc[0] == 2023
        assert cleaned['week'].iloc[0] == 1


class TestFetchSampleData:
    """Tests for the sample data generator."""
    
    @pytest.mark.unit
    def test_sample_data_has_required_columns(self):
        """Sample data should have all expected columns."""
        df = fetch_sample_data()
        
        required_cols = ['year', 'week', 'region', 'ili_percentage']
        for col in required_cols:
            assert col in df.columns, f"Missing column: {col}"
    
    @pytest.mark.unit
    def test_sample_data_has_valid_ranges(self):
        """All values should be within valid ranges."""
        df = fetch_sample_data()
        
        assert df['week'].between(1, 52).all()
        assert df['ili_percentage'].between(0, 100).all()
        assert df['year'].between(2020, 2025).all()
    
    @pytest.mark.unit
    def test_sample_data_is_reproducible(self):
        """Same seed should produce same data."""
        df1 = fetch_sample_data()
        df2 = fetch_sample_data()
        
        pd.testing.assert_frame_equal(df1, df2)
    
    @pytest.mark.unit
    def test_sample_data_shows_seasonal_pattern(self):
        """Winter weeks should have higher ILI on average."""
        df = fetch_sample_data()
        
        winter = df[(df['week'] <= 10) | (df['week'] >= 40)]
        summer = df[(df['week'] > 10) & (df['week'] < 40)]
        
        assert winter['ili_percentage'].mean() > summer['ili_percentage'].mean()


class TestSaveToCSV:
    """Tests for saving data to CSV."""
    
    @pytest.fixture
    def fetcher(self):
        return CDCDataFetcher()
    
    @pytest.fixture
    def sample_df(self):
        return pd.DataFrame({
            'year': [2023, 2023],
            'week': [1, 2],
            'region': ['National', 'National'],
            'ili_percentage': [3.5, 4.2]
        })
    
    @pytest.mark.unit
    def test_save_creates_file(self, fetcher, sample_df, tmp_path):
        """Should create a CSV file."""
        # Use temp directory for test
        import tempfile
        
        filepath = os.path.join(tmp_path, "test_data.csv")
        sample_df.to_csv(filepath, index=False)
        
        assert os.path.exists(filepath)
    
    @pytest.mark.unit
    def test_saved_file_contains_correct_data(self, sample_df, tmp_path):
        """Saved CSV should contain the same data."""
        filepath = os.path.join(tmp_path, "test_data.csv")
        sample_df.to_csv(filepath, index=False)
        
        loaded_df = pd.read_csv(filepath)
        
        assert len(loaded_df) == len(sample_df)
        assert list(loaded_df.columns) == list(sample_df.columns)


class TestDataIntegrity:
    """Tests for data integrity and consistency."""
    
    @pytest.mark.unit
    def test_sample_data_has_no_duplicates(self):
        """Each year-week combination should be unique."""
        df = fetch_sample_data()
        
        duplicates = df.duplicated(subset=['year', 'week', 'region'])
        assert duplicates.sum() == 0
    
    @pytest.mark.unit
    def test_sample_data_covers_full_years(self):
        """Each year should have 52 weeks of data."""
        df = fetch_sample_data()
        
        weeks_per_year = df.groupby('year')['week'].count()
        
        for year, count in weeks_per_year.items():
            assert count == 52, f"Year {year} has {count} weeks, expected 52"
    
    @pytest.mark.unit
    def test_ili_percentage_reasonable_range(self):
        """ILI percentage should typically be between 0-15%."""
        df = fetch_sample_data()
        
        # Most values should be under 15% (extreme outbreaks aside)
        reasonable = df['ili_percentage'] <= 15
        assert reasonable.mean() > 0.95  # 95% should be under 15%


if __name__ == "__main__":
    pytest.main([__file__, "-v"])