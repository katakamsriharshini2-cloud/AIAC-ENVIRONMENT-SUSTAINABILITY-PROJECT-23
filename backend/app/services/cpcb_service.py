import requests
import datetime
from typing import Dict, Any, List, Optional
from app.config import settings

class CPCBService:
    """
    CPCB / data.gov.in Real-Time Air Quality Index API Service.
    Dataset Resource ID: 3b01bcb8-0b14-4abf-b6f2-c1bfd384ba69
    """
    BASE_URL = "https://api.data.gov.in/resource/3b01bcb8-0b14-4abf-b6f2-c1bfd384ba69"

    @classmethod
    def fetch_cpcb_realtime(cls, city: str = "Warangal", state: str = "Telangana") -> List[Dict[str, Any]]:
        """
        Fetch official CPCB real-time AQI measurements from data.gov.in.
        """
        params = {
            "api-key": settings.DATA_GOV_IN_API_KEY,
            "format": "json",
            "limit": 20
        }
        if city:
            params["filters[city]"] = city
        if state:
            params["filters[state]"] = state

        records = []
        try:
            resp = requests.get(cls.BASE_URL, params=params, timeout=12)
            if resp.status_code == 200:
                payload = resp.json()
                for item in payload.get("records", []):
                    # CPCB fields: station, city, state, pollutant_id, pollutant_avg, last_update
                    records.append(item)
        except Exception as e:
            print(f"[CPCBService] Failed to fetch CPCB live API: {e}")
        return records

    @classmethod
    def parse_station_record(cls, raw_records: List[Dict[str, Any]], city: str = "Warangal") -> Optional[Dict[str, Any]]:
        """
        Aggregate multi-pollutant rows from CPCB into a unified air quality record.
        """
        if not raw_records:
            return None

        station_name = raw_records[0].get("station", f"{city} CPCB Station")
        pollutants = {}
        for row in raw_records:
            pid = str(row.get("pollutant_id", "")).upper()
            val = row.get("pollutant_avg")
            try:
                val = float(val) if val not in [None, "NA", ""] else None
            except ValueError:
                val = None

            if "PM2.5" in pid:
                pollutants["pm25"] = val
            elif "PM10" in pid:
                pollutants["pm10"] = val
            elif "NO2" in pid:
                pollutants["no2"] = val
            elif "SO2" in pid:
                pollutants["so2"] = val
            elif "CO" in pid:
                pollutants["co"] = val
            elif "O3" in pid or "OZONE" in pid:
                pollutants["o3"] = val

        return {
            "location_name": station_name,
            "latitude": float(raw_records[0].get("latitude", 17.9689)),
            "longitude": float(raw_records[0].get("longitude", 79.5941)),
            "observation_timestamp": datetime.datetime.utcnow(),
            "pm25": pollutants.get("pm25"),
            "pm10": pollutants.get("pm10"),
            "no2": pollutants.get("no2"),
            "so2": pollutants.get("so2"),
            "co": pollutants.get("co"),
            "o3": pollutants.get("o3"),
            "unit": "µg/m³",
            "data_quality_status": "VERIFIED",
            "data_type": "GOVERNMENT_DATA",
            "source_name": "CPCB / data.gov.in",
            "source_url": "https://www.data.gov.in/catalog/real-time-air-quality-index"
        }
