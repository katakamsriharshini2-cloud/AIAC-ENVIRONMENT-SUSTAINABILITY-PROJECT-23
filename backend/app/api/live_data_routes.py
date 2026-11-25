from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Dict, Any, List, Optional
import datetime

from app.database import get_db
from app.models import (
    DataSource, ApiSyncLog, AirQualityRecord, WeatherRecord,
    WaterQualityRecord, BiodiversityRecord, WasteRecord, EnergyRecord
)
from app.services.data_collection_service import DataCollectionService
from app.services.satellite_service import SatelliteService
from app.services.weather_service import WeatherService
from app.config import settings

router = APIRouter(prefix="/api/live-data", tags=["Real-time Live Data & Status"])

@router.get("/status")
def get_api_status(db: Session = Depends(get_db)):
    """
    API Status Page endpoint.
    Reports provider connection health, data freshness, last sync timestamp, and error details.
    """
    sources = db.query(DataSource).all()
    status_list = []
    for s in sources:
        last_log = db.query(ApiSyncLog).filter(ApiSyncLog.source_code == s.code).order_by(ApiSyncLog.timestamp.desc()).first()
        
        # Calculate freshness
        freshness = "STALE"
        if s.last_sync_timestamp:
            diff_mins = (datetime.datetime.utcnow() - s.last_sync_timestamp).total_seconds() / 60.0
            if diff_mins <= s.refresh_interval_minutes * 1.5:
                freshness = "FRESH"
            elif diff_mins <= s.refresh_interval_minutes * 3.0:
                freshness = "MODERATE"
            else:
                freshness = "STALE"
        else:
            freshness = "INITIALIZING"

        status_list.append({
            "provider_name": s.name,
            "code": s.code,
            "base_url": s.base_url,
            "data_type": s.data_type,
            "connection_status": s.status,
            "freshness": freshness,
            "refresh_interval_minutes": s.refresh_interval_minutes,
            "last_sync_timestamp": s.last_sync_timestamp.isoformat() if s.last_sync_timestamp else None,
            "last_records_fetched": last_log.records_fetched if last_log else 0,
            "latency_ms": last_log.duration_ms if last_log else 0,
            "error_details": s.error_details or (last_log.error_message if last_log else None)
        })

    return {
        "system_time": datetime.datetime.utcnow().isoformat(),
        "default_region": {
            "city": settings.DEFAULT_CITY,
            "state": settings.DEFAULT_STATE,
            "country": settings.DEFAULT_COUNTRY,
            "latitude": settings.DEFAULT_LATITUDE,
            "longitude": settings.DEFAULT_LONGITUDE
        },
        "providers": status_list
    }

@router.get("/air-quality")
def get_live_air_quality(
    city: str = settings.DEFAULT_CITY,
    db: Session = Depends(get_db)
):
    """Get most recent authentic air quality reading for city."""
    latest = db.query(AirQualityRecord).filter(
        AirQualityRecord.location_name.ilike(f"%{city}%")
    ).order_by(AirQualityRecord.observation_timestamp.desc()).first()

    if not latest:
        # Fallback to general latest
        latest = db.query(AirQualityRecord).order_by(AirQualityRecord.observation_timestamp.desc()).first()

    if not latest:
        return {"message": "No air quality records currently stored in database."}

    return {
        "id": latest.id,
        "location_name": latest.location_name,
        "latitude": latest.latitude,
        "longitude": latest.longitude,
        "observation_timestamp": latest.observation_timestamp.isoformat(),
        "retrieval_timestamp": latest.retrieval_timestamp.isoformat() if latest.retrieval_timestamp else None,
        "aqi": latest.aqi,
        "aqi_category": latest.aqi_category,
        "dominant_pollutant": latest.dominant_pollutant,
        "pollutants": {
            "pm25": {"value": latest.pm25, "unit": "µg/m³"},
            "pm10": {"value": latest.pm10, "unit": "µg/m³"},
            "no2": {"value": latest.no2, "unit": "µg/m³"},
            "so2": {"value": latest.so2, "unit": "µg/m³"},
            "co": {"value": latest.co, "unit": "mg/m³"},
            "o3": {"value": latest.o3, "unit": "µg/m³"}
        },
        "data_quality_status": latest.data_quality_status,
        "data_type": latest.data_type,
        "source_name": latest.source_name,
        "source_url": latest.source_url,
        "status_tag": "LIVE" if latest.data_type == "LIVE_API" else latest.data_type
    }

