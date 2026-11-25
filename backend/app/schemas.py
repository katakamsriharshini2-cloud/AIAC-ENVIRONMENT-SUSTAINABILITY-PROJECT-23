from pydantic import BaseModel, Field
from typing import Optional, List, Any, Dict
from datetime import datetime

# ----------------- AUTH & USER SCHEMAS -----------------
class UserRegister(BaseModel):
    email: str = Field(..., description="User email address")
    password: str = Field(..., min_length=6)
    full_name: str
    role: Optional[str] = "public_user"  # admin, environmental_officer, public_user

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None


# ----------------- STATION SCHEMAS -----------------
class StationBase(BaseModel):
    station_code: str
    name: str
    city: str
    state: str
    country: str = "India"
    latitude: float
    longitude: float
    station_type: str = "INTEGRATED"
    status: str = "ACTIVE"
    source_type: str = "CPCB"

class StationCreate(StationBase):
    pass

class StationUpdate(BaseModel):
    name: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    station_type: Optional[str] = None
    status: Optional[str] = None

class StationResponse(StationBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ----------------- AIR QUALITY SCHEMAS -----------------
class AirQualityBase(BaseModel):
    location_name: str
    latitude: float
    longitude: float
    observation_timestamp: datetime
    aqi: Optional[float] = None
    aqi_category: Optional[str] = None
    pm25: Optional[float] = None
    pm10: Optional[float] = None
    no2: Optional[float] = None
    so2: Optional[float] = None
    co: Optional[float] = None
    o3: Optional[float] = None
    dominant_pollutant: Optional[str] = None
    unit: str = "µg/m³"
    data_quality_status: str = "VERIFIED"
    data_type: str = "LIVE_API"
    source_name: str
    source_url: Optional[str] = None

class AirQualityCreate(AirQualityBase):
    station_id: Optional[int] = None

class AirQualityResponse(AirQualityBase):
    id: int
    station_id: Optional[int] = None
    retrieval_timestamp: datetime

    class Config:
        from_attributes = True


# ----------------- WATER QUALITY SCHEMAS -----------------
class WaterQualityBase(BaseModel):
    water_body_name: str
    location_name: str
    latitude: float
    longitude: float
    observation_timestamp: datetime
    ph: Optional[float] = None
    dissolved_oxygen: Optional[float] = None
    bod: Optional[float] = None
    turbidity: Optional[float] = None
    tds: Optional[float] = None
    water_temperature: Optional[float] = None
    water_quality_index: Optional[float] = None
    wqi_status: Optional[str] = None
    data_quality_status: str = "VERIFIED"
    data_type: str = "GOVERNMENT_DATA"
    source_name: str
    source_url: Optional[str] = None

class WaterQualityCreate(WaterQualityBase):
    station_id: Optional[int] = None

class WaterQualityResponse(WaterQualityBase):
    id: int
    station_id: Optional[int] = None
    retrieval_timestamp: datetime

    class Config:
        from_attributes = True


# ----------------- WEATHER SCHEMAS -----------------
class WeatherBase(BaseModel):
    location_name: str
    latitude: float
    longitude: float
    observation_timestamp: datetime
    temperature: float
    apparent_temperature: Optional[float] = None
    humidity: float
    rainfall: float = 0.0
    precipitation: float = 0.0
    wind_speed: Optional[float] = None
    wind_direction: Optional[float] = None
    atmospheric_pressure: Optional[float] = None
    cloud_cover: Optional[float] = None
    weather_condition: str = "Clear"
    is_forecast: bool = False
    forecast_date: Optional[datetime] = None
    data_quality_status: str = "VERIFIED"
    data_type: str = "LIVE_API"
    source_name: str = "Open-Meteo"
    source_url: Optional[str] = None

class WeatherCreate(WeatherBase):
    station_id: Optional[int] = None

class WeatherResponse(WeatherBase):
    id: int
    station_id: Optional[int] = None
    retrieval_timestamp: datetime

    class Config:
        from_attributes = True


# ----------------- WASTE & ENERGY SCHEMAS -----------------
class WasteBase(BaseModel):
    bin_id: str
    location_name: str
    latitude: float
    longitude: float
    timestamp: datetime
    bin_fill_percentage: float
    waste_quantity_kg: float
    waste_type: str = "GENERAL"
    collection_status: str = "PENDING"
    recycling_status: str = "NOT_RECYCLED"
    data_quality_status: str = "VERIFIED"
    data_type: str = "IOT_SENSOR"
    source_name: str = "Smart Waste Sensor"

class WasteCreate(WasteBase):
    pass

class WasteResponse(WasteBase):
    id: int

    class Config:
        from_attributes = True

class EnergyBase(BaseModel):
    meter_id: str
    location_name: str
    latitude: float
    longitude: float
    timestamp: datetime
    consumption_kwh: float
    power_kw: float
    renewable_generation_kwh: float = 0.0
    renewable_percentage: float = 0.0
    energy_source: str = "GRID"
    data_quality_status: str = "VERIFIED"
    data_type: str = "IOT_SENSOR"
    source_name: str = "Smart Energy Meter"

class EnergyCreate(EnergyBase):
    pass

class EnergyResponse(EnergyBase):
    id: int

    class Config:
        from_attributes = True


# ----------------- BIODIVERSITY SCHEMAS -----------------
class BiodiversityBase(BaseModel):
    species_name: str
    scientific_name: str
    category: str
    observation_date: datetime
    location_name: str
    latitude: float
    longitude: float
    basis_of_record: str = "HUMAN_OBSERVATION"
    conservation_status: str = "LC"
    country: str = "India"
    state: str = "Telangana"
    city: str = "Warangal"
    data_type: str = "GOVERNMENT_DATA"
    source_name: str = "GBIF"
    source_url: Optional[str] = None

class BiodiversityCreate(BiodiversityBase):
    pass

class BiodiversityResponse(BiodiversityBase):
    id: int

    class Config:
        from_attributes = True


# ----------------- INCIDENT & REPORT SCHEMAS -----------------
class IncidentBase(BaseModel):
    title: str
    description: str
    incident_type: str
    severity: str = "MEDIUM"
    location_name: str
    latitude: float
    longitude: float
    evidence_url: Optional[str] = None

class IncidentCreate(IncidentBase):
    pass

class IncidentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    severity: Optional[str] = None
    status: Optional[str] = None
    assigned_officer_id: Optional[int] = None
    resolution_notes: Optional[str] = None

class IncidentResponse(IncidentBase):
    id: int
    incident_code: str
    status: str
    reported_by_user_id: Optional[int] = None
    assigned_officer_id: Optional[int] = None
    resolution_notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    resolved_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class PublicReportCreate(BaseModel):
    reporter_name: str
    reporter_contact: Optional[str] = None
    category: str
    title: str
    description: str
    location_name: str
    latitude: float
    longitude: float
    photo_url: Optional[str] = None

class PublicReportUpdate(BaseModel):
    status: Optional[str] = None
    verification_notes: Optional[str] = None
    officer_id: Optional[int] = None

class PublicReportResponse(BaseModel):
    id: int
    report_code: str
    reporter_name: str
    reporter_contact: Optional[str] = None
    category: str
    title: str
    description: str
    location_name: str
    latitude: float
    longitude: float
    photo_url: Optional[str] = None
    status: str
    verification_notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ----------------- SUSTAINABILITY SCHEMAS -----------------
class InitiativeBase(BaseModel):
    title: str
    category: str
    description: str
    target_reduction_pct: float = 20.0
    current_progress_pct: float = 0.0
    start_date: datetime
    end_date: datetime
    status: str = "IN_PROGRESS"
    leader_name: Optional[str] = None

class InitiativeCreate(InitiativeBase):
    pass

class InitiativeUpdate(BaseModel):
    title: Optional[str] = None
    target_reduction_pct: Optional[float] = None
    current_progress_pct: Optional[float] = None
    status: Optional[str] = None

class InitiativeResponse(InitiativeBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ----------------- AI & OPTIMIZATION SCHEMAS -----------------
class PredictRequest(BaseModel):
    target_metric: str = "AQI"  # AQI, TEMPERATURE, RAINFALL, ENERGY_KWH, WASTE_KG
    horizon_hours: int = 24
    location_name: Optional[str] = "Warangal"

class PredictionPoint(BaseModel):
    timestamp: str
    predicted_value: float
    confidence_lower: float
    confidence_upper: float

class PredictResponse(BaseModel):
    target_metric: str
    model_name: str
    location_name: str
    mae: float
    rmse: float
    r2: float
    historical_points_used: int
    predictions: List[PredictionPoint]
    actual_vs_predicted_recent: List[Dict[str, Any]]

class AnomalyDetectRequest(BaseModel):
    metric: str = "AQI"  # AQI, PM25, WATER_PH, WATER_DO, ENERGY_KWH, WASTE_FILL
    threshold_sigma: float = 2.5

class AnomalyItem(BaseModel):
    id: int
    timestamp: str
    location: str
    value: float
    expected_range: str
    anomaly_score: float
    severity: str
    explanation: str

class AnomalyDetectResponse(BaseModel):
    metric: str
    anomalies_detected_count: int
    total_evaluated: int
    anomalies: List[AnomalyItem]

class WasteOptimizationRequest(BaseModel):
    depot_location: str = "Warangal Central Sanitation Depot"
    max_vehicle_capacity_kg: float = 4000.0

class WasteOptimizationResponse(BaseModel):
    route_name: str
    schedule_date: str
    algorithm: str
    original_distance_km: float
    optimized_distance_km: float
    distance_saved_km: float
    efficiency_gain_pct: float
    fuel_saved_liters: float
    co2_reduction_kg: float
    total_waste_collected_kg: float
    bins_visited_count: int
    stops_in_order: List[Dict[str, Any]]

class ResourceAllocationRequest(BaseModel):
    available_emergency_teams: int = 5
    available_inspectors: int = 4

class ResourceAllocationResponse(BaseModel):
    total_allocations: int
    allocations: List[Dict[str, Any]]
    explanation: str


# ----------------- IOT READING SCHEMAS -----------------
class IoTReadingsWaste(BaseModel):
    bin_id: str
    location_name: str
    latitude: float
    longitude: float
    bin_fill_percentage: float
    waste_quantity_kg: float
    waste_type: Optional[str] = "GENERAL"
    timestamp: Optional[datetime] = None

class IoTReadingsEnergy(BaseModel):
    meter_id: str
    location_name: str
    latitude: float
    longitude: float
    consumption_kwh: float
    power_kw: float
    renewable_generation_kwh: Optional[float] = 0.0
    energy_source: Optional[str] = "GRID"
    timestamp: Optional[datetime] = None

class IoTReadingsWater(BaseModel):
    sensor_id: str
    water_body_name: str
    location_name: str
    latitude: float
    longitude: float
    ph: float
    dissolved_oxygen: float
    turbidity: float
    tds: float
    water_temperature: float
    timestamp: Optional[datetime] = None


# ----------------- DATA SOURCE & SYNC SCHEMAS -----------------
class DataSourceResponse(BaseModel):
    id: int
    name: str
    code: str
    base_url: str
    data_type: str
    is_active: bool
    refresh_interval_minutes: int
    last_sync_timestamp: Optional[datetime] = None
    status: str
    error_details: Optional[str] = None

    class Config:
        from_attributes = True

class ApiSyncLogResponse(BaseModel):
    id: int
    source_code: str
    status: str
    records_fetched: int
    duration_ms: int
    error_message: Optional[str] = None
    timestamp: datetime

    class Config:
        from_attributes = True
