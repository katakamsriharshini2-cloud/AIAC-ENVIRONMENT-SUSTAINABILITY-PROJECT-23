from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import datetime

from app.database import get_db
from app.models import (
    AirQualityRecord, WaterQualityRecord, WeatherRecord,
    WasteRecord, EnergyRecord, BiodiversityRecord,
    EnvironmentalIncident, SustainabilityInitiative, User, AuditLog
)
from app.schemas import (
    AirQualityCreate, AirQualityResponse,
    WaterQualityCreate, WaterQualityResponse,
    WeatherCreate, WeatherResponse,
    WasteCreate, WasteResponse,
    EnergyCreate, EnergyResponse,
    BiodiversityCreate, BiodiversityResponse,
    IncidentCreate, IncidentUpdate, IncidentResponse,
    InitiativeCreate, InitiativeUpdate, InitiativeResponse
)
from app.auth import get_current_user, require_admin, require_officer_or_admin
from app.services.data_validation_service import DataValidationService

router = APIRouter(prefix="/api", tags=["Environmental Records CRUD"])

# ----------------- AIR QUALITY CRUD -----------------
@router.get("/air-quality", response_model=List[AirQualityResponse])
def get_air_quality_records(
    location: Optional[str] = None,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    query = db.query(AirQualityRecord)
    if location:
        query = query.filter(AirQualityRecord.location_name.ilike(f"%{location}%"))
    return query.order_by(AirQualityRecord.observation_timestamp.desc()).limit(limit).all()

@router.post("/air-quality", response_model=AirQualityResponse, status_code=status.HTTP_201_CREATED)
def create_air_quality_record(
    record_in: AirQualityCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_officer_or_admin)
):
    validated = DataValidationService.validate_air_record(record_in.dict())
    record = AirQualityRecord(**validated)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


# ----------------- WATER QUALITY CRUD -----------------
@router.get("/water-quality", response_model=List[WaterQualityResponse])
def get_water_quality_records(
    water_body: Optional[str] = None,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    query = db.query(WaterQualityRecord)
    if water_body:
        query = query.filter(WaterQualityRecord.water_body_name.ilike(f"%{water_body}%"))
    return query.order_by(WaterQualityRecord.observation_timestamp.desc()).limit(limit).all()

@router.post("/water-quality", response_model=WaterQualityResponse, status_code=status.HTTP_201_CREATED)
def create_water_quality_record(
    record_in: WaterQualityCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_officer_or_admin)
):
    validated = DataValidationService.validate_water_record(record_in.dict())
    record = WaterQualityRecord(**validated)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


# ----------------- WEATHER CRUD -----------------
@router.get("/weather", response_model=List[WeatherResponse])
def get_weather_records(
    location: Optional[str] = None,
    is_forecast: Optional[bool] = False,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    query = db.query(WeatherRecord)
    if location:
        query = query.filter(WeatherRecord.location_name.ilike(f"%{location}%"))
    if is_forecast is not None:
        query = query.filter(WeatherRecord.is_forecast == is_forecast)
    return query.order_by(WeatherRecord.observation_timestamp.desc()).limit(limit).all()

@router.post("/weather", response_model=WeatherResponse, status_code=status.HTTP_201_CREATED)
def create_weather_record(
    record_in: WeatherCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_officer_or_admin)
):
    validated = DataValidationService.validate_weather_record(record_in.dict())
    record = WeatherRecord(**validated)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


# ----------------- WASTE CRUD -----------------
@router.get("/waste", response_model=List[WasteResponse])
def get_waste_records(
    bin_id: Optional[str] = None,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    query = db.query(WasteRecord)
    if bin_id:
        query = query.filter(WasteRecord.bin_id == bin_id)
    return query.order_by(WasteRecord.timestamp.desc()).limit(limit).all()

@router.post("/waste", response_model=WasteResponse, status_code=status.HTTP_201_CREATED)
def create_waste_record(
    record_in: WasteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_officer_or_admin)
):
    record = WasteRecord(**record_in.dict())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


# ----------------- ENERGY CRUD -----------------
@router.get("/energy", response_model=List[EnergyResponse])
def get_energy_records(
    meter_id: Optional[str] = None,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    query = db.query(EnergyRecord)
    if meter_id:
        query = query.filter(EnergyRecord.meter_id == meter_id)
    return query.order_by(EnergyRecord.timestamp.desc()).limit(limit).all()

@router.post("/energy", response_model=EnergyResponse, status_code=status.HTTP_201_CREATED)
def create_energy_record(
    record_in: EnergyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_officer_or_admin)
):
    record = EnergyRecord(**record_in.dict())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


# ----------------- BIODIVERSITY CRUD -----------------
@router.get("/biodiversity", response_model=List[BiodiversityResponse])
def get_biodiversity_records(
    category: Optional[str] = None,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    query = db.query(BiodiversityRecord)
    if category:
        query = query.filter(BiodiversityRecord.category.ilike(f"%{category}%"))
    return query.order_by(BiodiversityRecord.observation_date.desc()).limit(limit).all()

@router.post("/biodiversity", response_model=BiodiversityResponse, status_code=status.HTTP_201_CREATED)
def create_biodiversity_record(
    record_in: BiodiversityCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_officer_or_admin)
):
    record = BiodiversityRecord(**record_in.dict())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


# ----------------- INCIDENTS CRUD -----------------
@router.get("/incidents", response_model=List[IncidentResponse])
def get_incidents(
    status_filter: Optional[str] = None,
    severity: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(EnvironmentalIncident)
    if status_filter:
        query = query.filter(EnvironmentalIncident.status == status_filter)
    if severity:
        query = query.filter(EnvironmentalIncident.severity == severity)
    return query.order_by(EnvironmentalIncident.created_at.desc()).all()

@router.post("/incidents", response_model=IncidentResponse, status_code=status.HTTP_201_CREATED)
def create_incident(
    incident_in: IncidentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    count = db.query(EnvironmentalIncident).count() + 1
    code = f"INC-2026-{count:03d}"
    incident = EnvironmentalIncident(
        incident_code=code,
        reported_by_user_id=current_user.id,
        status="REPORTED",
        **incident_in.dict()
    )
    db.add(incident)
    db.commit()
    db.refresh(incident)
    return incident

@router.put("/incidents/{id}", response_model=IncidentResponse)
def update_incident(
    id: int,
    incident_in: IncidentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_officer_or_admin)
):
    incident = db.query(EnvironmentalIncident).filter(EnvironmentalIncident.id == id).first()
    if not incident:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incident not found")

    for k, v in incident_in.dict(exclude_unset=True).items():
        setattr(incident, k, v)

    if incident_in.status in ["RESOLVED", "CLOSED"] and not incident.resolved_at:
        incident.resolved_at = datetime.datetime.utcnow()

    db.commit()
    db.refresh(incident)
    return incident


# ----------------- SUSTAINABILITY INITIATIVES CRUD -----------------
@router.get("/initiatives", response_model=List[InitiativeResponse])
def get_initiatives(db: Session = Depends(get_db)):
    return db.query(SustainabilityInitiative).order_by(SustainabilityInitiative.created_at.desc()).all()

@router.post("/initiatives", response_model=InitiativeResponse, status_code=status.HTTP_201_CREATED)
def create_initiative(
    init_in: InitiativeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_officer_or_admin)
):
    initiative = SustainabilityInitiative(**init_in.dict())
    db.add(initiative)
    db.commit()
    db.refresh(initiative)
    return initiative