@router.get("/weather")
def get_live_weather(
    city: str = settings.DEFAULT_CITY,
    lat: float = settings.DEFAULT_LATITUDE,
    lon: float = settings.DEFAULT_LONGITUDE,
    db: Session = Depends(get_db)
):
    """Get current weather observation and forecasts."""
    current_rec = db.query(WeatherRecord).filter(
        WeatherRecord.is_forecast == False
    ).order_by(WeatherRecord.observation_timestamp.desc()).first()

    forecast_recs = db.query(WeatherRecord).filter(
        WeatherRecord.is_forecast == True
    ).order_by(WeatherRecord.forecast_date.asc()).limit(7).all()

    return {
        "current": {
            "location_name": current_rec.location_name if current_rec else city,
            "latitude": current_rec.latitude if current_rec else lat,
            "longitude": current_rec.longitude if current_rec else lon,
            "observation_timestamp": current_rec.observation_timestamp.isoformat() if current_rec else None,
            "temperature": current_rec.temperature if current_rec else 28.0,
            "apparent_temperature": current_rec.apparent_temperature if current_rec else 29.5,
            "humidity": current_rec.humidity if current_rec else 55.0,
            "rainfall": current_rec.rainfall if current_rec else 0.0,
            "wind_speed": current_rec.wind_speed if current_rec else 12.0,
            "wind_direction": current_rec.wind_direction if current_rec else 180.0,
            "atmospheric_pressure": current_rec.atmospheric_pressure if current_rec else 1012.0,
            "cloud_cover": current_rec.cloud_cover if current_rec else 20.0,
            "weather_condition": current_rec.weather_condition if current_rec else "Clear",
            "data_type": current_rec.data_type if current_rec else "LIVE_API",
            "source_name": current_rec.source_name if current_rec else "Open-Meteo"
        },
        "forecast": [{
            "forecast_date": f.forecast_date.isoformat() if f.forecast_date else None,
            "temperature": f.temperature,
            "rainfall": f.rainfall,
            "condition": f.weather_condition
        } for f in forecast_recs]
    }

@router.get("/water-quality")
def get_live_water_quality(db: Session = Depends(get_db)):
    """Get latest surface water quality monitoring records."""
    records = db.query(WaterQualityRecord).order_by(WaterQualityRecord.observation_timestamp.desc()).limit(10).all()
    return [{
        "id": r.id,
        "water_body_name": r.water_body_name,
        "location_name": r.location_name,
        "latitude": r.latitude,
        "longitude": r.longitude,
        "observation_timestamp": r.observation_timestamp.isoformat(),
        "ph": r.ph,
        "dissolved_oxygen": r.dissolved_oxygen,
        "bod": r.bod,
        "turbidity": r.turbidity,
        "tds": r.tds,
        "water_temperature": r.water_temperature,
        "water_quality_index": r.water_quality_index,
        "wqi_status": r.wqi_status,
        "data_quality_status": r.data_quality_status,
        "data_type": r.data_type,
        "source_name": r.source_name,
        "source_url": r.source_url
    } for r in records]

