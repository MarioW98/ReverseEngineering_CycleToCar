from src.loaders import load_vehicle, load_cycle
from src.optimizer import calibrate_bsfc
from src.simulator import simulate_consumption

# Carica dati
vehicle = load_vehicle("data/cars/BMW/serie 1/116d.yaml", 
                       "data/cars/BMW/serie 1/116d_torque_curve_oem_digitized.csv")
nedc = load_cycle("data/cycles/nedc.csv", "NEDC")

# Calibra
bsfc_model = calibrate_bsfc(vehicle, nedc, target_consumption=4.3)
print(f"BSFC calibrato: {bsfc_model.bsfc_g_kwh:.1f} g/kWh")

# Simula
result = simulate_consumption(vehicle, nedc, bsfc_model)
print(f"Consumo simulato: {result['consumption_l_100km']:.2f} L/100km")