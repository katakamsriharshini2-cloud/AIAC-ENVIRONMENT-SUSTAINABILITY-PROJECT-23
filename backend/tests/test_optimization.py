import pytest
from app.services.optimization_service import OptimizationService

def test_haversine_distance():
    # Warangal to Hanamkonda (~5 km)
    dist = OptimizationService.haversine_distance(17.9784, 79.5941, 18.0120, 79.5580)
    assert 4.0 <= dist <= 6.5

def test_waste_route_optimization(db_session):
    data = OptimizationService.optimize_waste_collection_route(
        db=db_session,
        depot_name="Warangal Central Sanitation Depot",
        max_vehicle_capacity_kg=4000.0
    )
    assert "original_distance_km" in data
    assert "optimized_distance_km" in data
    assert "fuel_saved_liters" in data
    assert "co2_reduction_kg" in data
    assert "stops_in_order" in data
    assert len(data["stops_in_order"]) > 0
    assert data["bins_visited_count"] == len(data["stops_in_order"])
    assert data["optimized_distance_km"] <= data["original_distance_km"]

def test_resource_allocation(db_session):
    data = OptimizationService.allocate_resources(
        db=db_session,
        emergency_teams=3,
        inspectors=3
    )
    assert "allocations" in data
    assert "total_allocations" in data
    if data["total_allocations"] > 0:
        first_alloc = data["allocations"][0]
        assert "priority_score" in first_alloc
        assert "assigned_unit" in first_alloc
        assert "target_location" in first_alloc
