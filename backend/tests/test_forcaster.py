"""
Unit Tests for Forecaster Module
--------------------------------
Tests for time-series forecasting functionality.
"""

import pytest
import pandas as pd
import numpy as np
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from forecaster import FluForecaster, run_forecast_pipeline
from data_fetcher import fetch_sample_data


class TestFluForecasterDataPrep:
    """Tests for data preparation."""
    
    @pytest.fixture
    def sample_df(self):
        """Create sample DataFrame for testing."""
        return fetch_sample_data()
    
    @pytest.fixture
    def forecaster(self):
        return FluForecaster()
    
    @pytest.mark.unit
    def test_prepare_data_returns_correct_split(self, forecaster, sample_df):
        """Train/test split should have correct sizes."""
        test_size = 12
        train, test = forecaster.prepare_data(sample_df, test_size=test_size)
        
        assert len(test) == test_size
        assert len(train) == len(sample_df) - test_size
    
    @pytest.mark.unit
    def test_prepare_data_raises_error_for_missing_column(self, forecaster, sample_df):
        """Should raise error if target column doesn't exist."""
        with pytest.raises(ValueError, match="not found"):
            forecaster.prepare_data(sample_df, target_col='nonexistent_column')
    
    @pytest.mark.unit
    def test_prepare_data_raises_error_for_insufficient_data(self, forecaster):
        """Should raise error if not enough data."""
        small_df = pd.DataFrame({
            'year': [2023] * 5,
            'week': range(1, 6),
            'ili_percentage': [1.0] * 5
        })
        
        with pytest.raises(ValueError, match="Not enough data"):
            forecaster.prepare_data(small_df, test_size=10)


class TestARIMAModel:
    """Tests for ARIMA model."""
    
    @pytest.fixture
    def forecaster(self):
        return FluForecaster()
    
    @pytest.fixture
    def train_data(self):
        """Generate sample training data."""
        np.random.seed(42)
        return pd.Series(np.random.uniform(1, 5, 100))
    
    @pytest.mark.unit
    def test_fit_arima_sets_model(self, forecaster, train_data):
        """ARIMA fitting should set model attributes."""
        forecaster.fit_arima(train_data)
        
        assert forecaster.is_fitted == True
        assert forecaster.model_type == 'ARIMA'
        assert forecaster.model is not None
    
    @pytest.mark.unit
    def test_fit_arima_raises_error_for_small_data(self, forecaster):
        """Should raise error if data too small."""
        small_data = pd.Series([1, 2, 3, 4, 5])
        
        with pytest.raises(ValueError, match="at least 20"):
            forecaster.fit_arima(small_data)
    
    @pytest.mark.unit
    def test_predict_returns_correct_length(self, forecaster, train_data):
        """Predictions should have requested length."""
        forecaster.fit_arima(train_data)
        
        predictions = forecaster.predict(steps=4)
        
        assert len(predictions) == 4
    
    @pytest.mark.unit
    def test_predict_returns_non_negative(self, forecaster, train_data):
        """ILI predictions should never be negative."""
        forecaster.fit_arima(train_data)
        
        predictions = forecaster.predict(steps=10)
        
        assert all(p >= 0 for p in predictions)
    
    @pytest.mark.unit
    def test_predict_raises_error_if_not_fitted(self, forecaster):
        """Should raise error if predict called before fit."""
        with pytest.raises(RuntimeError, match="not fitted"):
            forecaster.predict(steps=4)
    
    @pytest.mark.unit
    def test_predict_raises_error_for_invalid_steps(self, forecaster, train_data):
        """Should raise error for steps < 1."""
        forecaster.fit_arima(train_data)
        
        with pytest.raises(ValueError, match="at least 1"):
            forecaster.predict(steps=0)


class TestMovingAverageModel:
    """Tests for Moving Average baseline model."""
    
    @pytest.fixture
    def forecaster(self):
        return FluForecaster()
    
    @pytest.fixture
    def train_data(self):
        return pd.Series([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0])
    
    @pytest.mark.unit
    def test_fit_moving_average_sets_model(self, forecaster, train_data):
        """MA fitting should set model attributes."""
        forecaster.fit_moving_average(train_data, window=4)
        
        assert forecaster.is_fitted == True
        assert forecaster.model_type == 'MovingAverage'
    
    @pytest.mark.unit
    def test_moving_average_prediction_is_average(self, forecaster, train_data):
        """First MA prediction should be average of last n values."""
        window = 4
        forecaster.fit_moving_average(train_data, window=window)
        
        predictions = forecaster.predict(steps=1)
        expected = np.mean(train_data.tail(window))
        
        assert np.isclose(predictions[0], expected)


class TestModelEvaluation:
    """Tests for model evaluation metrics."""
    
    @pytest.fixture
    def forecaster(self):
        return FluForecaster()
    
    @pytest.mark.unit
    def test_evaluate_returns_all_metrics(self, forecaster):
        """Evaluation should return MAE, RMSE, MAPE."""
        actual = pd.Series([1.0, 2.0, 3.0, 4.0])
        predicted = np.array([1.1, 2.2, 2.9, 4.1])
        
        metrics = forecaster.evaluate(actual, predicted)
        
        assert 'MAE' in metrics
        assert 'RMSE' in metrics
        assert 'MAPE' in metrics
    
    @pytest.mark.unit
    def test_evaluate_perfect_prediction(self, forecaster):
        """Perfect predictions should have zero error."""
        actual = pd.Series([1.0, 2.0, 3.0])
        predicted = np.array([1.0, 2.0, 3.0])
        
        metrics = forecaster.evaluate(actual, predicted)
        
        assert metrics['MAE'] == 0
        assert metrics['RMSE'] == 0
    
    @pytest.mark.unit
    def test_evaluate_handles_length_mismatch(self, forecaster):
        """Should handle different lengths gracefully."""
        actual = pd.Series([1.0, 2.0, 3.0, 4.0, 5.0])
        predicted = np.array([1.0, 2.0, 3.0])
        
        # Should not raise error
        metrics = forecaster.evaluate(actual, predicted)
        
        assert metrics['MAE'] >= 0


class TestForecastPipeline:
    """Tests for the complete pipeline."""
    
    @pytest.mark.unit
    def test_pipeline_returns_all_components(self):
        """Pipeline should return metrics, predictions, forecast."""
        df = fetch_sample_data()
        
        results = run_forecast_pipeline(df, forecast_weeks=4, test_weeks=12)
        
        assert 'metrics' in results
        assert 'test_actual' in results
        assert 'test_predicted' in results
        assert 'future_forecast' in results
        assert 'model_type' in results
    
    @pytest.mark.unit
    def test_pipeline_forecast_length(self):
        """Future forecast should have correct length."""
        df = fetch_sample_data()
        
        forecast_weeks = 8
        results = run_forecast_pipeline(df, forecast_weeks=forecast_weeks)
        
        assert len(results['future_forecast']) == forecast_weeks


if __name__ == "__main__":
    pytest.main([__file__, "-v"])