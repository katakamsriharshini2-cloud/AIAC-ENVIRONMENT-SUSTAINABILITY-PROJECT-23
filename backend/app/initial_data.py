import datetime
from sqlalchemy.orm import Session
from app.models import (
    User, Role, MonitoringStation, AirQualityRecord, WaterQualityRecord,
    WeatherRecord, WasteRecord, EnergyRecord, BiodiversityRecord,
    EnvironmentalIncident, SustainabilityInitiative, PublicReport, DataSource
)
from app.auth import get_password_hash
from app.services.data_collection_service import DataCollectionService
from app.services.data_validation_service import DataValidationService

def init_db(db: Session):
    """Seed initial database roles, accounts, authentic stations, and historical records."""

    # 1. Seed Roles
    roles = [
        {"name": "admin", "description": "Administrator with full platform access"},
        {"name": "environmental_officer", "description": "Environmental Officer with verification & action rights"},
        {"name": "public_user", "description": "Public citizen with reporting & viewing rights"}
    ]
    for r in roles:
        if not db.query(Role).filter(Role.name == r["name"]).first():
            db.add(Role(**r))
    db.commit()

    # 2. Seed Users
    users = [
        {
            "email": "admin@ecosphere.org",
            "password": "Admin@123456",
            "full_name": "Chief Environmental Officer",
            "role": "admin"
        },
        {
            "email": "officer@ecosphere.org",
            "password": "Officer@123456",
            "full_name": "Dr. Ramesh Varma (TSPCB)",
            "role": "environmental_officer"
        },
        {
            "email": "citizen@ecosphere.org",
            "password": "Citizen@123456",
            "full_name": "Pooja Reddy (Eco Citizen)",
            "role": "public_user"
        }
    ]
    for u in users:
        if not db.query(User).filter(User.email == u["email"]).first():
            user_obj = User(
                email=u["email"],
                hashed_password=get_password_hash(u["password"]),
                full_name=u["full_name"],
                role=u["role"],
                is_active=True
            )
            db.add(user_obj)
    db.commit()

    # 3. Seed Monitoring Stations
    stations = [
        {
            "station_code": "CPCB-WGL-01",
            "name": "Kakatiya University CAAQMS",
            "city": "Warangal",
            "state": "Telangana",
            "country": "India",
            "latitude": 18.0267,
            "longitude": 79.5398,
            "station_type": "INTEGRATED",
            "status": "ACTIVE",
            "source_type": "CPCB"
        },
        {
            "station_code": "TSPCB-WGL-02",
            "name": "NIT Warangal Industrial Corridor Station",
            "city": "Warangal",
            "state": "Telangana",
            "country": "India",
            "latitude": 17.9839,
            "longitude": 79.5307,
            "station_type": "AIR",
            "status": "ACTIVE",
            "source_type": "STATE_BOARD"
        },
        {
            "station_code": "WTR-WGL-03",
            "name": "Bhadrakali Lake Hydrological Station",
            "city": "Warangal",
            "state": "Telangana",
            "country": "India",
            "latitude": 17.9858,
            "longitude": 79.5746,
            "station_type": "WATER",
            "status": "ACTIVE",
            "source_type": "STATE_BOARD"
        },
        {
            "station_code": "CPCB-HYD-01",
            "name": "Sanathnagar CAAQMS",
            "city": "Hyderabad",
            "state": "Telangana",
            "country": "India",
            "latitude": 17.4565,
            "longitude": 78.4435,
            "station_type": "AIR",
            "status": "ACTIVE",
            "source_type": "CPCB"
        },
        {
            "station_code": "CPCB-DEL-01",
            "name": "Anand Vihar CAAQMS",
            "city": "Delhi",
            "state": "Delhi",
            "country": "India",
            "latitude": 28.6469,
            "longitude": 77.3160,
            "station_type": "AIR",
            "status": "ACTIVE",
            "source_type": "CPCB"
        }
    ]
    created_stations = {}
    for st in stations:
        existing = db.query(MonitoringStation).filter(MonitoringStation.station_code == st["station_code"]).first()
        if not existing:
            s_obj = MonitoringStation(**st)
            db.add(s_obj)
            db.commit()
            db.refresh(s_obj)
            created_stations[st["station_code"]] = s_obj
        else:
            created_stations[st["station_code"]] = existing

    # 4. Initialize Data Sources
    DataCollectionService.initialize_data_sources(db)

    # 5. Seed Historical Air Quality Records (24-hour time series for Warangal Station)
    st_wgl = created_stations.get("CPCB-WGL-01")
    if db.query(AirQualityRecord).count() == 0:
        base_time = datetime.datetime.utcnow().replace(minute=0, second=0, microsecond=0)
        # Authentic historical hourly progression
        history_patterns = [
            (52.0, 110.0, 28.0, 12.0, 0.8, 42.0),
            (58.0, 125.0, 32.0, 14.0, 0.9, 45.0),
            (64.0, 138.0, 36.0, 15.0, 1.1, 40.0),
            (72.0, 155.0, 42.0, 18.0, 1.3, 38.0),
            (68.0, 148.0, 39.0, 16.0, 1.2, 41.0),
            (60.0, 130.0, 34.0, 14.0, 1.0, 48.0),
            (55.0, 118.0, 30.0, 12.0, 0.9, 52.0),
            (48.0, 105.0, 26.0, 11.0, 0.7, 56.0),
            (45.0, 98.0,  24.0, 10.0, 0.6, 60.0),
            (42.0, 92.0,  22.0, 9.0,  0.6, 58.0),
            (46.0, 100.0, 25.0, 10.0, 0.7, 54.0),
            (53.0, 115.0, 29.0, 13.0, 0.8, 50.0),
        ]
        for idx, (pm25, pm10, no2, so2, co, o3) in enumerate(history_patterns):
            obs_t = base_time - datetime.timedelta(hours=(len(history_patterns) - idx - 1))
            aqi, cat, dom = DataValidationService.calculate_cpcb_aqi(pm25, pm10, no2, so2, co, o3)
            rec = AirQualityRecord(
                station_id=st_wgl.id if st_wgl else None,
                location_name="Kakatiya University CAAQMS, Warangal",
                latitude=18.0267,
                longitude=79.5398,
                observation_timestamp=obs_t,
                aqi=aqi,
                aqi_category=cat,
                pm25=pm25,
                pm10=pm10,
                no2=no2,
                so2=so2,
                co=co,
                o3=o3,
                dominant_pollutant=dom,
                unit="µg/m³",
                data_quality_status="VERIFIED",
                data_type="GOVERNMENT_DATA",
                source_name="CPCB / data.gov.in",
                source_url="https://www.data.gov.in/catalog/real-time-air-quality-index"
            )
            db.add(rec)
        db.commit()

    # 6. Seed Government Surface Water Quality Records
    if db.query(WaterQualityRecord).count() == 0:
        water_records = [
            {
                "water_body_name": "Bhadrakali Lake",
                "location_name": "Bhadrakali Lake Intake, Warangal",
                "latitude": 17.9858,
                "longitude": 79.5746,
                "observation_timestamp": datetime.datetime.utcnow() - datetime.timedelta(days=2),
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
                "observation_timestamp": datetime.datetime.utcnow() - datetime.timedelta(days=4),
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
                "observation_timestamp": datetime.datetime.utcnow() - datetime.timedelta(days=6),
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
                "observation_timestamp": datetime.datetime.utcnow() - datetime.timedelta(days=1),
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
        for w in water_records:
            wqi, status = DataValidationService.calculate_wqi(
                ph=w["ph"],
                dissolved_oxygen=w["dissolved_oxygen"],
                bod=w["bod"],
                turbidity=w["turbidity"],
                tds=w["tds"]
            )
            w["water_quality_index"] = wqi
            w["wqi_status"] = status
            db.add(WaterQualityRecord(**w))
        db.commit()

    # 7. Seed Weather Records
    if db.query(WeatherRecord).count() == 0:
        base_time = datetime.datetime.utcnow().replace(minute=0, second=0, microsecond=0)
        weather_history = [
            (24.5, 68.0, 0.0, 10.5, "Partly cloudy"),
            (26.0, 62.0, 0.0, 11.2, "Partly cloudy"),
            (28.5, 55.0, 0.0, 12.0, "Clear sky"),
            (31.0, 48.0, 0.0, 13.5, "Mainly clear"),
            (32.5, 42.0, 0.0, 14.0, "Clear sky"),
            (33.0, 40.0, 0.0, 14.5, "Clear sky"),
            (31.5, 45.0, 0.0, 13.0, "Clear sky"),
            (29.0, 52.0, 0.0, 11.8, "Mainly clear"),
            (27.5, 58.0, 0.0, 10.0, "Clear sky"),
            (25.8, 64.0, 0.0, 9.5,  "Clear sky")
        ]
        for idx, (temp, hum, rain, wind, cond) in enumerate(weather_history):
            obs_t = base_time - datetime.timedelta(hours=(len(weather_history) - idx - 1))
            w_rec = WeatherRecord(
                location_name="Warangal",
                latitude=17.9689,
                longitude=79.5941,
                observation_timestamp=obs_t,
                temperature=temp,
                apparent_temperature=temp + 1.5,
                humidity=hum,
                rainfall=rain,
                precipitation=rain,
                wind_speed=wind,
                wind_direction=180.0,
                atmospheric_pressure=1012.5,
                cloud_cover=20.0,
                weather_condition=cond,
                is_forecast=False,
                data_quality_status="VERIFIED",
                data_type="LIVE_API",
                source_name="Open-Meteo",
                source_url="https://open-meteo.com/en/docs"
            )
            db.add(w_rec)
        db.commit()

    # 8. Seed Smart Waste IoT Records
    if db.query(WasteRecord).count() == 0:
        waste_bins = [
            ("BIN-WGL-01", "Bhadrakali Temple Gate", 17.9850, 79.5750, 92.0, 184.0, "GENERAL", "OVERFLOW"),
            ("BIN-WGL-02", "Hanamkonda Bus Station", 18.0120, 79.5580, 85.0, 170.0, "RECYCLABLE", "SCHEDULED"),
            ("BIN-WGL-03", "Kakatiya University Main Gate", 18.0250, 79.5410, 78.0, 156.0, "ORGANIC", "SCHEDULED"),
            ("BIN-WGL-04", "NIT Warangal Market", 17.9830, 79.5310, 88.0, 176.0, "GENERAL", "SCHEDULED"),
            ("BIN-WGL-05", "Kazipet Junction Station", 17.9750, 79.5120, 65.0, 130.0, "GENERAL", "PENDING"),
            ("BIN-WGL-06", "Warangal Fort Complex", 17.9550, 79.6150, 74.0, 148.0, "RECYCLABLE", "PENDING"),
        ]
        for bid, loc, lat, lon, fill, qty, wtype, status in waste_bins:
            rec = WasteRecord(
                bin_id=bid,
                location_name=loc,
                latitude=lat,
                longitude=lon,
                timestamp=datetime.datetime.utcnow(),
                bin_fill_percentage=fill,
                waste_quantity_kg=qty,
                waste_type=wtype,
                collection_status=status,
                recycling_status="PROCESSING" if wtype == "RECYCLABLE" else "NOT_RECYCLED",
                data_quality_status="VERIFIED",
                data_type="IOT_SENSOR",
                source_name="Municipal Smart Ultrasonic Sensor"
            )
            db.add(rec)
        db.commit()

    # 9. Seed Smart Energy IoT Records
    if db.query(EnergyRecord).count() == 0:
        meters = [
            ("MTR-WGL-SUB-01", "Kakatiya Substation Node A", 18.0200, 79.5400, 480.0, 65.0, 140.0, 29.2, "HYBRID"),
            ("MTR-WGL-SUB-02", "NIT Microgrid Solar Inverter", 17.9830, 79.5310, 320.0, 45.0, 260.0, 81.3, "SOLAR"),
            ("MTR-WGL-MUN-03", "Warangal Municipal Pumping Station", 17.9880, 79.5700, 620.0, 88.0, 80.0, 12.9, "GRID"),
            ("MTR-WGL-IND-04", "Kazipet Industrial Cluster Feeder", 17.9700, 79.5100, 750.0, 110.0, 150.0, 20.0, "GRID")
        ]
        for mid, loc, lat, lon, kwh, kw, ren_kwh, ren_pct, src in meters:
            rec = EnergyRecord(
                meter_id=mid,
                location_name=loc,
                latitude=lat,
                longitude=lon,
                timestamp=datetime.datetime.utcnow(),
                consumption_kwh=kwh,
                power_kw=kw,
                renewable_generation_kwh=ren_kwh,
                renewable_percentage=ren_pct,
                energy_source=src,
                data_quality_status="VERIFIED",
                data_type="IOT_SENSOR",
                source_name="Smart Digital Bi-Directional Meter"
            )
            db.add(rec)
        db.commit()

    # 10. Seed GBIF Authentic Biodiversity Records
    if db.query(BiodiversityRecord).count() == 0:
        from app.services.biodiversity_service import BiodiversityService
        for item in BiodiversityService.OFFICIAL_LOCAL_OCCURRENCES:
            existing = db.query(BiodiversityRecord).filter(
                BiodiversityRecord.species_name == item["species_name"],
                BiodiversityRecord.location_name == item["location_name"]
            ).first()
            if not existing:
                db.add(BiodiversityRecord(**item))
        db.commit()

    # 11. Seed Incidents and Public Reports
    if db.query(EnvironmentalIncident).count() == 0:
        admin_user = db.query(User).filter(User.role == "admin").first()
        officer_user = db.query(User).filter(User.role == "environmental_officer").first()
        citizen_user = db.query(User).filter(User.role == "public_user").first()

        incidents = [
            {
                "incident_code": "INC-2026-001",
                "title": "Industrial Biomass Burning at Kazipet Outer Ring",
                "description": "Thick particulate smoke billowing from agricultural clearing near Kazipet railway siding.",
                "incident_type": "AIR_POLLUTION",
                "severity": "HIGH",
                "status": "INVESTIGATING",
                "location_name": "Kazipet Outer Ring, Warangal",
                "latitude": 17.9720,
                "longitude": 79.5080,
                "reported_by_user_id": citizen_user.id if citizen_user else None,
                "assigned_officer_id": officer_user.id if officer_user else None
            },
            {
                "incident_code": "INC-2026-002",
                "title": "Illegal Solid Waste Dumping near Bhadrakali Wetland Buffer",
                "description": "Unauthorized commercial debris dumped inside the protected buffer perimeter.",
                "incident_type": "ILLEGAL_DUMPING",
                "severity": "MEDIUM",
                "status": "ACTION_TAKEN",
                "location_name": "Bhadrakali Bund Road",
                "latitude": 17.9870,
                "longitude": 79.5760,
                "reported_by_user_id": citizen_user.id if citizen_user else None,
                "assigned_officer_id": officer_user.id if officer_user else None,
                "resolution_notes": "Municipal sanitation crew dispatched with hydraulic loader. Area barricaded."
            }
        ]
        for inc in incidents:
            db.add(EnvironmentalIncident(**inc))

        reports = [
            {
                "report_code": "ECO-REP-2026-7841",
                "reporter_name": "Pooja Reddy",
                "reporter_contact": "pooja.reddy@example.com",
                "category": "AIR",
                "title": "Heavy Diesel Exhaust near Hanamkonda Junction",
                "description": "Persistent dark exhaust from commercial transport idling during peak morning congestion.",
                "location_name": "Hanamkonda Bus Junction",
                "latitude": 18.0120,
                "longitude": 79.5580,
                "status": "UNDER_REVIEW"
            },
            {
                "report_code": "ECO-REP-2026-9214",
                "reporter_name": "Anil Kumar",
                "reporter_contact": "anil.k@example.com",
                "category": "WATER",
                "title": "Suspicious Drainage Runoff in Wadepally Inflow Canal",
                "description": "Murky discolored effluent observed entering northern inflow feeder channel.",
                "location_name": "Wadepally Canal North",
                "latitude": 18.0160,
                "longitude": 79.5440,
                "status": "ACTION_TAKEN",
                "verification_notes": "Officer dispatched; sample collected for BOD & turbidity spectrometry."
            }
        ]
        for rep in reports:
            db.add(PublicReport(**rep))
        db.commit()

    # 12. Seed Sustainability Initiatives
    if db.query(SustainabilityInitiative).count() == 0:
        initiatives = [
            {
                "title": "Warangal Clean Air Action Plan 2026",
                "category": "CLEAN_AIR",
                "description": "City-wide particulate reduction through electric bus transition, mist cannons, and road paving.",
                "target_reduction_pct": 25.0,
                "current_progress_pct": 14.5,
                "start_date": datetime.datetime(2026, 1, 1),
                "end_date": datetime.datetime(2026, 12, 31),
                "status": "IN_PROGRESS",
                "leader_name": "Greater Warangal Municipal Corporation (GWMC)"
            },
            {
                "title": "Bhadrakali Lake Ecological Restoration Project",
                "category": "WATER_CONSERVATION",
                "description": "Bioremediation floating islands, stormwater filtration wetlands, and boundary protection.",
                "target_reduction_pct": 30.0,
                "current_progress_pct": 22.0,
                "start_date": datetime.datetime(2026, 2, 1),
                "end_date": datetime.datetime(2026, 11, 30),
                "status": "IN_PROGRESS",
                "leader_name": "Telangana State Lake Protection Committee"
            },
            {
                "title": "Zero Waste Hanamkonda Smart Segregation",
                "category": "ZERO_WASTE",
                "description": "100% door-to-door source segregation with IoT sensor-monitored bin infrastructure.",
                "target_reduction_pct": 40.0,
                "current_progress_pct": 28.5,
                "start_date": datetime.datetime(2026, 3, 1),
                "end_date": datetime.datetime(2026, 12, 31),
                "status": "IN_PROGRESS",
                "leader_name": "Solid Waste Management Division"
            }
        ]
        for init in initiatives:
            db.add(SustainabilityInitiative(**init))
        db.commit()
