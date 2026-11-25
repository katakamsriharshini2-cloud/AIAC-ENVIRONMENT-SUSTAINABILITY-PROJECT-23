import pytest
from app.services.waste_service import WasteService
from app.services.energy_service import EnergyService
from app.services.water_quality_service import WaterQualityService
from app.api.portal_routes import submit_public_report, track_report
from app.api.live_data_routes import get_api_status
from app.schemas import PublicReportCreate

def test_ingest_waste_iot(db_session):
    reading = {
        "bin_id": "BIN-TEST-99",
        "location_name": "Warangal Market Yard",
        "latitude": 17.9710,
        "longitude": 79.5850,
        "bin_fill_percentage": 94.5,
        "waste_quantity_kg": 189.0,
        "waste_type": "ORGANIC"
    }
    rec = WasteService.process_reading(reading, db=db_session)
    assert rec.bin_id == "BIN-TEST-99"
    assert rec.collection_status == "OVERFLOW"

def test_ingest_energy_iot(db_session):
    reading = {
        "meter_id": "MTR-TEST-88",
        "location_name": "Solar Substation #3",
        "latitude": 17.9800,
        "longitude": 79.5400,
        "consumption_kwh": 350.0,
        "power_kw": 48.0,
        "renewable_generation_kwh": 280.0,
        "energy_source": "SOLAR"
    }
    rec = EnergyService.process_reading(reading, db=db_session)
    assert rec.meter_id == "MTR-TEST-88"
    assert rec.renewable_percentage == 80.0

def test_water_iot_reading():
    reading = {
        "sensor_id": "PROBE-WTR-01",
        "water_body_name": "Bhadrakali Inflow",
        "location_name": "Lake Ghat Probe #1",
        "latitude": 17.9858,
        "longitude": 79.5746,
        "ph": 7.5,
        "dissolved_oxygen": 6.8,
        "turbidity": 4.0,
        "tds": 310.0,
        "water_temperature": 26.0
    }
    validated = WaterQualityService.process_iot_sensor_reading(reading)
    assert validated["water_quality_index"] is not None
    assert validated["wqi_status"] in ["Good", "Excellent"]
    assert validated["data_type"] == "IOT_SENSOR"

def test_api_status_page(db_session):
    status_data = get_api_status(db=db_session)
    assert "providers" in status_data
    assert len(status_data["providers"]) >= 5
    codes = [p["code"] for p in status_data["providers"]]
    assert "OPEN_METEO" in codes
    assert "CPCB_GOV" in codes
    assert "GBIF" in codes

def test_public_report_submission_and_tracking(db_session):
    rep_in = PublicReportCreate(
        reporter_name="Suresh Babu",
        reporter_contact="suresh@example.com",
        category="WASTE",
        title="Overflowing Garbage Container at Waddepally Market",
        description="Bins spilling onto roadway creating environmental nuisance.",
        location_name="Waddepally Vegetable Market",
        latitude=18.0130,
        longitude=79.5450
    )
    rep = submit_public_report(rep_in, db=db_session)
    assert rep.id is not None
    assert rep.report_code.startswith("ECO-REP-2026-")

    tracked = track_report(rep.report_code, db=db_session)
    assert tracked.id == rep.id
    assert tracked.status == "SUBMITTED"
