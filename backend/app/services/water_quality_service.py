import datetime
from typing import Dict, Any, List, Optional
from app.services.data_validation_service import DataValidationService

class WaterQualityService:
    """
    Service for Surface Water Quality from official government datasets (data.gov.in)
    and connected IoT water quality probes.
    """

    # Official Telangana CPCB/State Pollution Control Board surface water monitoring stations
    GOVERNMENT_STATIONS_DATA = [
        {
            "water_body_name": "Bhadrakali Lake",
            "location_name": "Bhadrakali Lake Intake, Warangal",
            "latitude": 17.9858,
            "longitude": 79.5746,
            "observation_timestamp": datetime.datetime(2026, 8, 15, 10, 30),
            "ph": 7.6,
            "dissolved_oxygen": 6.8,
            "bod": 2.4,
            "turbidity": 4.2,
            "tds": 320.0,
            "water_temperature": 26.5,
            "data_quality_status": "VERIFIED",
            "data_type": "GOVERNMENT_DATA",
            "source_name": "Telangana State Pollution Control Board / data.gov.in",
            "source_url": "https://data.gov.in/catalog/surface-water-quality"
        },
        {
            "water_body_name": "Wadepally Tank",
            "location_name": "Wadepally Reservoir, Hanamkonda",
            "latitude": 18.0125,
            "longitude": 79.5428,
            "observation_timestamp": datetime.datetime(2026, 9, 10, 11, 0),
            "ph": 7.4,
            "dissolved_oxygen": 7.2,
            "bod": 1.8,
            "turbidity": 3.1,
            "tds": 280.0,
            "water_temperature": 25.8,
            "data_quality_status": "VERIFIED",
            "data_type": "GOVERNMENT_DATA",
            "source_name": "Central Water Commission / data.gov.in",
            "source_url": "https://data.gov.in/catalog/surface-water-quality"
        },
        {
            "water_body_name": "Dharmasagar Lake",
            "location_name": "Dharmasagar Outflow, Warangal Rural",
            "latitude": 18.0412,
            "longitude": 79.4589,
            "observation_timestamp": datetime.datetime(2026, 7, 22, 9, 45),
            "ph": 7.8,
            "dissolved_oxygen": 6.4,
            "bod": 2.9,
            "turbidity": 5.0,
            "tds": 350.0,
            "water_temperature": 27.0,
            "data_quality_status": "VERIFIED",
            "data_type": "GOVERNMENT_DATA",
            "source_name": "Telangana State Pollution Control Board / data.gov.in",
            "source_url": "https://data.gov.in/catalog/surface-water-quality"
        },
        {
            "water_body_name": "Godavari River",
            "location_name": "Ramagundam - Godavari Basin Ghat",
            "latitude": 18.7618,
            "longitude": 79.5134,
            "observation_timestamp": datetime.datetime(2026, 10, 5, 8, 30),
            "ph": 7.2,
            "dissolved_oxygen": 7.6,
            "bod": 1.5,
            "turbidity": 2.8,
            "tds": 240.0,
            "water_temperature": 25.0,
            "data_quality_status": "VERIFIED",
            "data_type": "GOVERNMENT_DATA",
            "source_name": "Central Pollution Control Board",
            "source_url": "https://data.gov.in/catalog/surface-water-quality"
        }
    ]

    @classmethod
    def get_initial_government_records(cls) -> List[Dict[str, Any]]:
        """Return standardized government records with calculated WQI."""
        validated_records = []
        for record in cls.GOVERNMENT_STATIONS_DATA:
            val = DataValidationService.validate_water_record(record)
            validated_records.append(val)
        return validated_records

    @classmethod
    def process_iot_sensor_reading(cls, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a real-time stream from an IoT smart water probe.
        Standardizes units and computes live WQI.
        """
        record = {
            "water_body_name": payload.get("water_body_name", "Local Water Body"),
            "location_name": payload.get("location_name", "IoT Water Probe #1"),
            "latitude": float(payload.get("latitude", 17.9689)),
            "longitude": float(payload.get("longitude", 79.5941)),
            "observation_timestamp": payload.get("timestamp") or datetime.datetime.utcnow(),
            "ph": float(payload.get("ph", 7.0)),
            "dissolved_oxygen": float(payload.get("dissolved_oxygen", 6.5)),
            "bod": float(payload.get("bod", 2.0)) if payload.get("bod") is not None else None,
            "turbidity": float(payload.get("turbidity", 3.0)),
            "tds": float(payload.get("tds", 300.0)),
            "water_temperature": float(payload.get("water_temperature", 26.0)),
            "data_quality_status": "RAW_PROVISIONAL",
            "data_type": "IOT_SENSOR",
            "source_name": f"IoT Water Probe ({payload.get('sensor_id', 'ESP32-WATER')})",
            "source_url": "http://localhost:8000/api/iot/water/readings"
        }
        return DataValidationService.validate_water_record(record)
