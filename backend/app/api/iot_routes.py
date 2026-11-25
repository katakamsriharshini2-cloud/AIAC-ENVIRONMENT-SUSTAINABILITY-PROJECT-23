from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import Dict, Any

from app.database import get_db
from app.models import WaterQualityRecord
from app.schemas import IoTReadingsWaste, IoTReadingsEnergy, IoTReadingsWater, WasteResponse, EnergyResponse, WaterQualityResponse
from app.services.waste_service import WasteService
from app.services.energy_service import EnergyService
from app.services.water_quality_service import WaterQualityService

router = APIRouter(prefix="/api/iot", tags=["IoT Ingestion Telemetry"])

@router.post("/waste/readings", response_model=WasteResponse, status_code=status.HTTP_201_CREATED)
def ingest_waste_reading(reading: IoTReadingsWaste, db: Session = Depends(get_db)):
    """Ingest live telemetry from ultrasonic smart waste bin."""
    return WasteService.process_reading(reading.dict(), db)

@router.post("/waste/upload-csv")
async def upload_waste_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Batch ingest municipal waste readings via CSV file."""
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="File must be a valid .csv file")
    content = await file.read()
    records = WasteService.parse_csv_records(content.decode("utf-8"), db)
    return {
        "status": "success",
        "records_imported": len(records),
        "message": f"Successfully ingested {len(records)} waste bin readings from CSV."
    }

@router.post("/energy/readings", response_model=EnergyResponse, status_code=status.HTTP_201_CREATED)
def ingest_energy_reading(reading: IoTReadingsEnergy, db: Session = Depends(get_db)):
    """Ingest live telemetry from digital bi-directional smart meter."""
    return EnergyService.process_reading(reading.dict(), db)

@router.post("/energy/upload-csv")
async def upload_energy_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Batch ingest smart grid meter readings via CSV file."""
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="File must be a valid .csv file")
    content = await file.read()
    records = EnergyService.parse_csv_records(content.decode("utf-8"), db)
    return {
        "status": "success",
        "records_imported": len(records),
        "message": f"Successfully imported {len(records)} smart meter readings from CSV."
    }

@router.post("/water/readings", response_model=WaterQualityResponse, status_code=status.HTTP_201_CREATED)
def ingest_water_reading(reading: IoTReadingsWater, db: Session = Depends(get_db)):
    """Ingest real-time telemetry from submerged IoT multi-probe water sensor."""
    parsed_record = WaterQualityService.process_iot_sensor_reading(reading.dict())
    rec = WaterQualityRecord(**parsed_record)
    db.add(rec)
    db.commit()
    db.refresh(rec)
    return rec
