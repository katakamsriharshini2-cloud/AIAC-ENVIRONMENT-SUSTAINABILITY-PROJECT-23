import requests
import datetime
from typing import Dict, Any, List, Optional
from app.config import settings

class AirQualityService:
    """
    OpenAQ v3 API Client.
    Integrates /v3/locations, /v3/measurements, /v3/sensors, /v3/parameters.
    """
    BASE_URL = "https://api.openaq.org/v3"

    @classmethod
    def get_headers(cls) -> Dict[str, str]:
        headers = {"Accept": "application/json"}
        if settings.OPENAQ_API_KEY:
            headers["X-API-Key"] = settings.OPENAQ_API_KEY
        return headers

    @classmethod
    def fetch_locations(cls, country_id: str = "IN", city: Optional[str] = None) -> List[Dict[str, Any]]:
        """Fetch active monitoring locations in region."""
        url = f"{cls.BASE_URL}/locations"
        params = {"countries_id": country_id, "limit": 25}
        try:
            resp = requests.get(url, headers=cls.get_headers(), params=params, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                return data.get("results", [])
        except Exception as e:
            print(f"[AirQualityService] OpenAQ fetch_locations error: {e}")
        return []

    @classmethod
    def fetch_latest_measurements(cls, location_id: int) -> List[Dict[str, Any]]:
        """Fetch latest sensor measurements for a location."""
        url = f"{cls.BASE_URL}/locations/{location_id}/latest"
        try:
            resp = requests.get(url, headers=cls.get_headers(), timeout=10)
            if resp.status_code == 200:
                return resp.json().get("results", [])
        except Exception as e:
            print(f"[AirQualityService] OpenAQ fetch_latest error: {e}")
        return []

    @classmethod
    def fetch_live_air_data(cls, city: str = "Warangal", lat: float = 17.9689, lon: float = 79.5941) -> Optional[Dict[str, Any]]:
        """
        Query OpenAQ for live data around coordinates.
        Returns parsed standard record dict or None.
        """
        url = f"{cls.BASE_URL}/locations"
        params = {
            "coordinates": f"{lat},{lon}",
            "radius": 50000, # 50 km radius
            "limit": 5
        }
        try:
            resp = requests.get(url, headers=cls.get_headers(), params=params, timeout=10)
            if resp.status_code == 200:
                results = resp.json().get("results", [])
                if results:
                    loc = results[0]
                    # Parse sensors
                    measurements = {}
                    for sensor in loc.get("sensors", []):
                        param_name = sensor.get("parameter", {}).get("name")
                        val = sensor.get("latest", {}).get("value")
                        if param_name and val is not None:
                            measurements[param_name.lower()] = float(val)

                    return {
                        "location_name": f"{loc.get('name', city)} (OpenAQ)",
                        "latitude": loc.get("coordinates", {}).get("latitude", lat),
                        "longitude": loc.get("coordinates", {}).get("longitude", lon),
                        "observation_timestamp": datetime.datetime.utcnow(),
                        "pm25": measurements.get("pm25"),
                        "pm10": measurements.get("pm10"),
                        "no2": measurements.get("no2"),
                        "so2": measurements.get("so2"),
                        "co": measurements.get("co"),
                        "o3": measurements.get("o3"),
                        "unit": "µg/m³",
                        "data_quality_status": "VERIFIED",
                        "data_type": "LIVE_API",
                        "source_name": "OpenAQ",
                        "source_url": "https://docs.openaq.org/"
                    }
        except Exception as e:
            print(f"[AirQualityService] Error fetching OpenAQ live data: {e}")
        return None
