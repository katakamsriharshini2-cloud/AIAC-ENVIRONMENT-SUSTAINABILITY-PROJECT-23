from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any, List

from app.database import get_db
from app.schemas import PredictRequest, AnomalyDetectRequest
from app.services.ai_service import AIService

router = APIRouter(prefix="/api/ai", tags=["AI & Machine Learning"])

@router.post("/predict")
def predict_environmental_metric(request: PredictRequest, db: Session = Depends(get_db)):
    """
    Run Scikit-learn regression forecast for the chosen environmental target metric.
    Evaluates MAE, RMSE, and R2 against holdout samples.
    """
    result = AIService.forecast_metric(
        db=db,
        target_metric=request.target_metric,
        horizon_hours=request.horizon_hours,
        location=request.location_name or "Warangal"
    )
    if "error" in result and result.get("error") != "INSUFFICIENT_HISTORICAL_DATA":
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.get("/insights")
def get_ai_insights(db: Session = Depends(get_db)):
    """
    Synthesize live telemetry into dynamic, rule- and model-driven environmental recommendations.
    """
    return AIService.generate_recommendations(db=db)

@router.post("/anomaly-detection")
def detect_anomalies(request: AnomalyDetectRequest, db: Session = Depends(get_db)):
    """
    Run IsolationForest and Z-score outlier detection to identify environmental anomalies.
    """
    return AIService.detect_anomalies(
        db=db,
        metric=request.metric,
        threshold_sigma=request.threshold_sigma
    )
