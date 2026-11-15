import numpy as np
from .models import Vehicle, DrivingCycle, EngineOperatingPoint

AIR_DENSITY = 1.225  # kg/m³
G = 9.81             # m/s²

def calculate_resistant_forces(vehicle: Vehicle, speed_ms: float, acc_ms2: float) -> float:
    """Calcola la forza resistente totale (N)."""
    f_aero = 0.5 * AIR_DENSITY * vehicle.cx_a * (speed_ms ** 2)
    f_roll = vehicle.mass_kg * G * vehicle.crr
    f_inertia = vehicle.mass_kg * vehicle.gamma * acc_ms2
    return f_aero + f_roll + f_inertia

def get_nedc_gear(speed_kmh: float, current_gear: int, vehicle: Vehicle) -> int:
    """Logica di cambiata NEDC con isteresi."""
    if speed_kmh < 1.0:
        return 1
    
    # Calcola RPM nella marcia corrente
    wheel_rps = (speed_kmh / 3.6) / (2 * np.pi * vehicle.wheel_radius_m)
    engine_rps = wheel_rps * vehicle.transmission.gear_ratios[current_gear - 1] * vehicle.transmission.final_drive_ratio
    current_rpm = engine_rps * 60
    
    # Scalata se RPM troppo bassi
    if current_rpm < 800 and current_gear > 1:
        current_gear -= 1
    
    # Salita basata su soglie NEDC
    if current_gear == 1 and speed_kmh >= 15: current_gear = 2
    elif current_gear == 2 and speed_kmh >= 35: current_gear = 3
    elif current_gear == 3 and speed_kmh >= 50: current_gear = 4
    elif current_gear == 4 and speed_kmh >= 70: current_gear = 5
    elif current_gear == 5 and speed_kmh >= 100: current_gear = 6
    
    return current_gear

def simulate_cycle(vehicle: Vehicle, cycle: DrivingCycle) -> list[EngineOperatingPoint]:
    """Simula il ciclo e restituisce i punti di funzionamento motore."""
    points = []
    current_gear = 1
    
    for i in range(len(cycle.time_s)):
        speed_ms = cycle.speed_ms[i]
        speed_kmh = cycle.speed_kmh[i]
        acc = cycle.acc_ms2[i]
        
        # Cambio marcia
        current_gear = get_nedc_gear(speed_kmh, current_gear, vehicle)
        
        # RPM
        if speed_ms <= 0.1:
            rpm = 800.0
        else:
            wheel_rps = speed_ms / (2 * np.pi * vehicle.wheel_radius_m)
            engine_rps = wheel_rps * vehicle.transmission.gear_ratios[current_gear - 1] * vehicle.transmission.final_drive_ratio
            rpm = max(engine_rps * 60, 800.0)
        
        # Forze e coppia
        f_tractive = calculate_resistant_forces(vehicle, speed_ms, acc)
        t_wheel = f_tractive * vehicle.wheel_radius_m
        
        # DFCO
        fuel_cut = (f_tractive <= 0 and rpm > 800)
        
        if fuel_cut:
            t_engine = 0.0
        else:
            gear_ratio = vehicle.transmission.gear_ratios[current_gear - 1]
            t_engine = (t_wheel / (gear_ratio * vehicle.transmission.final_drive_ratio * vehicle.transmission.efficiency)) if t_wheel > 0 else 0.0
        
        # Potenza
        power_kw = (t_engine * rpm) / 9549.0
        
        points.append(EngineOperatingPoint(
            time_s=cycle.time_s[i],
            speed_kmh=speed_kmh,
            gear=current_gear,
            rpm=rpm,
            torque_nm=t_engine,
            power_kw=power_kw,
            fuel_cut=fuel_cut
        ))
    
    return points