import requests
import datetime
from typing import Dict, Any, Optional, List
from app.config import settings

class WeatherService:
    """
    Open-Meteo Real-Time & Forecast Weather Service.
    Free, non-commercial open weather API with hourly and daily forecasts.
    """
    BASE_URL = "https://api.open-meteo.com/v1/forecast"

    WEATHER_CODE_MAP = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        71: "Slight snow",
        80: "Slight rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        95: "Thunderstorm",
        96: "Thunderstorm with slight hail",
        99: "Thunderstorm with heavy hail"
    }

    @classmethod
    def fetch_weather(cls, lat: float = 17.9689, lon: float = 79.5941, city: str = "Warangal") -> Optional[Dict[str, Any]]:
        """
        Fetch current weather conditions, hourly and daily forecast from Open-Meteo.
        """
        params = {
            "latitude": lat,
            "longitude": lon,
            "current": [
                "temperature_2m",
                "relative_humidity_2m",
                "apparent_temperature",
                "precipitation",
                "rain",
                "weather_code",
                "surface_pressure",
                "wind_speed_10m",
                "wind_direction_10m",
                "cloud_cover"
            ],
            "hourly": [
                "temperature_2m",
                "relative_humidity_2m",
                "precipitation_probability",
                "wind_speed_10m"
            ],
            "daily": [
                "temperature_2m_max",
                "temperature_2m_min",
                "precipitation_sum",
                "weather_code"
            ],
            "timezone": "auto"
        }

        try:
            resp = requests.get(cls.BASE_URL, params=params, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                current = data.get("current", {})
                code = current.get("weather_code", 0)
                condition = cls.WEATHER_CODE_MAP.get(code, "Clear")

                # Parse current record
                current_record = {
                    "location_name": city,
                    "latitude": lat,
                    "longitude": lon,
                    "observation_timestamp": datetime.datetime.fromisoformat(current.get("time")) if current.get("time") else datetime.datetime.utcnow(),
                    "temperature": current.get("temperature_2m", 28.0),
                    "apparent_temperature": current.get("apparent_temperature", 29.5),
                    "humidity": current.get("relative_humidity_2m", 55.0),
                    "rainfall": current.get("rain", 0.0),
                    "precipitation": current.get("precipitation", 0.0),
                    "wind_speed": current.get("wind_speed_10m", 12.0),
                    "wind_direction": current.get("wind_direction_10m", 180.0),
                    "atmospheric_pressure": current.get("surface_pressure", 1012.0),
                    "cloud_cover": current.get("cloud_cover", 20.0),
                    "weather_condition": condition,
                    "is_forecast": False,
                    "data_quality_status": "VERIFIED",
                    "data_type": "LIVE_API",
                    "source_name": "Open-Meteo",
                    "source_url": "https://open-meteo.com/en/docs"
                }

                # Parse 24-hr hourly forecast
                hourly_raw = data.get("hourly", {})
                times = hourly_raw.get("time", [])[:24]
                temps = hourly_raw.get("temperature_2m", [])[:24]
                humids = hourly_raw.get("relative_humidity_2m", [])[:24]
                precips = hourly_raw.get("precipitation_probability", [])[:24]
                winds = hourly_raw.get("wind_speed_10m", [])[:24]

                hourly_forecast = []
                for i in range(len(times)):
                    hourly_forecast.append({
                        "time": times[i],
                        "temperature": temps[i] if i < len(temps) else None,
                        "humidity": humids[i] if i < len(humids) else None,
                        "precipitation_probability": precips[i] if i < len(precips) else 0,
                        "wind_speed": winds[i] if i < len(winds) else 0
                    })

                # Parse 7-day daily forecast
                daily_raw = data.get("daily", {})
                d_times = daily_raw.get("time", [])[:7]
                t_max = daily_raw.get("temperature_2m_max", [])[:7]
                t_min = daily_raw.get("temperature_2m_min", [])[:7]
                p_sum = daily_raw.get("precipitation_sum", [])[:7]
                w_codes = daily_raw.get("weather_code", [])[:7]

                daily_forecast = []
                for i in range(len(d_times)):
                    wcode = w_codes[i] if i < len(w_codes) else 0
                    daily_forecast.append({
                        "date": d_times[i],
                        "temp_max": t_max[i] if i < len(t_max) else None,
                        "temp_min": t_min[i] if i < len(t_min) else None,
                        "precipitation_sum": p_sum[i] if i < len(p_sum) else 0,
                        "condition": cls.WEATHER_CODE_MAP.get(wcode, "Clear")
                    })

                return {
                    "current": current_record,
                    "hourly": hourly_forecast,
                    "daily": daily_forecast
                }
        except Exception as e:
            print(f"[WeatherService] Open-Meteo API error: {e}")
        return None
