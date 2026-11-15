from scipy.optimize import minimize
from .models import Vehicle, DrivingCycle
from .engine import ConstantBSFC
from .simulator import simulate_consumption

def calibrate_bsfc(vehicle: Vehicle, cycle: DrivingCycle, target_consumption: float) -> ConstantBSFC:
    """Trova il BSFC costante che matcha il consumo target."""
    
    def objective(bsfc_value):
        model = ConstantBSFC(bsfc_value[0])
        result = simulate_consumption(vehicle, cycle, model)
        return (result['consumption_l_100km'] - target_consumption) ** 2
    
    result = minimize(objective, [220.0], bounds=[(150.0, 350.0)])
    return ConstantBSFC(result.x[0])