import yaml
import pandas as pd
import numpy as np
from pathlib import Path
from .models import Vehicle, Engine, Transmission, DrivingCycle

def load_vehicle(yaml_path: str, torque_csv_path: str) -> Vehicle:
    """Carica un veicolo da YAML + CSV curva di coppia."""
    # 🔧 FIX: Converti le stringhe in oggetti Path
    yaml_path = Path(yaml_path)
    torque_csv_path = Path(torque_csv_path)
    
    with open(yaml_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    torque_df = pd.read_csv(torque_csv_path)
    
    engine = Engine(
        displacement_cc=data['displacement_cc'],
        max_power_kw=data['max_power_kw'],
        max_torque_nm=data['max_torque_nm'],
        torque_curve_rpm=torque_df['rpm'].values,
        torque_curve_nm=torque_df['torque_nm'].values,
        fuel_type=data['fuel']
    )
    
    # 🔧 FIX: Ora yaml_path è un Path, quindi .parent funziona
    # Struttura: data/cars/BMW/serie 1/116d.yaml
    # parent = data/cars/BMW/serie 1
    # parent.parent = data/cars/BMW  ← qui si trova il transmission YAML
    trans_yaml = yaml_path.parent.parent / f"{data['manual_transmission_code']}-transmission.yaml"
    
    with open(trans_yaml, 'r') as f:
        trans_data = yaml.safe_load(f)
    
    transmission = Transmission(
        gear_ratios=trans_data['gear_ratios'],
        final_drive_ratio=trans_data['final_drive_ratio']
    )
    
    return Vehicle(
        name=data['model'],
        mass_kg=data['unladen_mass_eu_kg'] + 100,  # Massa di prova
        cx_a=0.64,  # TODO: caricare da YAML se disponibile
        crr=0.011,
        wheel_radius_m=0.310,
        gamma=1.08,
        engine=engine,
        transmission=transmission
    )

def load_cycle(csv_path: str, name: str = None) -> DrivingCycle:
    """Carica un ciclo di omologazione da CSV segmentato."""
    # 🔧 FIX: Anche qui converti in Path per coerenza
    csv_path = Path(csv_path)
    df = pd.read_csv(csv_path)
    
    time_list, v_kmh_list, v_ms_list, acc_list = [], [], [], []
    current_time = 0
    
    for _, row in df.iterrows():
        v_start = row['start_velocity']
        acc = row['acceleration']
        duration = int(row['duration'])
        
        for t in range(duration):
            v_kmh = v_start + (acc * t * 3.6)
            v_ms = v_kmh / 3.6
            time_list.append(current_time)
            v_kmh_list.append(v_kmh)
            v_ms_list.append(v_ms)
            acc_list.append(acc)
            current_time += 1
    
    return DrivingCycle(
        name=name or csv_path.stem,
        time_s=np.array(time_list),
        speed_kmh=np.array(v_kmh_list),
        speed_ms=np.array(v_ms_list),
        acc_ms2=np.array(acc_list)
    )