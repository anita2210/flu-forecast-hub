"""
Flu Forecast Hub - Backend Application
--------------------------------------
A data analytics project demonstrating flu trend analysis
and visualization capabilities.
"""

__version__ = "0.1.0"
__author__ = "Your Name"

from .data_fetcher import CDCDataFetcher, fetch_sample_data

__all__ = ['CDCDataFetcher', 'fetch_sample_data']