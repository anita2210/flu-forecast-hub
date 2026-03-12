<div align="center">

# 🦠 Flu Forecast Hub

### Predicting Influenza Trends with Data Science

<br>

An end-to-end data analytics project that collects CDC flu data,<br>
builds forecasting models, and presents insights through interactive visualizations.

<br>

---

</div>

## 🔗 Live Demo

<div align="center">

| 🌐 Website | 📊 Tableau Dashboard |
|:----------:|:--------------------:|
| [flu-forecast-hub.onrender.com](https://flu-forecast-hub.onrender.com) | [View Dashboard](https://public.tableau.com/views/FluForecastHub/Overview) |

</div>

---

## ✨ Project Workflow

<div align="center">

| Step | Task | Description |
|:----:|:----:|:------------|
| 1 | **Collect** | Fetch flu surveillance data from CDC |
| 2 | **Clean** | Validate and process raw data |
| 3 | **Analyze** | Explore seasonal patterns and trends |
| 4 | **Predict** | Forecast using ARIMA time-series model |
| 5 | **Visualize** | Build interactive Tableau dashboard |
| 6 | **Deploy** | Launch Flask web application |

</div>

---

## 🛠️ Technologies Used

<div align="center">

| Category | Technologies |
|:--------:|:-------------|
| **Data & ML** | Python · Pandas · NumPy · Statsmodels · Scikit-learn |
| **Visualization** | Tableau · Matplotlib · Seaborn |
| **Web** | Flask · HTML · CSS · Bootstrap |
| **DevOps** | GitHub Actions · Pytest · Render |

</div>

---

## 📁 Project Structure

```
flu-forecast-hub/
│
├── backend/
│   ├── app/
│   │   ├── data_fetcher.py      ← CDC data collection
│   │   ├── forecaster.py        ← ARIMA model
│   │   └── web/templates/       ← HTML pages
│   └── tests/                   ← 32 unit tests
│
├── notebooks/
│   ├── 01_exploratory_analysis.ipynb
│   └── 02_forecasting.ipynb
│
├── scripts/
│   └── run_web.py               ← Local server
│
└── app.py                       ← Deployment entry
```

---

## 🚀 Quick Start

```bash
git clone https://github.com/anita2210/flu-forecast-hub.git
cd flu-forecast-hub
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python scripts/run_web.py
```

<div align="center">

📍 Open **http://127.0.0.1:5000** in your browser

</div>

---

## 🔌 API Reference

<div align="center">

| Method | Endpoint | Description |
|:------:|:---------|:------------|
| `GET` | `/api/data` | Recent flu records |
| `GET` | `/api/forecast` | 8-week predictions |
| `GET` | `/api/stats` | Summary statistics |

</div>

---

## 📊 Dashboard Charts

<div align="center">

| Chart | Insight |
|:------|:--------|
| 📈 ILI Trend | Weekly flu activity over 5 years |
| 🗓️ Seasonal Heatmap | Patterns by week and year |
| 📉 Year Comparison | Side-by-side flu seasons |
| 📊 Severity Count | Distribution of flu levels |

</div>

---

## 🧪 Testing

<div align="center">

**32 unit tests** covering data fetcher, forecaster, and APIs

</div>

```bash
pytest backend/tests/ -v
```

---

<div align="center">

## 👩‍💻 Author

**Anita**

[![GitHub](https://img.shields.io/badge/GitHub-@anita2210-black?style=flat&logo=github)](https://github.com/anita2210)

<br>

⭐ **Star this repo if you found it helpful!!!**

</div>




