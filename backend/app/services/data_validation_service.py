import math
from typing import Dict, Any, Optional, Tuple
from datetime import datetime

class DataValidationService:
    """
    Standardization, range-checking, duplicate detection, and index calculations
    (CPCB NAQI and WQI formulas).
    """

    @staticmethod
    def calculate_cpcb_aqi(pm25: Optional[float] = None, pm10: Optional[float] = None,
                           no2: Optional[float] = None, so2: Optional[float] = None,
                           co: Optional[float] = None, o3: Optional[float] = None) -> Tuple[Optional[float], Optional[str], Optional[str]]:
        """
        CPCB Indian National Air Quality Index (NAQI) sub-index calculation.
        Returns: (aqi_value, category, dominant_pollutant)
        """
        sub_indices = {}

        # PM2.5 (µg/m3, 24-hr)
        if pm25 is not None and pm25 >= 0:
            if pm25 <= 30:
                sub_indices['PM2.5'] = pm25 * 50 / 30
            elif pm25 <= 60:
                sub_indices['PM2.5'] = 50 + (pm25 - 30) * 50 / 30
            elif pm25 <= 90:
                sub_indices['PM2.5'] = 100 + (pm25 - 60) * 100 / 30
            elif pm25 <= 120:
                sub_indices['PM2.5'] = 200 + (pm25 - 90) * 100 / 30
            elif pm25 <= 250:
                sub_indices['PM2.5'] = 300 + (pm25 - 120) * 100 / 130
            else:
                sub_indices['PM2.5'] = 400 + (pm25 - 250) * 100 / 130

        # PM10 (µg/m3, 24-hr)
        if pm10 is not None and pm10 >= 0:
            if pm10 <= 50:
                sub_indices['PM10'] = pm10
            elif pm10 <= 100:
                sub_indices['PM10'] = pm10
            elif pm10 <= 250:
                sub_indices['PM10'] = 100 + (pm10 - 100) * 100 / 150
            elif pm10 <= 350:
                sub_indices['PM10'] = 200 + (pm10 - 250)
            elif pm10 <= 430:
                sub_indices['PM10'] = 300 + (pm10 - 350) * 100 / 80
            else:
                sub_indices['PM10'] = 400 + (pm10 - 430) * 100 / 80

        # NO2 (µg/m3, 24-hr)
        if no2 is not None and no2 >= 0:
            if no2 <= 40:
                sub_indices['NO2'] = no2 * 50 / 40
            elif no2 <= 80:
                sub_indices['NO2'] = 50 + (no2 - 40) * 50 / 40
            elif no2 <= 180:
                sub_indices['NO2'] = 100 + (no2 - 80) * 100 / 100
            elif no2 <= 280:
                sub_indices['NO2'] = 200 + (no2 - 180) * 100 / 100
            elif no2 <= 400:
                sub_indices['NO2'] = 300 + (no2 - 280) * 100 / 120
            else:
                sub_indices['NO2'] = 400 + (no2 - 400) * 100 / 120

        # SO2 (µg/m3, 24-hr)
        if so2 is not None and so2 >= 0:
            if so2 <= 40:
                sub_indices['SO2'] = so2 * 50 / 40
            elif so2 <= 80:
                sub_indices['SO2'] = 50 + (so2 - 40) * 50 / 40
            elif so2 <= 380:
                sub_indices['SO2'] = 100 + (so2 - 80) * 100 / 300
            elif so2 <= 800:
                sub_indices['SO2'] = 200 + (so2 - 380) * 100 / 420
            else:
                sub_indices['SO2'] = 300 + (so2 - 800) * 100 / 800

        # CO (mg/m3, 8-hr)
        if co is not None and co >= 0:
            if co <= 1.0:
                sub_indices['CO'] = co * 50 / 1.0
            elif co <= 2.0:
                sub_indices['CO'] = 50 + (co - 1.0) * 50 / 1.0
            elif co <= 10.0:
                sub_indices['CO'] = 100 + (co - 2.0) * 100 / 8.0
            elif co <= 17.0:
                sub_indices['CO'] = 200 + (co - 10.0) * 100 / 7.0
            else:
                sub_indices['CO'] = 300 + (co - 17.0) * 100 / 17.0

        if not sub_indices:
            return None, None, None

        dominant_pollutant = max(sub_indices, key=sub_indices.get)
        aqi_val = round(sub_indices[dominant_pollutant], 1)

        # CPCB Category
        if aqi_val <= 50:
            category = "Good"
        elif aqi_val <= 100:
            category = "Satisfactory"
        elif aqi_val <= 200:
            category = "Moderate"
        elif aqi_val <= 300:
            category = "Poor"
        elif aqi_val <= 400:
            category = "Very Poor"
        else:
            category = "Severe"

        return aqi_val, category, dominant_pollutant

    @staticmethod
    def calculate_wqi(ph: Optional[float], dissolved_oxygen: Optional[float],
                      bod: Optional[float], turbidity: Optional[float],
                      tds: Optional[float]) -> Tuple[Optional[float], Optional[str]]:
        """
        Weighted arithmetic Water Quality Index (WQI).
        Returns: (wqi_score 0-100, status_string)
        Higher score = cleaner water (0 to 100 scale).
        """
        if ph is None or dissolved_oxygen is None:
            return None, None

        # Ideal values: pH=7.0, DO>=6.0 mg/L, BOD<=2.0 mg/L, Turbidity<=5 NTU, TDS<=500 mg/L
        scores = []
        weights = []

        # pH score
        if 6.5 <= ph <= 8.5:
            ph_score = 100 - abs(ph - 7.0) * 20
        else:
            ph_score = max(0, 100 - abs(ph - 7.0) * 35)
        scores.append(ph_score)
        weights.append(0.25)

        # Dissolved Oxygen score (higher is better)
        do_score = min(100, max(0, dissolved_oxygen * 14.0))
        scores.append(do_score)
        weights.append(0.30)

        # BOD (lower is better)
        if bod is not None:
            bod_score = max(0, 100 - (bod * 15.0))
            scores.append(bod_score)
            weights.append(0.20)

        # Turbidity (lower is better)
        if turbidity is not None:
            turb_score = max(0, 100 - (turbidity * 5.0))
            scores.append(turb_score)
            weights.append(0.15)

        # TDS (lower is better)
        if tds is not None:
            tds_score = max(0, 100 - (tds / 10.0))
            scores.append(tds_score)
            weights.append(0.10)

        total_weight = sum(weights)
        wqi = round(sum(s * w for s, w in zip(scores, weights)) / total_weight, 1)

        if wqi >= 85:
            status = "Excellent"
        elif wqi >= 70:
            status = "Good"
        elif wqi >= 50:
            status = "Moderate/Acceptable"
        elif wqi >= 35:
            status = "Poor"
        else:
            status = "Very Poor / Unsuitable"

        return wqi, status

    @staticmethod
    def validate_air_record(data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and clean air quality measurements."""
        cleaned = dict(data)
        # Check non-negative and reasonable bounds
        for key in ['pm25', 'pm10', 'no2', 'so2', 'co', 'o3']:
            val = cleaned.get(key)
            if val is not None:
                if val < 0 or val > 2000:
                    cleaned[key] = None

        if cleaned.get('aqi') is None:
            aqi, cat, dom = DataValidationService.calculate_cpcb_aqi(
                pm25=cleaned.get('pm25'),
                pm10=cleaned.get('pm10'),
                no2=cleaned.get('no2'),
                so2=cleaned.get('so2'),
                co=cleaned.get('co'),
                o3=cleaned.get('o3')
            )
            cleaned['aqi'] = aqi
            cleaned['aqi_category'] = cat
            cleaned['dominant_pollutant'] = dom

        return cleaned

    @staticmethod
    def validate_water_record(data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and clean water quality parameters."""
        cleaned = dict(data)
        if cleaned.get('ph') is not None:
            if cleaned['ph'] < 0 or cleaned['ph'] > 14:
                cleaned['ph'] = None
        if cleaned.get('dissolved_oxygen') is not None and cleaned['dissolved_oxygen'] < 0:
            cleaned['dissolved_oxygen'] = None

        wqi, status = DataValidationService.calculate_wqi(
            ph=cleaned.get('ph'),
            dissolved_oxygen=cleaned.get('dissolved_oxygen'),
            bod=cleaned.get('bod'),
            turbidity=cleaned.get('turbidity'),
            tds=cleaned.get('tds')
        )
        cleaned['water_quality_index'] = wqi
        cleaned['wqi_status'] = status
        return cleaned

    @staticmethod
    def validate_weather_record(data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate temperature, humidity, rainfall ranges."""
        cleaned = dict(data)
        if cleaned.get('humidity') is not None:
            cleaned['humidity'] = min(100.0, max(0.0, cleaned['humidity']))
        if cleaned.get('rainfall') is not None:
            cleaned['rainfall'] = max(0.0, cleaned['rainfall'])
        return cleaned
