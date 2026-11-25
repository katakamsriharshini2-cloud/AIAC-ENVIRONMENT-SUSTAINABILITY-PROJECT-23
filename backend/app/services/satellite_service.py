import datetime
from typing import Dict, Any, List

class SatelliteService:
    """
    NASA GIBS (Global Imagery Browse Services) Integration.
    Provides standard WMTS endpoint templates and documented NASA EOSDIS layers.
    Does NOT claim satellite imagery directly measures ground-level AQI or water chemistry.
    """

    GIBS_WMTS_BASE = "https://gibs.earthdata.nasa.gov/wmts/epsg3857/best"

    LAYERS = [
        {
            "id": "MODIS_Terra_CorrectedReflectance_TrueColor",
            "name": "MODIS Terra TrueColor",
            "format": "image/jpeg",
            "matrix_set": "GoogleMapsCompatible_Level9",
            "description": "Natural color imagery useful for monitoring haze, smoke, clouds, and land cover.",
            "category": "Land Cover / Atmosphere",
            "sensor": "MODIS on Terra Satellite",
            "attribution": "NASA EOSDIS GIBS",
            "tile_url_template": f"{GIBS_WMTS_BASE}/MODIS_Terra_CorrectedReflectance_TrueColor/default/{{time}}/GoogleMapsCompatible_Level9/{{z}}/{{y}}/{{x}}.jpg"
        },
        {
            "id": "VIIRS_SNPP_CorrectedReflectance_TrueColor",
            "name": "VIIRS TrueColor (High Resolution)",
            "format": "image/jpeg",
            "matrix_set": "GoogleMapsCompatible_Level9",
            "description": "High-resolution daily imagery for surface observations and atmospheric haze.",
            "category": "Land Cover / Cloud Observation",
            "sensor": "VIIRS on Suomi NPP",
            "attribution": "NASA EOSDIS GIBS",
            "tile_url_template": f"{GIBS_WMTS_BASE}/VIIRS_SNPP_CorrectedReflectance_TrueColor/default/{{time}}/GoogleMapsCompatible_Level9/{{z}}/{{y}}/{{x}}.jpg"
        },
        {
            "id": "MODIS_Terra_NDVI_16Day",
            "name": "MODIS Normalized Difference Vegetation Index (NDVI)",
            "format": "image/png",
            "matrix_set": "GoogleMapsCompatible_Level8",
            "description": "Vegetation greenness and canopy density index for agricultural and forest health monitoring.",
            "category": "Vegetation Monitoring",
            "sensor": "MODIS Terra 16-Day",
            "attribution": "NASA EOSDIS GIBS",
            "tile_url_template": f"{GIBS_WMTS_BASE}/MODIS_Terra_NDVI_16Day/default/{{time}}/GoogleMapsCompatible_Level8/{{z}}/{{y}}/{{x}}.png"
        },
        {
            "id": "MODIS_Terra_Thermal_Anomalies_All",
            "name": "MODIS Thermal Anomalies / Active Fires",
            "format": "image/png",
            "matrix_set": "GoogleMapsCompatible_Level8",
            "description": "Active thermal hotspots and agricultural burning detections.",
            "category": "Wildfire / Thermal Anomalies",
            "sensor": "MODIS Terra Thermal",
            "attribution": "NASA EOSDIS GIBS",
            "tile_url_template": f"{GIBS_WMTS_BASE}/MODIS_Terra_Thermal_Anomalies_All/default/{{time}}/GoogleMapsCompatible_Level8/{{z}}/{{y}}/{{x}}.png"
        }
    ]

    @classmethod
    def get_available_layers(cls, date_str: str = None) -> Dict[str, Any]:
        """
        Return available satellite layers with resolved tile URLs for the selected date.
        """
        if not date_str:
            # GIBS products usually available up to yesterday
            target_date = (datetime.datetime.utcnow() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        else:
            target_date = date_str

        resolved_layers = []
        for l in cls.LAYERS:
            layer_copy = dict(l)
            layer_copy["current_date"] = target_date
            layer_copy["tile_url"] = l["tile_url_template"].replace("{time}", target_date)
            resolved_layers.append(layer_copy)

        return {
            "acquisition_date": target_date,
            "provider": "NASA EOSDIS GIBS",
            "documentation_url": "https://nasa-gibs.github.io/gibs-api-docs/",
            "layers": resolved_layers,
            "scientific_disclaimer": "NASA satellite imagery provides optical reflectance and thermal radiances; it does not replace in-situ ground air quality (AQI) or water chemical sensors."
        }
