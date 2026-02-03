"""
Flu Forecast Hub - Flask Web Application (Deployment Version)
"""

import sys
import os

# Setup paths
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(current_dir, 'backend', 'app'))

from flask import Flask, render_template, jsonify

# Import our modules
from backend.app.data_fetcher import fetch_sample_data
from backend.app.forecaster import FluForecaster, run_forecast_pipeline

# Create Flask app with template folder
template_dir = os.path.join(current_dir, 'backend', 'app', 'web', 'templates')
app = Flask(__name__, template_folder=template_dir)

# ============== ROUTES ==============

@app.route('/')
def home():
    """Home page with overview."""
    df = fetch_sample_data()
    
    stats = {
        'total_records': len(df),
        'years': f"{int(df['year'].min())} - {int(df['year'].max())}",
        'avg_ili': round(df['ili_percentage'].mean(), 2),
        'max_ili': round(df['ili_percentage'].max(), 2),
        'min_ili': round(df['ili_percentage'].min(), 2)
    }
    
    return render_template('home.html', stats=stats)


@app.route('/forecast')
def forecast():
    """Forecast page showing predictions."""
    df = fetch_sample_data()
    
    results = run_forecast_pipeline(df, forecast_weeks=8, test_weeks=12)
    
    forecast_data = {
        'predictions': [round(x, 2) for x in results['future_forecast']],
        'metrics': results['metrics'],
        'model': results['model_type']
    }
    
    return render_template('forecast.html', forecast=forecast_data)


@app.route('/dashboard')
def dashboard():
    """Embedded Tableau dashboard."""
    tableau_url = "https://public.tableau.com/views/FluForecastHubDashboard/FluDashboard"
    return render_template('dashboard.html', tableau_url=tableau_url)


@app.route('/about')
def about():
    """About page."""
    return render_template('about.html')


# ============== API ENDPOINTS ==============

@app.route('/api/data')
def api_data():
    """API endpoint for raw data."""
    df = fetch_sample_data()
    return jsonify({
        'status': 'success',
        'count': len(df),
        'data': df.tail(20).to_dict(orient='records')
    })


@app.route('/api/forecast')
def api_forecast():
    """API endpoint for forecast."""
    df = fetch_sample_data()
    results = run_forecast_pipeline(df, forecast_weeks=8, test_weeks=12)
    
    return jsonify({
        'status': 'success',
        'model': results['model_type'],
        'metrics': results['metrics'],
        'forecast': [round(x, 2) for x in results['future_forecast']]
    })


@app.route('/api/stats')
def api_stats():
    """API endpoint for statistics."""
    df = fetch_sample_data()
    
    return jsonify({
        'status': 'success',
        'statistics': {
            'mean': round(df['ili_percentage'].mean(), 2),
            'std': round(df['ili_percentage'].std(), 2),
            'min': round(df['ili_percentage'].min(), 2),
            'max': round(df['ili_percentage'].max(), 2),
            'records': len(df)
        }
    })


# ============== RUN APP ==============

if __name__ == '__main__':
    app.run(debug=True, port=5000)