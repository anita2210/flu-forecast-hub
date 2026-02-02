"""
Forecasting Module
------------------
Time-series forecasting models for flu prediction.

Learning Points:
- ARIMA model for time-series
- Train/test splitting for time-series
- Model evaluation metrics
"""

import pandas as pd
import numpy as np
from typing import Tuple, Dict, Optional
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_absolute_error, mean_squared_error
import warnings

warnings.filterwarnings('ignore')


class FluForecaster:
    """
    Forecasts flu ILI percentages using time-series models.
    
    Supports:
    - ARIMA (AutoRegressive Integrated Moving Average)
    - Simple Moving Average (baseline)
    """
    
    def __init__(self):
        self.model = None
        self.model_type = None
        self.is_fitted = False
        self.train_data = None
    
    def prepare_data(
        self, 
        df: pd.DataFrame, 
        target_col: str = 'ili_percentage',
        test_size: int = 12
    ) -> Tuple[pd.Series, pd.Series]:
        """
        Prepare data for time-series modeling.
        
        Args:
            df: DataFrame with flu data
            target_col: Column to forecast
            test_size: Number of weeks to hold out for testing
            
        Returns:
            Tuple of (train_series, test_series)
        """
        if target_col not in df.columns:
            raise ValueError(f"Column '{target_col}' not found in DataFrame")
        
        if len(df) < test_size + 10:
            raise ValueError("Not enough data for train/test split")
        
        # Sort by time
        df = df.sort_values(['year', 'week']).reset_index(drop=True)
        
        # Get target series
        series = df[target_col].values
        
        # Split: all except last test_size for training
        train = pd.Series(series[:-test_size])
        test = pd.Series(series[-test_size:])
        
        return train, test
    
    def fit_arima(
        self, 
        train_data: pd.Series, 
        order: Tuple[int, int, int] = (2, 1, 2)
    ) -> 'FluForecaster':
        """
        Fit ARIMA model to training data.
        
        Args:
            train_data: Training time series
            order: (p, d, q) parameters for ARIMA
                   p = autoregressive terms
                   d = differencing
                   q = moving average terms
                   
        Returns:
            self (for method chaining)
        """
        if len(train_data) < 20:
            raise ValueError("Need at least 20 data points for ARIMA")
        
        self.train_data = train_data
        
        try:
            self.model = ARIMA(train_data, order=order)
            self.model = self.model.fit()
            self.model_type = 'ARIMA'
            self.is_fitted = True
        except Exception as e:
            raise RuntimeError(f"ARIMA fitting failed: {e}")
        
        return self
    
    def fit_moving_average(
        self, 
        train_data: pd.Series, 
        window: int = 4
    ) -> 'FluForecaster':
        """
        Fit simple moving average model (baseline).
        
        Args:
            train_data: Training time series
            window: Number of periods for moving average
            
        Returns:
            self
        """
        self.train_data = train_data
        self.model = {'window': window, 'last_values': train_data.tail(window).values}
        self.model_type = 'MovingAverage'
        self.is_fitted = True
        
        return self
    
    def predict(self, steps: int = 4) -> np.ndarray:
        """
        Forecast future values.
        
        Args:
            steps: Number of periods to forecast
            
        Returns:
            Array of predictions
        """
        if not self.is_fitted:
            raise RuntimeError("Model not fitted. Call fit_arima() or fit_moving_average() first")
        
        if steps < 1:
            raise ValueError("Steps must be at least 1")
        
        if self.model_type == 'ARIMA':
            forecast = self.model.forecast(steps=steps)
            # Ensure non-negative predictions (ILI can't be negative)
            forecast = np.maximum(forecast, 0)
            return forecast.values
        
        elif self.model_type == 'MovingAverage':
            # Simple: predict the average of last n values
            predictions = []
            values = list(self.model['last_values'])
            
            for _ in range(steps):
                pred = np.mean(values[-self.model['window']:])
                predictions.append(pred)
                values.append(pred)
            
            return np.array(predictions)
        
        else:
            raise RuntimeError(f"Unknown model type: {self.model_type}")
    
    def evaluate(
        self, 
        test_data: pd.Series, 
        predictions: np.ndarray
    ) -> Dict[str, float]:
        """
        Evaluate model performance.
        
        Args:
            test_data: Actual values
            predictions: Predicted values
            
        Returns:
            Dictionary with MAE, RMSE, MAPE metrics
        """
        if len(test_data) != len(predictions):
            # Trim to shorter length
            min_len = min(len(test_data), len(predictions))
            test_data = test_data[:min_len]
            predictions = predictions[:min_len]
        
        actual = np.array(test_data)
        pred = np.array(predictions)
        
        mae = mean_absolute_error(actual, pred)
        rmse = np.sqrt(mean_squared_error(actual, pred))
        
        # MAPE (Mean Absolute Percentage Error)
        # Avoid division by zero
        mask = actual != 0
        if mask.sum() > 0:
            mape = np.mean(np.abs((actual[mask] - pred[mask]) / actual[mask])) * 100
        else:
            mape = np.nan
        
        return {
            'MAE': round(mae, 4),
            'RMSE': round(rmse, 4),
            'MAPE': round(mape, 2) if not np.isnan(mape) else None
        }
    
    def get_model_summary(self) -> str:
        """Get summary of fitted model."""
        if not self.is_fitted:
            return "No model fitted yet"
        
        if self.model_type == 'ARIMA':
            return str(self.model.summary())
        else:
            return f"Moving Average (window={self.model['window']})"


def run_forecast_pipeline(
    df: pd.DataFrame,
    forecast_weeks: int = 4,
    test_weeks: int = 12
) -> Dict:
    """
    Run complete forecasting pipeline.
    
    Args:
        df: DataFrame with flu data
        forecast_weeks: Weeks to forecast into future
        test_weeks: Weeks to hold out for testing
        
    Returns:
        Dictionary with results
    """
    forecaster = FluForecaster()
    
    # Prepare data
    train, test = forecaster.prepare_data(df, test_size=test_weeks)
    
    # Fit ARIMA
    forecaster.fit_arima(train)
    
    # Predict on test period
    test_predictions = forecaster.predict(steps=len(test))
    
    # Evaluate
    metrics = forecaster.evaluate(test, test_predictions)
    
    # Forecast future
    forecaster.fit_arima(pd.Series(df['ili_percentage'].values))  # Refit on all data
    future_forecast = forecaster.predict(steps=forecast_weeks)
    
    return {
        'metrics': metrics,
        'test_actual': test.values,
        'test_predicted': test_predictions,
        'future_forecast': future_forecast,
        'model_type': forecaster.model_type
    }


if __name__ == "__main__":
    # Quick test
    import sys
    import os
    sys.path.insert(0, os.path.dirname(__file__))
    
    from data_fetcher import fetch_sample_data
    
    print("🔮 Running Forecast Pipeline...")
    print("=" * 50)
    
    # Get data
    df = fetch_sample_data()
    
    # Run pipeline
    results = run_forecast_pipeline(df)
    
    print(f"\n📊 Model: {results['model_type']}")
    print(f"\n📈 Evaluation Metrics:")
    for metric, value in results['metrics'].items():
        print(f"   • {metric}: {value}")
    
    print(f"\n🔮 Next 4 Weeks Forecast:")
    for i, val in enumerate(results['future_forecast'], 1):
        print(f"   • Week +{i}: {val:.2f}%")