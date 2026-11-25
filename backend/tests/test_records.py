import pytest
from app.api.station_routes import get_stations, create_station
from app.api.record_routes import (
    get_air_quality_records, get_water_quality_records,
    get_weather_records, get_incidents, create_incident, update_incident
)
from app.schemas import StationCreate, IncidentCreate, IncidentUpdate
from app.models import User

def test_get_stations(db_session):
    stations = get_stations(db=db_session)
    assert len(stations) >= 3
    station_names = [s.name for s in stations]
    assert any("Kakatiya" in name for name in station_names)

def test_get_air_quality_records(db_session):
    records = get_air_quality_records(db=db_session)
    assert len(records) > 0
    assert records[0].aqi is not None
    assert records[0].pm25 is not None

def test_get_water_quality_records(db_session):
    records = get_water_quality_records(db=db_session)
    assert len(records) > 0
    assert records[0].water_quality_index is not None
    assert records[0].dissolved_oxygen is not None

def test_get_weather_records(db_session):
    records = get_weather_records(db=db_session)
    assert len(records) > 0
    assert records[0].temperature is not None

def test_incident_lifecycle(db_session):
    admin = db_session.query(User).filter(User.role == "admin").first()
    officer = db_session.query(User).filter(User.role == "environmental_officer").first()

    inc_in = IncidentCreate(
        title="Industrial Stack Emission Exceedance",
        description="Stack opacity breached 40% near Industrial Area Phase 2.",
        incident_type="AIR_POLLUTION",
        severity="HIGH",
        location_name="Kazipet Industrial Estate",
        latitude=17.9700,
        longitude=79.5100
    )
    inc = create_incident(inc_in, db=db_session, current_user=admin)
    assert inc.id is not None
    assert inc.incident_code.startswith("INC-2026-")

    # Update incident
    upd_in = IncidentUpdate(
        status="ACTION_TAKEN",
        assigned_officer_id=officer.id,
        resolution_notes="Officer inspected facility and issued particulate abatement notice."
    )
    updated = update_incident(inc.id, upd_in, db=db_session, current_user=officer)
    assert updated.status == "ACTION_TAKEN"
    assert updated.assigned_officer_id == officer.id
