from .models import Vehicle, DrivingCycle
from .dynamics import simulate_cycle
from .engine import BSFCModel

def simulate_consumption(vehicle: Vehicle, cycle: DrivingCycle, engine_model: BSFCModel) -> dict:
    """Simula il consumo e restituisce un report."""
    points = simulate_cycle(vehicle, cycle)
    consumption = engine_model.fuel_consumption(points, cycle.distance_km)
    
    return {
        'cycle_name': cycle.name,
        'distance_km': cycle.distance_km,
        'duration_s': cycle.duration_s,
        'consumption_l_100km': consumption,
        'points': points
    }