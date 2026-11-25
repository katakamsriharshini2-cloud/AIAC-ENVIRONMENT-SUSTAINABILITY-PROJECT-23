// API base URL — reads from .env (VITE_API_URL) or defaults to localhost:8000
const API_BASE = (typeof import.meta !== "undefined" && import.meta.env?.VITE_API_URL) || "http://localhost:8000";

async function request(endpoint, options = {}) {
  const token = localStorage.getItem("ecosphere_token");
  const headers = {
    "Content-Type": "application/json",
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
    ...options.headers,
  };

  let res;
  try {
    res = await fetch(`${API_BASE}${endpoint}`, { ...options, headers });
  } catch (networkErr) {
    // fetch() itself threw — backend is not running or unreachable
    throw new Error(
      "Cannot reach the backend server at " + API_BASE + ". " +
      "Please make sure the backend is running: " +
      "cd backend && python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload"
    );
  }

  if (!res.ok) {
    let detail = res.statusText;
    try {
      const err = await res.json();
      detail = err.detail || err.message || detail;
    } catch {
      // Response body was not JSON — keep statusText
    }
    throw new Error(detail || `Request failed (HTTP ${res.status})`);
  }

  return res.json();
}

// Auth
export const authApi = {
  login: (email, password) =>
    request("/api/auth/login", { method: "POST", body: JSON.stringify({ email, password }) }),
  register: (data) =>
    request("/api/auth/register", { method: "POST", body: JSON.stringify(data) }),
  me: () => request("/api/auth/me"),
};

// Overview & Live Data
export const liveApi = {
  status:       ()       => request("/api/live-data/status"),
  airQuality:   (city)   => request(`/api/live-data/air-quality?city=${city || "Warangal"}`),
  weather:      ()       => request("/api/live-data/weather"),
  waterQuality: ()       => request("/api/live-data/water-quality"),
  biodiversity: ()       => request("/api/live-data/biodiversity"),
  satellite:    (date)   => request(`/api/live-data/satellite${date ? "?date=" + date : ""}`),
  waste:        ()       => request("/api/live-data/waste"),
  energy:       ()       => request("/api/live-data/energy"),
  history:      (limit)  => request(`/api/live-data/history?limit=${limit || 20}`),
  refresh:      (prov)   => request(`/api/live-data/refresh${prov ? "?provider=" + prov : ""}`, { method: "POST" }),
};

// Analytics
export const analyticsApi = {
  overview:      ()       => request("/api/analytics/overview"),
  airQuality:    (loc)    => request(`/api/analytics/air-quality${loc ? "?location=" + loc : ""}`),
  waterQuality:  ()       => request("/api/analytics/water-quality"),
  waste:         ()       => request("/api/analytics/waste"),
  energy:        ()       => request("/api/analytics/energy"),
  sustainability:()       => request("/api/analytics/sustainability"),
  exportCsv:     (metric) => `${API_BASE}/api/analytics/export/csv?metric=${metric}`,
  exportPdf:     ()       => `${API_BASE}/api/analytics/export/pdf`,
};

// AI
export const aiApi = {
  predict: (metric, hours, location) =>
    request("/api/ai/predict", {
      method: "POST",
      body: JSON.stringify({ target_metric: metric, horizon_hours: hours, location_name: location }),
    }),
  insights:        ()              => request("/api/ai/insights"),
  anomalyDetection:(metric, sigma) =>
    request("/api/ai/anomaly-detection", {
      method: "POST",
      body: JSON.stringify({ metric, threshold_sigma: sigma }),
    }),
};

// Optimization
export const optimizationApi = {
  optimizeWaste: () =>
    request("/api/optimization/waste", { method: "POST", body: JSON.stringify({}) }),
  allocateResources: (teams, inspectors) =>
    request("/api/optimization/resources", {
      method: "POST",
      body: JSON.stringify({ available_emergency_teams: teams, available_inspectors: inspectors }),
    }),
  results: () => request("/api/optimization/results"),
};

// CRUD endpoints
export const crudApi = {
  stations:       ()        => request("/api/stations"),
  incidents:      (status)  => request(`/api/incidents${status ? "?status_filter=" + status : ""}`),
  createIncident: (data)    => request("/api/incidents", { method: "POST", body: JSON.stringify(data) }),
  updateIncident: (id, data)=> request(`/api/incidents/${id}`, { method: "PUT", body: JSON.stringify(data) }),
  initiatives:    ()        => request("/api/initiatives"),
  airQuality:     (limit)   => request(`/api/air-quality?limit=${limit || 50}`),
  waterQuality:   (limit)   => request(`/api/water-quality?limit=${limit || 50}`),
  weather:        (limit)   => request(`/api/weather?limit=${limit || 50}`),
  waste:          (limit)   => request(`/api/waste?limit=${limit || 50}`),
  energy:         (limit)   => request(`/api/energy?limit=${limit || 50}`),
  biodiversity:   (limit)   => request(`/api/biodiversity?limit=${limit || 50}`),
};

// Portal
export const portalApi = {
  submitReport: (data)     => request("/api/portal/reports", { method: "POST", body: JSON.stringify(data) }),
  listReports:  (category) => request(`/api/portal/reports${category ? "?category=" + category : ""}`),
  trackReport:  (code)     => request(`/api/portal/reports/track/${code}`),
};

// IoT
export const iotApi = {
  wasteReading:  (data) => request("/api/iot/waste/readings",  { method: "POST", body: JSON.stringify(data) }),
  energyReading: (data) => request("/api/iot/energy/readings", { method: "POST", body: JSON.stringify(data) }),
  waterReading:  (data) => request("/api/iot/water/readings",  { method: "POST", body: JSON.stringify(data) }),
};
