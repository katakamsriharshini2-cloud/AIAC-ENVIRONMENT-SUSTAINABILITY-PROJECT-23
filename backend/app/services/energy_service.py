import io
import csv
import datetime
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.models import EnergyRecord

class EnergyService:
    """
    IoT Smart Meter & Energy Monitoring Service.
    Handles meter readings, renewable generation calculation, CSV imports.
    """

    @staticmethod
    def process_reading(reading_data: Dict[str, Any], db: Session) -> EnergyRecord:
        """Process and persist IoT energy meter reading."""
        ts = reading_data.get("timestamp") or datetime.datetime.utcnow()
        if isinstance(ts, str):
            try:
                ts = datetime.datetime.fromisoformat(ts.replace("Z", "+00:00"))
            except Exception:
                ts = datetime.datetime.utcnow()

        consumption = float(reading_data.get("consumption_kwh", 0.0))
        power = float(reading_data.get("power_kw", 0.0))
        renewable = float(reading_data.get("renewable_generation_kwh", 0.0))

        ren_pct = round((renewable / consumption * 100.0), 1) if consumption > 0 else 0.0
        ren_pct = min(100.0, max(0.0, ren_pct))

        record = EnergyRecord(
            meter_id=reading_data["meter_id"],
            location_name=reading_data.get("location_name", "Substation Meter"),
            latitude=float(reading_data.get("latitude", 17.9689)),
            longitude=float(reading_data.get("longitude", 79.5941)),
            timestamp=ts,
            consumption_kwh=consumption,
            power_kw=power,
            renewable_generation_kwh=renewable,
            renewable_percentage=ren_pct,
            energy_source=reading_data.get("energy_source", "GRID"),
            data_quality_status="VERIFIED",
            data_type="IOT_SENSOR",
            source_name=reading_data.get("source_name", "Smart Digital Meter")
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        return record

    @staticmethod
    def parse_csv_records(csv_content: str, db: Session) -> List[EnergyRecord]:
        """Parse uploaded CSV data of energy readings."""
        reader = csv.DictReader(io.StringIO(csv_content))
        created_records = []
        for row in reader:
            record_dict = {
                "meter_id": row.get("meter_id", "MTR-CSV"),
                "location_name": row.get("location_name", "Smart Grid Node"),
                "latitude": float(row.get("latitude", 17.9689)),
                "longitude": float(row.get("longitude", 79.5941)),
                "consumption_kwh": float(row.get("consumption_kwh", 120.0)),
                "power_kw": float(row.get("power_kw", 25.0)),
                "renewable_generation_kwh": float(row.get("renewable_generation_kwh", 35.0)),
                "energy_source": row.get("energy_source", "HYBRID"),
                "source_name": "Grid Utility CSV Import"
            }
            rec = EnergyService.process_reading(record_dict, db)
            created_records.append(rec)
        return created_records
