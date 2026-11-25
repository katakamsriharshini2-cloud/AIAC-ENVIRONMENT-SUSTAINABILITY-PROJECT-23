import datetime
import time
from typing import Dict, Any, List
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import (
    DataSource, ApiSyncLog, AirQualityRecord, WeatherRecord,
    WaterQualityRecord, BiodiversityRecord, MonitoringStation
)
from app.services.weather_service import WeatherService
from app.services.air_quality_service import AirQualityService
from app.services.cpcb_service import CPCBService
from app.services.water_quality_service import WaterQualityService
from app.services.biodiversity_service import BiodiversityService
from app.services.data_validation_service import DataValidationService

class DataCollectionService:
    """
    Central Real-Time Data Collection and Integration Engine.
    Handles automated polling, background APScheduler tasks, sync logs, and health statuses.
    """

    @classmethod
    def initialize_data_sources(cls, db: Session):
        """Seed registry of external data sources if not present."""
        sources = [
            {
                "name": "Open-Meteo Weather API",
                "code": "OPEN_METEO",
                "base_url": "https://api.open-meteo.com/v1/forecast",
                "data_type": "LIVE_API",
                "refresh_interval_minutes": 15,
                "status": "HEALTHY"
            },
            {
                "name": "CPCB Indian Air Quality Index (data.gov.in)",
                "code": "CPCB_GOV",
                "base_url": "https://api.data.gov.in/resource/3b01bcb8-0b14-4abf-b6f2-c1bfd384ba69",
                "data_type": "GOVERNMENT_DATA",
                "refresh_interval_minutes": 15,
                "status": "HEALTHY"
            },
            {
                "name": "OpenAQ Global Air Quality API",
                "code": "OPENAQ",
                "base_url": "https://api.openaq.org/v3",
                "data_type": "LIVE_API",
                "refresh_interval_minutes": 30,
                "status": "HEALTHY"
            },
            {
                "name": "National Water Quality Monitoring (data.gov.in)",
                "code": "GOV_WATER",
                "base_url": "https://data.gov.in/catalog/surface-water-quality",
                "data_type": "GOVERNMENT_DATA",
                "refresh_interval_minutes": 1440,
                "status": "HEALTHY"
            },
            {
                "name": "GBIF Biodiversity Occurrence API",
                "code": "GBIF",
                "base_url": "https://api.gbif.org/v1/occurrence/search",
                "data_type": "LIVE_API",
                "refresh_interval_minutes": 360,
                "status": "HEALTHY"
            },
            {
                "name": "NASA GIBS Satellite Earth Imagery",
                "code": "NASA_GIBS",
                "base_url": "https://gibs.earthdata.nasa.gov/wmts/epsg3857/best",
                "data_type": "LIVE_API",
                "refresh_interval_minutes": 720,
                "status": "HEALTHY"
            },
            {
                "name": "Smart Municipal Waste IoT Telemetry",
                "code": "IOT_WASTE",
                "base_url": "/api/iot/waste/readings",
                "data_type": "IOT_SENSOR",
                "refresh_interval_minutes": 5,
                "status": "HEALTHY"
            },
            {
                "name": "Smart Grid Energy IoT Telemetry",
                "code": "IOT_ENERGY",
                "base_url": "/api/iot/energy/readings",
                "data_type": "IOT_SENSOR",
                "refresh_interval_minutes": 5,
                "status": "HEALTHY"
            }
        ]

        for s in sources:
            existing = db.query(DataSource).filter(DataSource.code == s["code"]).first()
            if not existing:
                db.add(DataSource(**s))
        db.commit()

    @classmethod
    def sync_weather(cls, db: Session, city: str = "Warangal", lat: float = 17.9689, lon: float = 79.5941) -> int:
        """Poll and persist live weather and forecasts."""
        start_time = time.time()
        source = db.query(DataSource).filter(DataSource.code == "OPEN_METEO").first()
        try:
            weather_data = WeatherService.fetch_weather(lat=lat, lon=lon, city=city)
            if weather_data and "current" in weather_data:
                curr = weather_data["current"]
                validated = DataValidationService.validate_weather_record(curr)
                
                # Check duplicate
                existing = db.query(WeatherRecord).filter(
                    WeatherRecord.location_name == validated["location_name"],
                    WeatherRecord.observation_timestamp == validated["observation_timestamp"],
                    WeatherRecord.is_forecast == False
                ).first()
                if not existing:
                    rec = WeatherRecord(**validated)
                    db.add(rec)

                # Persist next 6 forecast entries
                for fc in weather_data.get("daily", [])[:6]:
                    fc_date = datetime.datetime.fromisoformat(fc["date"])
                    rec_fc = WeatherRecord(
                        location_name=city,
                        latitude=lat,
                        longitude=lon,
                        observation_timestamp=datetime.datetime.utcnow(),
                        temperature=fc.get("temp_max", 30.0),
                        humidity=50.0,
                        rainfall=fc.get("precipitation_sum", 0.0),
                        weather_condition=fc.get("condition", "Clear"),
                        is_forecast=True,
                        forecast_date=fc_date,
                        data_quality_status="PROVISIONAL",
                        data_type="LIVE_API",
                        source_name="Open-Meteo Forecast"
                    )
                    db.add(rec_fc)

                db.commit()
                duration = int((time.time() - start_time) * 1000)
                cls._log_sync(db, source, "OPEN_METEO", "SUCCESS", 1 + len(weather_data.get("daily", [])[:6]), duration)
                return 1
            else:
                duration = int((time.time() - start_time) * 1000)
                cls._log_sync(db, source, "OPEN_METEO", "FAILURE", 0, duration, "No response or network error")
                return 0
        except Exception as e:
            duration = int((time.time() - start_time) * 1000)
            cls._log_sync(db, source, "OPEN_METEO", "FAILURE", 0, duration, str(e))
            return 0

    @classmethod
    def sync_air_quality(cls, db: Session, city: str = "Warangal", state: str = "Telangana") -> int:
        """Poll and persist live air quality data from CPCB and OpenAQ."""
        start_time = time.time()
        source = db.query(DataSource).filter(DataSource.code == "CPCB_GOV").first()
        try:
            records = CPCBService.fetch_cpcb_realtime(city=city, state=state)
            count = 0
            if records:
                parsed = CPCBService.parse_station_record(records, city=city)
                if parsed:
                    validated = DataValidationService.validate_air_record(parsed)
                    existing = db.query(AirQualityRecord).filter(
                        AirQualityRecord.location_name == validated["location_name"],
                        AirQualityRecord.observation_timestamp == validated["observation_timestamp"]
                    ).first()
                    if not existing:
                        db.add(AirQualityRecord(**validated))
                        db.commit()
                        count += 1
            duration = int((time.time() - start_time) * 1000)
            status_code = "SUCCESS" if count > 0 else "PARTIAL"
            cls._log_sync(db, source, "CPCB_GOV", status_code, count, duration)
            return count
        except Exception as e:
            duration = int((time.time() - start_time) * 1000)
            cls._log_sync(db, source, "CPCB_GOV", "FAILURE", 0, duration, str(e))
            return 0

    @classmethod
    def sync_biodiversity(cls, db: Session) -> int:
        """Poll and update GBIF species occurrences."""
        start_time = time.time()
        source = db.query(DataSource).filter(DataSource.code == "GBIF").first()
        try:
            occurrences = BiodiversityService.fetch_gbif_occurrences(limit=10)
            count = 0
            for item in occurrences:
                existing = db.query(BiodiversityRecord).filter(
                    BiodiversityRecord.species_name == item["species_name"],
                    BiodiversityRecord.location_name == item["location_name"]
                ).first()
                if not existing:
                    db.add(BiodiversityRecord(**item))
                    count += 1
            db.commit()
            duration = int((time.time() - start_time) * 1000)
            cls._log_sync(db, source, "GBIF", "SUCCESS", count, duration)
            return count
        except Exception as e:
            duration = int((time.time() - start_time) * 1000)
            cls._log_sync(db, source, "GBIF", "FAILURE", 0, duration, str(e))
            return 0

    @classmethod
    def _log_sync(cls, db: Session, source: DataSource, code: str, status: str, count: int, duration_ms: int, err: str = None):
        """Record sync log and update source metadata."""
        log = ApiSyncLog(
            source_id=source.id if source else None,
            source_code=code,
            status=status,
            records_fetched=count,
            duration_ms=duration_ms,
            error_message=err
        )
        db.add(log)
        if source:
            source.last_sync_timestamp = datetime.datetime.utcnow()
            source.status = "HEALTHY" if status == "SUCCESS" else ("DEGRADED" if status == "PARTIAL" else "OFFLINE")
            source.error_details = err
        db.commit()