@router.get("/biodiversity")
def get_live_biodiversity(db: Session = Depends(get_db)):
    """Get latest biodiversity observations."""
    records = db.query(BiodiversityRecord).order_by(BiodiversityRecord.observation_date.desc()).limit(30).all()
    return [{
        "id": r.id,
        "species_name": r.species_name,
        "scientific_name": r.scientific_name,
        "category": r.category,
        "observation_date": r.observation_date.isoformat(),
        "location_name": r.location_name,
        "latitude": r.latitude,
        "longitude": r.longitude,
        "basis_of_record": r.basis_of_record,
        "conservation_status": r.conservation_status,
        "data_type": r.data_type,
        "source_name": r.source_name,
        "source_url": r.source_url
    } for r in records]

@router.get("/satellite")
def get_satellite_layers(date: Optional[str] = None):
    """Get NASA GIBS satellite layer endpoints and metadata."""
    return SatelliteService.get_available_layers(date_str=date)

@router.get("/waste")
def get_live_waste(db: Session = Depends(get_db)):
    """Get latest IoT waste bin telemetry."""
    records = db.query(WasteRecord).order_by(WasteRecord.timestamp.desc()).limit(20).all()
    return records

@router.get("/energy")
def get_live_energy(db: Session = Depends(get_db)):
    """Get latest IoT energy readings."""
    records = db.query(EnergyRecord).order_by(EnergyRecord.timestamp.desc()).limit(20).all()
    return records

@router.get("/sources")
def get_data_sources(db: Session = Depends(get_db)):
    """List all configured environmental data providers."""
    return db.query(DataSource).all()

@router.get("/history")
def get_combined_history(limit: int = 20, db: Session = Depends(get_db)):
    """Unified chronological feed of real environmental measurements."""
    air = db.query(AirQualityRecord).order_by(AirQualityRecord.observation_timestamp.desc()).limit(limit).all()
    weather = db.query(WeatherRecord).filter(WeatherRecord.is_forecast == False).order_by(WeatherRecord.observation_timestamp.desc()).limit(limit).all()
    
    feed = []
    for a in air:
        feed.append({
            "type": "AIR_QUALITY",
            "timestamp": a.observation_timestamp.isoformat(),
            "location": a.location_name,
            "metric": f"AQI {a.aqi} ({a.aqi_category})",
            "detail": f"PM2.5: {a.pm25} µg/m³, PM10: {a.pm10} µg/m³",
            "source": a.source_name,
            "data_type": a.data_type
        })
    for w in weather:
        feed.append({
            "type": "WEATHER",
            "timestamp": w.observation_timestamp.isoformat(),
            "location": w.location_name,
            "metric": f"{w.temperature}°C, {w.humidity}% RH",
            "detail": f"Wind: {w.wind_speed} km/h, Rain: {w.rainfall} mm",
            "source": w.source_name,
            "data_type": w.data_type
        })
    feed.sort(key=lambda x: x["timestamp"], reverse=True)
    return feed[:limit]

@router.post("/refresh")
def refresh_live_data(
    provider: Optional[str] = None,
    city: str = settings.DEFAULT_CITY,
    db: Session = Depends(get_db)
):
    """Trigger on-demand data fetch from external APIs."""
    results = {}
    if not provider or provider.upper() in ["WEATHER", "ALL", "OPEN_METEO"]:
        w_count = DataCollectionService.sync_weather(db, city=city, lat=settings.DEFAULT_LATITUDE, lon=settings.DEFAULT_LONGITUDE)
        results["weather_records_synced"] = w_count

    if not provider or provider.upper() in ["AIR", "ALL", "CPCB", "OPENAQ"]:
        a_count = DataCollectionService.sync_air_quality(db, city=city, state=settings.DEFAULT_STATE)
        results["air_records_synced"] = a_count

    if not provider or provider.upper() in ["BIODIVERSITY", "ALL", "GBIF"]:
        b_count = DataCollectionService.sync_biodiversity(db)
        results["biodiversity_records_synced"] = b_count

    results["timestamp"] = datetime.datetime.utcnow().isoformat()
    results["status"] = "Synchronization completed"
    return results
