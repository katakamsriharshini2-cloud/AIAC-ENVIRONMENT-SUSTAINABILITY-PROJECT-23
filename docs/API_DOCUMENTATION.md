# 📖 ECOSPHERE AI — REST API Documentation
**Comprehensive Endpoint Reference**

Base URL in Local Development: `http://localhost:8000`
Interactive Swagger UI: `http://localhost:8000/docs`
ReDoc Specification: `http://localhost:8000/redoc`

---

## 1. Authentication (`/api/auth`)

All secured endpoints require the standard HTTP header:
`Authorization: Bearer <jwt_access_token>`

### `POST /api/auth/login`
Authenticates user and returns JWT bearer token.
* **Request Body:**
  ```json
  {
    "email": "admin@ecosphere.org",
    "password": "Admin@123456"
  }
  ```
* **Response (200 OK):**
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIsIn...",
    "token_type": "bearer",
    "user": {
      "id": 1,
      "email": "admin@ecosphere.org",
      "full_name": "System Administrator",
      "role": "administrator"
    }
  }
  ```

### `POST /api/auth/register`
Creates new user account (`public_user` or `environmental_officer`).
* **Request Body:**
  ```json
  {
    "email": "officer2@ecosphere.org",
    "password": "Officer@123456",
    "full_name": "Dr. Ananya Reddy",
    "role": "environmental_officer"
  }
  ```

### `GET /api/auth/me`
Retrieves currently authenticated session user profile. Requires JWT.

---

## 2. Monitoring Stations (`/api/stations`)

### `GET /api/stations`
Lists all environmental monitoring stations across Telangana.
* **Query Parameters:**
  * `station_type` (optional): `AIR_QUALITY`, `WATER_QUALITY`, `WEATHER`, `INDUSTRIAL_EMISSIONS`
  * `city` (optional): `Warangal`, `Hyderabad`, etc.

### `POST /api/stations`
Creates a new monitoring station. Requires `environmental_officer` or `administrator` role.
* **Request Body:**
  ```json
  {
    "station_code": "WAR-CAAQMS-02",
    "name": "Kazipet Railway Junction CAAQMS",
    "station_type": "AIR_QUALITY",
    "latitude": 17.9740,
    "longitude": 79.5210,
    "city": "Warangal",
    "state": "Telangana"
  }
  ```

---

## 3. Live Environmental Telemetry (`/api/live-data`)

### `GET /api/live-data/status`
Returns real-time health, synchronization timestamps, and status for all integrated providers (OpenAQ, CPCB, Open-Meteo, GBIF, NASA GIBS, IoT sensors).

### `GET /api/live-data/air-quality`
Fetches live air quality telemetry. Prioritizes CPCB data for Indian cities with OpenAQ fallback.
* **Query Parameter:** `city` (default: `Warangal`)
* **Response (200 OK):**
  ```json
  {
    "status": "success",
    "source": "GOVERNMENT_DATA",
    "data": {
      "city": "Warangal",
      "station": "Warangal Municipal Station (CPCB)",
      "aqi": 142,
      "category": "Moderate",
      "pm25": 58.4,
      "pm10": 112.0,
      "no2": 34.2,
      "so2": 12.8,
      "co": 1.1,
      "o3": 45.6,
      "timestamp": "2026-11-20T18:45:00Z"
    }
  }
  ```

### `GET /api/live-data/weather`
Returns live surface conditions, 24-hour hourly forecast, and 7-day numerical forecasts from Open-Meteo for Warangal coordinates.

### `GET /api/live-data/water-quality`
Retrieves surface water quality telemetry for Telangana catchment basins (Waddepally Lake, Bhadrakali Lake, Dharmasagar, Kakatiya Canal).

### `GET /api/live-data/biodiversity`
Fetches verified flora and fauna biodiversity vouchers from GBIF for Telangana coordinate bounds.

### `GET /api/live-data/satellite`
Returns NASA GIBS satellite product configurations and WMTS tile URL templates.

### `POST /api/live-data/refresh`
Forces an immediate synchronization cycle across external environmental providers.

---

## 4. Environmental Analytics (`/api/analytics`)

### `GET /api/analytics/overview`
Aggregates municipal key performance indicators (KPIs) and computes the **Ecological Sustainability Index (ESI)** (0-100 scale).

### `GET /api/analytics/air-quality`
Time-series trend records, PM2.5/PM10 ratio calculations, and diurnal curves.

### `GET /api/analytics/export/csv?metric={metric}`
Streams downloadable CSV of historical observations. Metric values: `air`, `water`, `waste`, `energy`.

### `GET /api/analytics/export/pdf`
Dynamically generates and downloads an official executive environmental summary PDF via ReportLab.

---

## 5. AI & Machine Learning (`/api/ai`)

### `POST /api/ai/predict`
Executes Scikit-learn Ridge/Polynomial regression forecasting for a target metric over a specified horizon.
* **Request Body:**
  ```json
  {
    "target_metric": "AQI",
    "horizon_hours": 24,
    "location_name": "Warangal"
  }
  ```
* **Response (200 OK):**
  ```json
  {
    "metric": "AQI",
    "horizon_hours": 24,
    "model_used": "Ridge Regression (Alpha=1.0)",
    "training_samples": 48,
    "mae": 4.18,
    "rmse": 6.82,
    "r2": 0.912,
    "predictions": [
      { "step": "+1h", "predicted": 144.2, "confidence_lower": 132.6, "confidence_upper": 155.8 },
      { "step": "+2h", "predicted": 146.8, "confidence_lower": 135.0, "confidence_upper": 158.5 }
    ]
  }
  ```

### `POST /api/ai/anomaly-detection`
Scans database telemetry using multi-variate `IsolationForest` to isolate statistical outliers.
* **Request Body:**
  ```json
  {
    "metric": "AQI",
    "threshold_sigma": 2.0
  }
  ```

### `GET /api/ai/insights`
Generates autonomous actionable mitigation advisories based on current pollution levels and weather trends.

---

## 6. Algorithmic Optimization (`/api/optimization`)

### `POST /api/optimization/waste`
Calculates optimal municipal solid waste collection dispatch using Dijkstra's shortest-path algorithm and priority queues over smart-bin nodes.
* **Response (200 OK):**
  ```json
  {
    "original_distance_km": 46.2,
    "optimized_distance_km": 31.4,
    "distance_saved_km": 14.8,
    "fuel_saved_liters": 4.2,
    "co2_reduced_kg": 11.3,
    "stops": [
      { "seq": 1, "name": "Hanamkonda Central Depot", "lat": 17.9821, "lon": 79.5781, "fill": 0 },
      { "seq": 2, "name": "Warangal Railway Station Bin 04", "lat": 17.9628, "lon": 79.6012, "fill": 94 }
    ]
  }
  ```

### `POST /api/optimization/resources`
Computes Multi-Criteria Decision Analysis (MCDA) resource allocation for emergency teams and environmental inspectors.

---

## 7. IoT Telemetry Ingestion Gateway (`/api/iot`)

### `POST /api/iot/waste/readings`
Ingests ultrasonic bin depth readings.
* **Request Body:**
  ```json
  {
    "bin_id": "BIN-WAR-001",
    "fill_percentage": 88.5,
    "waste_type": "MUNICIPAL_SOLID",
    "waste_weight_kg": 120.4,
    "location_name": "Hanamkonda Bus Station",
    "latitude": 17.9821,
    "longitude": 79.5781
  }
  ```

### `POST /api/iot/energy/readings`
Ingests electricity smart-meter readings.

### `POST /api/iot/water/readings`
Ingests optical multi-parameter submerged hydrological probe readings (pH, DO, BOD, Turbidity, TDS, Temp).

---

## 8. Public Citizen Grievance Portal (`/api/portal`)

### `POST /api/portal/reports`
Submits citizen grievance. Returns unique tracking code `ECO-XXXXXX`.

### `GET /api/portal/reports/track/{code}`
Retrieves public status and officer remediation remarks for a specific tracking code.
