from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models import MonitoringStation, User, AuditLog
from app.schemas import StationCreate, StationUpdate, StationResponse
from app.auth import get_current_user, require_admin, require_officer_or_admin

router = APIRouter(prefix="/api/stations", tags=["Monitoring Stations"])

@router.get("", response_model=List[StationResponse])
def get_stations(
    city: Optional[str] = None,
    state: Optional[str] = None,
    station_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """List monitoring stations with optional filters for city, state, or type."""
    query = db.query(MonitoringStation)
    if city:
        query = query.filter(MonitoringStation.city.ilike(f"%{city}%"))
    if state:
        query = query.filter(MonitoringStation.state.ilike(f"%{state}%"))
    if station_type:
        query = query.filter(MonitoringStation.station_type == station_type.upper())
    return query.all()

@router.get("/{id}", response_model=StationResponse)
def get_station(id: int, db: Session = Depends(get_db)):
    """Get single monitoring station details by ID."""
    station = db.query(MonitoringStation).filter(MonitoringStation.id == id).first()
    if not station:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Station not found")
    return station

@router.post("", response_model=StationResponse, status_code=status.HTTP_201_CREATED)
def create_station(
    station_in: StationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_officer_or_admin)
):
    """Create a new environmental monitoring station (Admin / Officer)."""
    existing = db.query(MonitoringStation).filter(MonitoringStation.station_code == station_in.station_code).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Station code already exists.")

    station = MonitoringStation(**station_in.dict())
    db.add(station)
    db.commit()
    db.refresh(station)

    audit = AuditLog(
        user_id=current_user.id,
        action="CREATE_STATION",
        entity="monitoring_stations",
        entity_id=str(station.id),
        details=f"Created station '{station.name}' ({station.station_code})"
    )
    db.add(audit)
    db.commit()

    return station

@router.put("/{id}", response_model=StationResponse)
def update_station(
    id: int,
    station_in: StationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_officer_or_admin)
):
    """Update station metadata or operating status."""
    station = db.query(MonitoringStation).filter(MonitoringStation.id == id).first()
    if not station:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Station not found")

    for key, val in station_in.dict(exclude_unset=True).items():
        setattr(station, key, val)

    db.commit()
    db.refresh(station)

    audit = AuditLog(
        user_id=current_user.id,
        action="UPDATE_STATION",
        entity="monitoring_stations",
        entity_id=str(station.id),
        details=f"Updated station {station.station_code}"
    )
    db.add(audit)
    db.commit()

    return station

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_station(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Delete a station (Admin only)."""
    station = db.query(MonitoringStation).filter(MonitoringStation.id == id).first()
    if not station:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Station not found")

    db.delete(station)
    db.commit()

    audit = AuditLog(
        user_id=current_user.id,
        action="DELETE_STATION",
        entity="monitoring_stations",
        entity_id=str(id),
        details=f"Deleted station {station.station_code}"
    )
    db.add(audit)
    db.commit()
    return None
