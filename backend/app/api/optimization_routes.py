from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any

from app.database import get_db
from app.models import CollectionSchedule
from app.schemas import WasteOptimizationRequest, ResourceAllocationRequest
from app.services.optimization_service import OptimizationService

router = APIRouter(prefix="/api/optimization", tags=["Intelligent Optimization"])

@router.post("/waste")
def optimize_waste_collection(request: WasteOptimizationRequest, db: Session = Depends(get_db)):
    """
    Dijkstra Shortest Path & Priority Queue greedy waste collection route optimization.
    Returns comparison between original and optimized route distance, fuel saved, and CO2 reduction.
    """
    return OptimizationService.optimize_waste_collection_route(
        db=db,
        depot_name=request.depot_location,
        max_vehicle_capacity_kg=request.max_vehicle_capacity_kg
    )

@router.post("/resources")
def allocate_resources(request: ResourceAllocationRequest, db: Session = Depends(get_db)):
    """
    Multi-Criteria Decision Analysis (MCDA) resource prioritization across high-pollution hotspots,
    urgent incidents, and critical aquatic reservoirs.
    """
    return OptimizationService.allocate_resources(
        db=db,
        emergency_teams=request.available_emergency_teams,
        inspectors=request.available_inspectors
    )

@router.get("/results")
def get_past_optimization_schedules(db: Session = Depends(get_db)):
    """Retrieve history of calculated smart collection routes and saved fuel metrics."""
    schedules = db.query(CollectionSchedule).order_by(CollectionSchedule.created_at.desc()).limit(10).all()
    return schedules
