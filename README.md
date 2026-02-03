\# 🦠 Flu Forecast Hub



A comprehensive data analytics and visualization project demonstrating end-to-end data science workflow using CDC flu surveillance data.



\## 🌐 Live Demo



| Platform | Link |

|----------|------|

| \*\*Website\*\* | \[https://flu-forecast-hub.onrender.com](https://flu-forecast-hub.onrender.com) |

| \*\*Tableau Dashboard\*\* | \[View Dashboard](https://public.tableau.com/views/FluForecastHubDashboard/FluDashboard) |



\## 📊 Project Overview



This project analyzes historical flu trends and creates visualizations to help understand seasonal patterns, regional variations, and predictive indicators.



\### Features

\- 📈 \*\*Data Collection\*\*: Automated CDC flu data fetching and validation

\- 🤖 \*\*ARIMA Forecasting\*\*: Time-series predictions for future flu trends

\- 📊 \*\*Interactive Dashboard\*\*: 5-chart Tableau dashboard with heatmaps and trends

\- 🌐 \*\*Web Application\*\*: Flask-based interface with REST API

\- ✅ \*\*32 Unit Tests\*\*: Comprehensive test coverage with CI/CD



\## 🛠️ Technologies Used



| Category | Technologies |

|----------|-------------|

| \*\*Backend\*\* | Python, Flask, Pandas, NumPy |

| \*\*ML/Stats\*\* | Statsmodels (ARIMA), Scikit-learn |

| \*\*Visualization\*\* | Tableau, Matplotlib, Seaborn |

| \*\*Frontend\*\* | HTML5, CSS3, Bootstrap 5 |

| \*\*Testing\*\* | Pytest (32 tests) |

| \*\*CI/CD\*\* | GitHub Actions |

| \*\*Deployment\*\* | Render |



\## 🗂️ Project Structure



```

flu-forecast-hub/

├── backend/

│   ├── app/

│   │   ├── data\_fetcher.py    # CDC data collection

│   │   ├── forecaster.py      # ARIMA forecasting model

│   │   └── web/               # Flask web application

│   └── tests/                 # 32 unit tests

├── notebooks/

│   ├── 01\_exploratory\_analysis.ipynb

│   └── 02\_forecasting.ipynb

├── tableau/                   # Tableau data exports

├── scripts/                   # Utility scripts

└── app.py                     # Deployment entry point

```



\## 🚀 Getting Started



\### Prerequisites

\- Python 3.9+

\- Tableau Public (free)



\### Installation



```bash

\# Clone repository

git clone https://github.com/anita2210/flu-forecast-hub.git

cd flu-forecast-hub



\# Create virtual environment

python -m venv venv

source venv/bin/activate  # On Windows: venv\\Scripts\\activate



\# Install dependencies

pip install -r requirements.txt

```



\### Run Locally



```bash

\# Run web application

python scripts/run\_web.py



\# Open browser: http://127.0.0.1:5000

```



\### Run Tests



```bash

pytest backend/tests/ -v

```



\## 📈 API Endpoints



| Endpoint | Description |

|----------|-------------|

| `/api/data` | Get recent flu data records |

| `/api/forecast` | Get forecast predictions |

| `/api/stats` | Get data statistics |



\## 📊 Dashboard Preview



The Tableau dashboard includes:

\- ILI Trend (Time Series)

\- Seasonal Heatmap (Year vs Week)

\- Year-over-Year Comparison

\- Forecast Visualization

\- Severity Distribution



\## 🧪 Testing



\- \*\*32 Unit Tests\*\* covering data fetching, validation, and forecasting

\- \*\*CI/CD Pipeline\*\* with GitHub Actions

\- Tests run automatically on every push



\## 👤 Author



\*\*Anita\*\*



\- GitHub: \[@anita2210](https://github.com/anita2210)

\- Project: \[flu-forecast-hub](https://github.com/anita2210/flu-forecast-hub)







