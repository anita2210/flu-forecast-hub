"""
Run the Flu Forecast Hub web application.

Usage:
    python scripts/run_web.py
"""

import sys
import os

# Get project root
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add backend/app to path for imports (data_fetcher, forecaster)
sys.path.insert(0, os.path.join(project_root, 'backend', 'app'))

# Change to web directory so Flask can find templates
web_dir = os.path.join(project_root, 'backend', 'app', 'web')
os.chdir(web_dir)

# Now import Flask app
from flask import Flask, render_template, jsonify
from data_fetcher import fetch_sample_data
from forecaster import FluForecaster, run_forecast_pipeline

# Create Flask app
template_dir = os.path.join(project_root, 'backend', 'app', 'web', 'templates')
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
    print("=" * 50)
    print("🦠 Flu Forecast Hub - Web Application")
    print("=" * 50)
    print("\n📍 Open in browser: http://127.0.0.1:5000\n")
    print("Pages:")
    print("   • Home:      http://127.0.0.1:5000/")
    print("   • Forecast:  http://127.0.0.1:5000/forecast")
    print("   • Dashboard: http://127.0.0.1:5000/dashboard")
    print("   • About:     http://127.0.0.1:5000/about")
    print("\nAPI:")
    print("   • Data:      http://127.0.0.1:5000/api/data")
    print("   • Forecast:  http://127.0.0.1:5000/api/forecast")
    print("   • Stats:     http://127.0.0.1:5000/api/stats")
    print("\n" + "=" * 50)
    print("Press Ctrl+C to stop the server")
    print("=" * 50 + "\n")
    
    app.run(debug=True, port=5000, use_reloader=False)