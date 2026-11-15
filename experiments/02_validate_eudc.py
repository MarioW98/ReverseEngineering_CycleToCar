from src.loaders import load_vehicle, load_cycle
from src.optimizer import calibrate_bsfc
from src.simulator import simulate_consumption
from src.engine import ConstantBSFC

# Carica
vehicle = load_vehicle("data/cars/BMW/serie 1/116d.yaml", 
                       "data/cars/BMW/serie 1/116d_torque_curve_oem_digitized.csv")
nedc = load_cycle("data/cycles/nedc.csv", "NEDC")
eudc = load_cycle("data/cycles/eudc.csv", "EUDC")

# Calibra su NEDC
bsfc_model = calibrate_bsfc(vehicle, nedc, target_consumption=4.3)

# Valida su EUDC
result_eudc = simulate_consumption(vehicle, eudc, bsfc_model)
print(f"EUDC simulato: {result_eudc['consumption_l_100km']:.2f} L/100km (target: 4.0)")