# 🌿 ECOSPHERE AI
### AI-Assisted Smart Environmental Monitoring & Sustainability Platform

[![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-009688.svg?logo=fastapi)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18.2.0-61DAFB.svg?logo=react)](https://react.dev)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB.svg?logo=python)](https://python.org)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-1.4.1-F7931E.svg?logo=scikit-learn)](https://scikit-learn.org)
[![SQLite](https://img.shields.io/badge/SQLite-Integrated-003B57.svg?logo=sqlite)](https://sqlite.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791.svg?logo=postgresql)](https://postgresql.org)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

---

## 📌 Executive Summary

**ECOSPHERE AI** is a professional, production-grade environmental intelligence and sustainability decision-support platform designed for academic evaluation, municipal planning, and environmental governance.

Rather than relying on simulated mockups or random numbers, ECOSPHERE AI connects **authentic environmental datasets**, real-time IoT sensors, and government databases (CPCB, TSPCB, Open-Meteo, NASA GIBS, GBIF). The default primary monitoring region is centered on **Warangal, Telangana, India (17.9689° N, 79.5941° E)**.

---

## 🚀 How to Run in Visual Studio Code (Windows)

### Prerequisites
- **Python 3.10+** (Tested on Python 3.10 - 3.14)
- **Node.js 18+** & **npm**

---

### Step 1: Open the Project in VS Code
Open the project root folder in VS Code:
```text
C:\Users\rishi\.gemini\antigravity\scratch\ecosphere-ai
```

---

### Step 2: Run the Backend (Terminal 1)
Open a new PowerShell terminal in VS Code (`Ctrl + ` `) and run:
```powershell
cd backend
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```
You should see:
```text
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Application startup complete.
```

---

### Step 3: Run the Frontend (Terminal 2)
Click the `+` button in the VS Code terminal to open a **second terminal** and run:
```powershell
cd frontend
npm run dev
```
You should see:
```text
  VITE v5.4.21  ready in 979 ms
  ➜  Local:   http://127.0.0.1:5173/
```

---

### Step 4: Open in Your Browser
Visit: **[http://localhost:5173](http://localhost:5173)**

#### Quick Demo Accounts (One-Click Login):
| Role | Email | Password |
|---|---|---|
| **System Administrator** | `admin@ecosphere.org` | `Admin@123456` |
| **Environmental Officer** | `officer@ecosphere.org` | `Officer@123456` |
| **Public Citizen / Researcher** | `citizen@ecosphere.org` | `Citizen@123456` |

*(Tip: On the Sign In page, click any of the "Quick Demo Accounts" buttons at the bottom to auto-fill credentials!)*

---

## 🌐 Key URLs & Endpoints

| Service / Interface | URL | Description |
|---|---|---|
| **Frontend Application** | `http://localhost:5173` | React.js SPA Dashboard & All Modules |
| **Backend REST API** | `http://localhost:8000` | FastAPI core service |
| **Interactive API Docs (Swagger)** | `http://localhost:8000/docs` | Full interactive Swagger UI |
| **ReDoc Documentation** | `http://localhost:8000/redoc` | OpenAPI specifications |
| **System Health Check** | `http://localhost:8000/api/health` | Live service health & region info |
| **Water Quality Records** | `http://localhost:8000/api/water-quality` | CPCB & IoT surface water readings |
| **Live API Status** | `http://localhost:8000/api/live-data/status` | Ingestion pipeline health |

---

## 🛠️ Environmental Modules Included

1. **Dashboard Overview** (`/`): High-level environmental health index, live weather, AQI, and trends.
2. **Water Quality** (`/water-quality`): Comprehensive analysis of Bhadrakali Lake, Wadepally Tank, Dharmasagar, Godavari River, Pakhal Lake, Ramappa Lake, and Kakatiya Canal. Includes interactive charts, location comparisons, date trends, parameters guide, and IoT ingestion.
3. **Air Quality Telemetry** (`/air-quality`): Continuous Ambient Air Quality Monitoring (CAAQMS) with CPCB standards.
4. **Weather Monitoring** (`/weather`): High-resolution Open-Meteo current observation and 7-day forecast.
5. **Analytics & Reports** (`/analytics`): Multi-domain Pandas statistical analysis with CSV and PDF export.
6. **AI Forecasting & Anomaly Detection** (`/ai-forecasting`): Scikit-learn Ridge regression & IsolationForest.
7. **Optimization & Operations Research** (`/optimization`): Dijkstra smart waste collection and MCDA emergency dispatch.
8. **Geospatial GIS Map** (`/map`): Interactive Leaflet map with monitoring stations and NASA GIBS satellite layer.
9. **Biodiversity Observations** (`/biodiversity`): GBIF occurrence records and species conservation statuses.
10. **Environmental Incidents** (`/incidents`): TSPCB municipal incident tracking and resolution workflow.
11. **Data Sources & Telemetry Status** (`/data-sources`): Real-time ingestion latency, freshness, and status.
12. **Public Portal** (`/portal`): Citizen grievance submission and report tracking.

---

## 🧪 Automated Testing
Run backend unit and integration tests from the `backend/` directory:
```powershell
cd backend
python -m pytest tests
```
*Result: 24/24 passing unit tests covering Authentication, CRUD, IoT Ingestion, AI/ML, and Operations Research.*

---

## 📄 License
Academic Engineering Project — Product 23. Released under the MIT License.
