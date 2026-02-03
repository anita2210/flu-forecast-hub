<div align="center">

🦠 Flu Forecast Hub

Predicting Influenza Trends with Data Science

Show Image

Show Image

Show Image



An end-to-end data analytics project that collects CDC flu data, builds forecasting models, and presents insights through interactive visualizations.

</div>



✨ What This Project Does

I built this project to demonstrate the complete data science workflow:



Collect → Fetch real flu surveillance data from CDC

Clean → Validate and process the data

Analyze → Explore patterns and seasonal trends

Predict → Forecast future flu activity using ARIMA

Visualize → Create interactive Tableau dashboards

Deploy → Build and launch a web application





🔗 Quick Links

🌐 Live Website📊 Tableau Dashboard



🛠️ Built With

Data \& ML: Python · Pandas · NumPy · Statsmodels · Scikit-learn

Visualization: Tableau · Matplotlib · Seaborn

Web: Flask · HTML · CSS · Bootstrap

DevOps: GitHub Actions · Pytest · Render



📁 Project Structure

📦 flu-forecast-hub

├── 🐍 backend/app/

│   ├── data\_fetcher.py     → Fetches CDC data

│   ├── forecaster.py       → ARIMA predictions

│   └── web/templates/      → HTML pages

├── 📓 notebooks/

│   ├── 01\_exploratory\_analysis.ipynb

│   └── 02\_forecasting.ipynb

├── 🧪 backend/tests/       → 32 unit tests

└── 🚀 app.py               → Deployment entry



🚀 Run Locally

bash# Clone \& setup

git clone https://github.com/anita2210/flu-forecast-hub.git

cd flu-forecast-hub

python -m venv venv

venv\\Scripts\\activate

pip install -r requirements.txt



\# Run

python scripts/run\_web.py



\# Visit → http://127.0.0.1:5000



🔌 API Endpoints

GET  /api/data      →  Recent flu records

GET  /api/forecast  →  8-week predictions

GET  /api/stats     →  Summary statistics



📊 Dashboard Highlights

ChartInsight📈 ILI TrendWeekly flu activity over 5 years🗓️ HeatmapSeasonal patterns by week \& year📉 Year ComparisonCompare flu seasons side-by-side📊 SeverityDistribution of flu intensity



🧪 Testing

✅ 32 tests covering data validation, forecasting, and API

bashpytest backend/tests/ -v



<div align="center">

👩‍💻 Author

Anita

Made with ❤️ and lots of ☕

⭐ Star this repo if you found it helpful!

</div>





