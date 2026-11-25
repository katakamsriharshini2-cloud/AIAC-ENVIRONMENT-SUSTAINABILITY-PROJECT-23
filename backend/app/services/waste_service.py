import io
import csv
import datetime
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.models import WasteRecord

class WasteService:
    """
    IoT Waste Management Service.
    Handles sensor readings, CSV uploads, bin status calculations.
    """

    @staticmethod
    def process_reading(reading_data: Dict[str, Any], db: Session) -> WasteRecord:
        """Process and persist single IoT waste reading."""
        ts = reading_data.get("timestamp") or datetime.datetime.utcnow()
        if isinstance(ts, str):
            try:
                ts = datetime.datetime.fromisoformat(ts.replace("Z", "+00:00"))
            except Exception:
                ts = datetime.datetime.utcnow()

        fill_pct = float(reading_data.get("bin_fill_percentage", 0.0))
        status = "PENDING"
        if fill_pct >= 90.0:
            status = "OVERFLOW"
        elif fill_pct >= 75.0:
            status = "SCHEDULED"

        record = WasteRecord(
            bin_id=reading_data["bin_id"],
            location_name=reading_data.get("location_name", "Municipal Bin"),
            latitude=float(reading_data.get("latitude", 17.9689)),
            longitude=float(reading_data.get("longitude", 79.5941)),
            timestamp=ts,
            bin_fill_percentage=fill_pct,
            waste_quantity_kg=float(reading_data.get("waste_quantity_kg", fill_pct * 0.8)),
            waste_type=reading_data.get("waste_type", "GENERAL"),
            collection_status=status,
            recycling_status=reading_data.get("recycling_status", "NOT_RECYCLED"),
            data_quality_status="VERIFIED",
            data_type="IOT_SENSOR",
            source_name=reading_data.get("source_name", "Smart Ultrasonic Bin Sensor")
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        return record

    @staticmethod
    def parse_csv_records(csv_content: str, db: Session) -> List[WasteRecord]:
        """Parse uploaded CSV data of waste readings."""
        reader = csv.DictReader(io.StringIO(csv_content))
        created_records = []
        for row in reader:
            record_dict = {
                "bin_id": row.get("bin_id", "BIN-CSV"),
                "location_name": row.get("location_name", "Warangal Central"),
                "latitude": float(row.get("latitude", 17.9689)),
                "longitude": float(row.get("longitude", 79.5941)),
                "bin_fill_percentage": float(row.get("bin_fill_percentage", 50.0)),
                "waste_quantity_kg": float(row.get("waste_quantity_kg", 40.0)),
                "waste_type": row.get("waste_type", "GENERAL"),
                "source_name": "Municipal CSV Upload"
            }
            rec = WasteService.process_reading(record_dict, db)
            created_records.append(rec)
        return created_records
