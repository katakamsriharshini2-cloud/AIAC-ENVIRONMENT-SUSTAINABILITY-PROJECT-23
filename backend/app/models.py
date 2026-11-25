import datetime
from sqlalchemy import (
    Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey, UniqueConstraint, Index
)
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    role = Column(String(50), default="public_user", nullable=False)  # admin, environmental_officer, public_user
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    incidents_reported = relationship("EnvironmentalIncident", back_populates="reporter", foreign_keys="EnvironmentalIncident.reported_by_user_id")
    incidents_assigned = relationship("EnvironmentalIncident", back_populates="assigned_officer", foreign_keys="EnvironmentalIncident.assigned_officer_id")
    audit_logs = relationship("AuditLog", back_populates="user")


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(255), nullable=True)


class MonitoringStation(Base):
    __tablename__ = "monitoring_stations"

    id = Column(Integer, primary_key=True, index=True)
    station_code = Column(String(100), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    city = Column(String(100), index=True, nullable=False)
    state = Column(String(100), nullable=False)
    country = Column(String(100), default="India", nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    station_type = Column(String(50), default="INTEGRATED")  # AIR, WATER, WEATHER, INTEGRATED
    status = Column(String(50), default="ACTIVE")  # ACTIVE, MAINTENANCE, INACTIVE
    source_type = Column(String(50), default="CPCB")  # CPCB, OPENAQ, STATE_BOARD, IOT
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    air_records = relationship("AirQualityRecord", back_populates="station", cascade="all, delete-orphan")
    water_records = relationship("WaterQualityRecord", back_populates="station", cascade="all, delete-orphan")
    weather_records = relationship("WeatherRecord", back_populates="station", cascade="all, delete-orphan")


class AirQualityRecord(Base):
    __tablename__ = "air_quality_records"

    id = Column(Integer, primary_key=True, index=True)
    station_id = Column(Integer, ForeignKey("monitoring_stations.id", ondelete="SET NULL"), nullable=True, index=True)
    location_name = Column(String(255), nullable=False, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    observation_timestamp = Column(DateTime, nullable=False, index=True)
    retrieval_timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    
    aqi = Column(Float, nullable=True)
    aqi_category = Column(String(50), nullable=True)  # Good, Satisfactory, Moderate, Poor, Very Poor, Severe
    pm25 = Column(Float, nullable=True)
    pm10 = Column(Float, nullable=True)
    no2 = Column(Float, nullable=True)
    so2 = Column(Float, nullable=True)
    co = Column(Float, nullable=True)
    o3 = Column(Float, nullable=True)
    dominant_pollutant = Column(String(50), nullable=True)
    unit = Column(String(50), default="µg/m³")

    data_quality_status = Column(String(50), default="VERIFIED")  # VERIFIED, PROVISIONAL, SUSPECT, RAW
    data_type = Column(String(50), default="LIVE_API")  # LIVE_API, HISTORICAL, GOVERNMENT_DATA, IOT_SENSOR, SIMULATED
    source_name = Column(String(100), nullable=False)  # CPCB, OpenAQ
    source_url = Column(String(500), nullable=True)

    station = relationship("MonitoringStation", back_populates="air_records")

    __table_args__ = (
        UniqueConstraint("location_name", "observation_timestamp", "source_name", name="uq_air_reading"),
        Index("idx_air_time_loc", "location_name", "observation_timestamp"),
    )


class WaterQualityRecord(Base):
    __tablename__ = "water_quality_records"

    id = Column(Integer, primary_key=True, index=True)
    station_id = Column(Integer, ForeignKey("monitoring_stations.id", ondelete="SET NULL"), nullable=True, index=True)
    water_body_name = Column(String(255), nullable=False, index=True)  # e.g., Wadepally Tank, Bhadrakali Lake, Godavari River
    location_name = Column(String(255), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    observation_timestamp = Column(DateTime, nullable=False, index=True)
    retrieval_timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    ph = Column(Float, nullable=True)
    dissolved_oxygen = Column(Float, nullable=True)  # mg/L
    bod = Column(Float, nullable=True)               # Biochemical Oxygen Demand, mg/L
    turbidity = Column(Float, nullable=True)         # NTU
    tds = Column(Float, nullable=True)               # Total Dissolved Solids, mg/L
    water_temperature = Column(Float, nullable=True) # °C
    water_quality_index = Column(Float, nullable=True) # 0 - 100 WQI
    wqi_status = Column(String(50), nullable=True)    # Excellent, Good, Poor, Very Poor, Unsuitable

    data_quality_status = Column(String(50), default="VERIFIED")
    data_type = Column(String(50), default="GOVERNMENT_DATA")  # GOVERNMENT_DATA, IOT_SENSOR, HISTORICAL, SIMULATED
    source_name = Column(String(100), nullable=False)
    source_url = Column(String(500), nullable=True)

    station = relationship("MonitoringStation", back_populates="water_records")

    __table_args__ = (
        UniqueConstraint("water_body_name", "observation_timestamp", "source_name", name="uq_water_reading"),
    )


class WeatherRecord(Base):
    __tablename__ = "weather_records"

    id = Column(Integer, primary_key=True, index=True)
    station_id = Column(Integer, ForeignKey("monitoring_stations.id", ondelete="SET NULL"), nullable=True, index=True)
    location_name = Column(String(255), nullable=False, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    observation_timestamp = Column(DateTime, nullable=False, index=True)
    retrieval_timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    temperature = Column(Float, nullable=False)           # °C
    apparent_temperature = Column(Float, nullable=True)   # °C
    humidity = Column(Float, nullable=False)              # %
    rainfall = Column(Float, default=0.0)                 # mm
    precipitation = Column(Float, default=0.0)           # mm
    wind_speed = Column(Float, nullable=True)             # km/h
    wind_direction = Column(Float, nullable=True)         # degrees
    atmospheric_pressure = Column(Float, nullable=True)   # hPa
    cloud_cover = Column(Float, nullable=True)            # %
    weather_condition = Column(String(100), default="Clear")

    is_forecast = Column(Boolean, default=False)
    forecast_date = Column(DateTime, nullable=True)

    data_quality_status = Column(String(50), default="VERIFIED")
    data_type = Column(String(50), default="LIVE_API")
    source_name = Column(String(100), default="Open-Meteo")
    source_url = Column(String(500), nullable=True)

    station = relationship("MonitoringStation", back_populates="weather_records")

    __table_args__ = (
        UniqueConstraint("location_name", "observation_timestamp", "is_forecast", name="uq_weather_reading"),
    )


class WasteRecord(Base):
    __tablename__ = "waste_records"

    id = Column(Integer, primary_key=True, index=True)
    bin_id = Column(String(100), nullable=False, index=True)
    location_name = Column(String(255), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    timestamp = Column(DateTime, nullable=False, index=True)

    bin_fill_percentage = Column(Float, nullable=False)   # 0 to 100 %
    waste_quantity_kg = Column(Float, nullable=False)
    waste_type = Column(String(50), default="GENERAL")    # ORGANIC, RECYCLABLE, HAZARDOUS, GENERAL
    collection_status = Column(String(50), default="PENDING")  # PENDING, SCHEDULED, COLLECTED, OVERFLOW
    recycling_status = Column(String(50), default="NOT_RECYCLED") # NOT_RECYCLED, PROCESSING, RECYCLED

    data_quality_status = Column(String(50), default="VERIFIED")
    data_type = Column(String(50), default="IOT_SENSOR")
    source_name = Column(String(100), default="Smart Waste Sensor")


class EnergyRecord(Base):
    __tablename__ = "energy_records"

    id = Column(Integer, primary_key=True, index=True)
    meter_id = Column(String(100), nullable=False, index=True)
    location_name = Column(String(255), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    timestamp = Column(DateTime, nullable=False, index=True)

    consumption_kwh = Column(Float, nullable=False)
    power_kw = Column(Float, nullable=False)
    renewable_generation_kwh = Column(Float, default=0.0)
    renewable_percentage = Column(Float, default=0.0)     # %
    energy_source = Column(String(50), default="GRID")    # GRID, SOLAR, WIND, HYBRID

    data_quality_status = Column(String(50), default="VERIFIED")
    data_type = Column(String(50), default="IOT_SENSOR")
    source_name = Column(String(100), default="Smart Energy Meter")


class BiodiversityRecord(Base):
    __tablename__ = "biodiversity_records"

    id = Column(Integer, primary_key=True, index=True)
    species_name = Column(String(255), nullable=False, index=True)
    scientific_name = Column(String(255), nullable=False, index=True)
    category = Column(String(100), nullable=False)        # AVES, MAMMALIA, REPTILIA, PLANTAE, INSECTA
    observation_date = Column(DateTime, nullable=False, index=True)
    location_name = Column(String(255), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    basis_of_record = Column(String(100), default="HUMAN_OBSERVATION")
    conservation_status = Column(String(50), default="LC") # LC, NT, VU, EN, CR
    country = Column(String(100), default="India")
    state = Column(String(100), default="Telangana")
    city = Column(String(100), default="Warangal")

    data_type = Column(String(50), default="GOVERNMENT_DATA")
    source_name = Column(String(100), default="GBIF")
    source_url = Column(String(500), nullable=True)


class EnvironmentalIncident(Base):
    __tablename__ = "environmental_incidents"

    id = Column(Integer, primary_key=True, index=True)
    incident_code = Column(String(100), unique=True, index=True, nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    incident_type = Column(String(50), nullable=False)  # AIR_POLLUTION, WATER_POLLUTION, ILLEGAL_DUMPING, DEFORESTATION, NOISE
    severity = Column(String(50), default="MEDIUM")      # LOW, MEDIUM, HIGH, CRITICAL
    status = Column(String(50), default="REPORTED")      # REPORTED, INVESTIGATING, ACTION_TAKEN, RESOLVED, CLOSED
    location_name = Column(String(255), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    reported_by_user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    assigned_officer_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    evidence_url = Column(String(500), nullable=True)
    resolution_notes = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)

    reporter = relationship("User", back_populates="incidents_reported", foreign_keys=[reported_by_user_id])
    assigned_officer = relationship("User", back_populates="incidents_assigned", foreign_keys=[assigned_officer_id])


class SustainabilityInitiative(Base):
    __tablename__ = "sustainability_initiatives"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False)       # CLEAN_AIR, WATER_CONSERVATION, ZERO_WASTE, RENEWABLE_ENERGY, URBAN_FOREST
    description = Column(Text, nullable=False)
    target_reduction_pct = Column(Float, default=20.0)
    current_progress_pct = Column(Float, default=0.0)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    status = Column(String(50), default="IN_PROGRESS")   # PLANNED, IN_PROGRESS, COMPLETED
    leader_name = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    alert_type = Column(String(50), default="SYSTEM")    # AQI_ALERT, WATER_RISK, WASTE_OVERFLOW, INCIDENT_UPDATE, SYSTEM
    severity = Column(String(50), default="INFO")        # INFO, WARNING, CRITICAL
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class PublicReport(Base):
    __tablename__ = "public_reports"

    id = Column(Integer, primary_key=True, index=True)
    report_code = Column(String(100), unique=True, index=True, nullable=False)
    reporter_name = Column(String(100), nullable=False)
    reporter_contact = Column(String(100), nullable=True)
    category = Column(String(50), nullable=False)        # AIR, WATER, WASTE, NOISE, OTHER
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    location_name = Column(String(255), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    photo_url = Column(String(500), nullable=True)
    status = Column(String(50), default="SUBMITTED")     # SUBMITTED, UNDER_REVIEW, ACTION_TAKEN, RESOLVED, REJECTED
    verification_notes = Column(Text, nullable=True)
    officer_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)


class CollectionSchedule(Base):
    __tablename__ = "collection_schedules"

    id = Column(Integer, primary_key=True, index=True)
    route_name = Column(String(255), nullable=False)
    schedule_date = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(String(50), default="PLANNED")       # PLANNED, IN_PROGRESS, COMPLETED
    optimized_path_json = Column(Text, nullable=False)
    total_distance_km = Column(Float, nullable=False)
    bins_covered_count = Column(Integer, nullable=False)
    fuel_saved_liters = Column(Float, default=0.0)
    algorithm_used = Column(String(100), default="Dijkstra + Priority Queue")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class PredictionResult(Base):
    __tablename__ = "prediction_results"

    id = Column(Integer, primary_key=True, index=True)
    target_metric = Column(String(100), nullable=False)  # AQI, TEMPERATURE, RAINFALL, ENERGY_KWH, WASTE_KG
    model_name = Column(String(100), nullable=False)     # RidgeRegression, RandomForestRegressor, LinearRegression
    location_name = Column(String(255), nullable=False)
    forecast_timestamp = Column(DateTime, nullable=False)
    predicted_value = Column(Float, nullable=False)
    actual_value = Column(Float, nullable=True)
    confidence_lower = Column(Float, nullable=False)
    confidence_upper = Column(Float, nullable=False)
    mae = Column(Float, nullable=True)
    rmse = Column(Float, nullable=True)
    r2 = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    action = Column(String(100), nullable=False)
    entity = Column(String(100), nullable=False)
    entity_id = Column(String(100), nullable=True)
    details = Column(Text, nullable=True)
    ip_address = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="audit_logs")


class DataSource(Base):
    __tablename__ = "data_sources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    code = Column(String(50), unique=True, nullable=False)
    base_url = Column(String(500), nullable=False)
    data_type = Column(String(50), default="LIVE_API")   # LIVE_API, GOVERNMENT_DATA, HISTORICAL, IOT_SENSOR
    is_active = Column(Boolean, default=True)
    refresh_interval_minutes = Column(Integer, default=15)
    last_sync_timestamp = Column(DateTime, nullable=True)
    status = Column(String(50), default="HEALTHY")       # HEALTHY, DEGRADED, OFFLINE, STALE
    error_details = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)


class ApiSyncLog(Base):
    __tablename__ = "api_sync_logs"

    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(Integer, ForeignKey("data_sources.id", ondelete="CASCADE"), nullable=True)
    source_code = Column(String(50), nullable=False, index=True)
    status = Column(String(50), nullable=False)          # SUCCESS, FAILURE, PARTIAL
    records_fetched = Column(Integer, default=0)
    duration_ms = Column(Integer, default=0)
    error_message = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, index=True)
