# 🌐 ECOSPHERE AI — Environmental Dataset Sources & Provenance Catalog
**Ground-Truth Telemetry Integration**

ECOSPHERE AI enforces strict data provenance tracking. Every stored record contains data classification, source URL, observation timestamp, and retrieval timestamp.

---

## 1. Air Quality Telemetry: OpenAQ

* **Provider**: OpenAQ Community & Partner Network
* **Documentation**: [https://docs.openaq.org/](https://docs.openaq.org/)
* **API Base URL**: `https://api.openaq.org/v3`
* **Authentication**: Header `X-API-Key` via `OPENAQ_API_KEY`
* **License**: Creative Commons Attribution 4.0 International (CC BY 4.0)
* **Endpoints Integrated**:
  * `/locations` — Monitoring station metadata & coordinates
  * `/latest` — Real-time telemetry values
  * `/measurements` — Historical trends
* **Parameters Collected**: PM2.5 ($\mu g/m^3$), PM10 ($\mu g/m^3$), NO2 ($\mu g/m^3$), SO2 ($\mu g/m^3$), CO ($mg/m^3$), O3 ($\mu g/m^3$)
* **Data Classification**: `LIVE_API` / `HISTORICAL`

---

## 2. Indian National Air Quality: Central Pollution Control Board (CPCB)

* **Provider**: Ministry of Environment, Forest and Climate Change (MoEFCC), Government of India
* **Catalog URL**: [https://www.data.gov.in/catalog/real-time-air-quality-index](https://www.data.gov.in/catalog/real-time-air-quality-index)
* **Resource ID**: `3b01bcb8-0b14-4abf-b6f2-c1bfd384ba69`
* **Authentication**: Query parameter `api-key` via `DATA_GOV_IN_API_KEY`
* **License**: Government Open Data License - India (GODL) / NDSAP
* **Parameters Collected**: National Air Quality Index (NAQI), Sub-indices for PM2.5, PM10, NO2, SO2, CO, O3, City, State, Station Name, Timestamp
* **Priority Rule**: CPCB data is given first priority for Indian cities; OpenAQ is used as supplemental/international fallback.
* **Data Classification**: `GOVERNMENT_DATA`

---

## 3. High-Resolution Weather: Open-Meteo

* **Provider**: Open-Meteo Weather API (ZAMG / DWD numerical weather prediction)
* **Documentation**: [https://open-meteo.com/en/docs](https://open-meteo.com/en/docs)
* **API URL**: `https://api.open-meteo.com/v1/forecast`
* **Authentication**: None required for eligible non-commercial use
* **License**: Open Database License (ODbL)
* **Geographical Targeting**: Exact coordinates for Warangal (Lat: `17.9689`, Lon: `79.5941`)
* **Parameters Collected**:
  * Current: Temperature (2m), Relative Humidity, Apparent Temperature, Precipitation, Wind Speed, Wind Direction, Surface Pressure, Cloud Cover
  * Forecasts: 24-hour hourly profile and 7-day daily maximum/minimum and rainfall probabilities
* **Data Classification**: `LIVE_API`

---

## 4. Surface Hydrological Health: NWQMP / data.gov.in

* **Provider**: Central Pollution Control Board & Telangana State Pollution Control Board (TSPCB)
* **Catalog URL**: [https://data.gov.in/catalog/surface-water-quality](https://data.gov.in/catalog/surface-water-quality)
* **Parameters Collected**: pH, Dissolved Oxygen (mg/L), Biochemical Oxygen Demand (BOD mg/L), Turbidity (NTU), Total Dissolved Solids (TDS mg/L), Water Temperature (°C)
* **Monitored Basins**: Waddepally Lake, Bhadrakali Lake, Dharmasagar Reservoir, Kakatiya Canal Outlet
* **Critical Operational Rule**: Government water quality records represent periodic laboratory sampling dates. Actual sampling dates are explicitly surfaced in the UI to prevent misrepresenting periodic data as real-time. Continuous real-time hydrological data is supported via optical IoT sensor probes.
* **Data Classification**: `GOVERNMENT_DATA` / `HISTORICAL`

---

## 5. Biodiversity Occurrence Vouchers: GBIF

* **Provider**: Global Biodiversity Information Facility (GBIF)
* **Documentation**: [https://www.gbif.org/developer/summary](https://www.gbif.org/developer/summary)
* **API URL**: `https://api.gbif.org/v1/occurrence/search`
* **Authentication**: Open Access
* **License**: CC BY 4.0 / CC0
* **Query Filter**: Bound to Telangana coordinates (`decimalLatitude`, `decimalLongitude`)
* **Parameters Collected**: Scientific Name, Common Name, Taxonomic Rank, Kingdom, Basis of Record (`HUMAN_OBSERVATION`, `PRESERVED_SPECIMEN`, `MACHINE_OBSERVATION`), Observation Date, IUCN Red List Conservation Status
* **Data Classification**: `LIVE_API` / `HISTORICAL`

---

## 6. Remote Sensing & Satellite Layers: NASA GIBS

* **Provider**: NASA Global Imagery Browse Services (GIBS) / EOSDIS
* **Documentation**: [https://nasa-gibs.github.io/gibs-api-docs/](https://nasa-gibs.github.io/gibs-api-docs/)
* **Tile Standard**: Web Map Tile Service (WMTS) / EPSG:3857 (GoogleMapsCompatible)
* **Products Supported**:
  * `MODIS_Terra_CorrectedReflectance_TrueColor` — High-resolution true color optical composite
  * `MODIS_Terra_NDVI_8Day` — Normalized Difference Vegetation Index (vegetation health)
  * `VIIRS_SNPP_DayNightBand_ENCC` — Nighttime radiance and urban luminescence
* **Attribution**: NASA EOSDIS GIBS Open Data
* **Data Classification**: `HISTORICAL` / Remote Sensing

---

## 7. IoT Telemetry Streams (Waste & Energy)

* **Waste Stream**: Ultrasonic depth sensor mesh transmitting bin fill level percentage ($0-100\%$), mass ($kg$), and timestamp to `POST /api/iot/waste/readings`.
* **Energy Stream**: Automated smart electricity meters transmitting active power ($kW$), cumulative energy ($kWh$), and rooftop solar renewable generation to `POST /api/iot/energy/readings`.
* **Data Classification**: `IOT_SENSOR`
