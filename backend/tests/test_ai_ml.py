import pytest
from app.services.ai_service import AIService

def test_predict_aqi(db_session):
    res = AIService.forecast_metric(db=db_session, target_metric="AQI", horizon_hours=12, location="Warangal")
    assert "predictions" in res
    assert len(res["predictions"]) == 12
    assert "mae" in res
    assert "rmse" in res
    assert "r2" in res
    assert res["historical_points_used"] >= 5

def test_predict_temperature(db_session):
    res = AIService.forecast_metric(db=db_session, target_metric="TEMPERATURE", horizon_hours=6, location="Warangal")
    assert "predictions" in res
    assert len(res["predictions"]) == 6
    assert res["model_name"].startswith("Ridge")

def test_predict_energy(db_session):
    # Tests insufficient data fallback handling
    res = AIService.forecast_metric(db=db_session, target_metric="ENERGY_KWH", horizon_hours=6, location="Warangal")
    assert "predictions" in res or res.get("error") == "INSUFFICIENT_HISTORICAL_DATA"

def test_ai_insights(db_session):
    insights = AIService.generate_recommendations(db=db_session)
    assert isinstance(insights, list)
    assert len(insights) > 0
    categories = [i["category"] for i in insights]
    assert "AIR_QUALITY" in categories or "WATER_CONSERVATION" in categories
    assert "action" in insights[0]

def test_anomaly_detection_aqi(db_session):
    data = AIService.detect_anomalies(db=db_session, metric="AQI", threshold_sigma=2.0)
    assert "anomalies" in data
    assert "total_evaluated" in data
    assert data["metric"] == "AQI"
