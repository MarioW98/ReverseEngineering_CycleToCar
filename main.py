import pandas as pd
import numpy as np
import yaml
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# ==========================================
# 1. CARICAMENTO DATI DAL TUO REPOSITORY
# ==========================================
print("Caricamento dati...")

with open("data/cars/BMW/serie 1/116d.yaml", 'r', encoding='utf-8') as f:
    car = yaml.safe_load(f)

with open("data/cars/BMW/GS6-17DZ-transmission.yaml", 'r', encoding='utf-8') as f:
    trans = yaml.safe_load(f)

torque_curve = pd.read_csv("data/cars/BMW/serie 1/116d_torque_curve_oem_digitized.csv")
nedc_segments = pd.read_csv("data/cycles/nedc.csv")

# Parametri fissi stimati (mancanti nel YAML ma necessari per la fisica)
AIR_DENSITY = 1.225 # kg/m^3
CX_A = 0.64         # Cx * Area frontale (stimato per BMW F20: ~0.29 * 2.2)
CRR = 0.011         # Coefficiente di resistenza al rotolamento (gomme standard)
G = 9.81            # m/s^2
MASS = car['unladen_mass_eu_kg'] + 100 # Massa di prova NEDC (massa in ordine di marcia + 100kg)
GAMMA = 1.08        # Fattore di inerzia rotazionale (ruote, volano, albero)
WHEEL_RADIUS = 0.31 # m (calcolato da 195/55 R16: (16*0.0254 + 2*0.195*0.55)/2)
TRANS_EFF = 0.95    # Efficienza del cambio manuale
DIESEL_DENSITY_G_L = 832 # g/L

TARGET_CONSUMPTION = car['nedc_consumption_l_100km'][2] # 4.3 L/100km (combinato)

# ==========================================
# 2. ESPANSIONE DEL CICLO NEDC A 1 Hz
# ==========================================
print("Espansione ciclo NEDC a 1 Hz...")
cycle_data = []
current_time = 0

for _, row in nedc_segments.iterrows():
    v_start = row['start_velocity'] # km/h
    v_end = row['end_velocity']     # km/h
    acc = row['acceleration']       # m/s^2
    duration = int(row['duration']) # secondi
    
    for t in range(duration):
        # La velocità nel CSV è in km/h, l'accelerazione in m/s^2. 
        # Convertiamo l'incremento di velocità in km/h (acc * 3.6)
        v_kmh = v_start + (acc * t * 3.6)
        v_ms = v_kmh / 3.6
        
        cycle_data.append({
            'time': current_time,
            'v_kmh': v_kmh,
            'v_ms': v_ms,
            'acc_ms2': acc
        })
        current_time += 1

df_cycle = pd.DataFrame(cycle_data)
total_distance_km = df_cycle['v_ms'].sum() / 1000 # Distanza totale in km (dovrebbe essere ~11 km)
print(f"Distanza totale ciclo simulato: {total_distance_km:.2f} km")

# ==========================================
# 3. SIMULAZIONE DINAMICA E CAMBIO MARCE
# ==========================================
print("Simulazione dinamica del veicolo...")
gear_ratios = trans['gear_ratios']
final_drive = trans['final_drive_ratio']

results = []
current_gear = 1

for idx, row in df_cycle.iterrows():
    v_ms = row['v_ms']
    acc = row['acc_ms2']
    
    # 3.1 Calcolo delle forze resistenti
    f_aero = 0.5 * AIR_DENSITY * CX_A * (v_ms ** 2)
    f_roll = MASS * G * CRR
    f_inertia = MASS * GAMMA * acc
    f_tractive = f_aero + f_roll + f_inertia
    
    # 3.2 Logica di cambio marcia (semplificata per NEDC: cambiata anticipata per consumi)
    if v_ms == 0:
        current_gear = 1
        rpm = 800 # Minimo
    else:
        # Calcola RPM nella marcia corrente
        wheel_rps = v_ms / (2 * np.pi * WHEEL_RADIUS)
        engine_rps = wheel_rps * gear_ratios[current_gear - 1] * final_drive
        rpm = engine_rps * 60
        
        # Logica di salita/discesa marce con isteresi
        if rpm > 2200 and current_gear < 6:
            current_gear += 1
            wheel_rps = v_ms / (2 * np.pi * WHEEL_RADIUS)
            engine_rps = wheel_rps * gear_ratios[current_gear - 1] * final_drive
            rpm = engine_rps * 60
        elif rpm < 1100 and current_gear > 1:
            current_gear -= 1
            wheel_rps = v_ms / (2 * np.pi * WHEEL_RADIUS)
            engine_rps = wheel_rps * gear_ratios[current_gear - 1] * final_drive
            rpm = engine_rps * 60
            
    # Limita RPM al minimo al di sotto del quale il motore non scende (frizione o idle)
    rpm = max(rpm, 800)
    
    # 3.3 Calcolo Coppia Motore Richiesta
    t_wheel = f_tractive * WHEEL_RADIUS
    # Se siamo in decelerazione (f_tractive < 0), il motore è in taglio carburante (DFCO)
    t_engine = (t_wheel / (gear_ratios[current_gear - 1] * final_drive * TRANS_EFF)) if t_wheel > 0 else 0.0
    
    results.append({
        'time': row['time'],
        'v_kmh': row['v_kmh'],
        'gear': current_gear,
        'rpm': rpm,
        't_engine_nm': t_engine,
        'f_tractive_n': f_tractive
    })

df_sim = pd.DataFrame(results)

# ==========================================
# 4. REVERSE ENGINEERING: OTTIMIZZAZIONE BSFC
# ==========================================
print("Ottimizzazione del BSFC per matchare l'omologazione...")

def calculate_consumption(bsfc_constant):
    """
    Calcola il consumo L/100km dato un BSFC costante (g/kWh).
    """
    # Potenza motore in kW: P = (Coppia * RPM) / 9549
    power_kw = (df_sim['t_engine_nm'] * df_sim['rpm']) / 9549.0
    
    # Energia totale in kWh (ogni riga è 1 secondo, quindi / 3600)
    total_energy_kwh = power_kw.sum() / 3600.0
    
    # Massa carburante in grammi
    fuel_mass_g = total_energy_kwh * bsfc_constant
    
    # Volume in litri
    fuel_volume_l = fuel_mass_g / DIESEL_DENSITY_G_L
    
    # Consumo L/100km
    consumption = (fuel_volume_l / total_distance_km) * 100
    return consumption

def objective_function(bsfc_constant):
    """Funzione da minimizzare: differenza al quadrato tra consumo simulato e target"""
    sim_consumption = calculate_consumption(bsfc_constant[0])
    return (sim_consumption - TARGET_CONSUMPTION) ** 2

# Esegui l'ottimizzazione (il BSFC di un diesel moderno è tipicamente tra 180 e 250 g/kWh)
initial_guess = [220.0]
result = minimize(objective_function, initial_guess, bounds=[(150.0, 350.0)])

optimal_bsfc = result.x[0]
final_consumption = calculate_consumption(optimal_bsfc)

print("\n" + "="*50)
print("🏆 RISULTATI REVERSE ENGINEERING")
print("="*50)
print(f"Consumo NEDC Dichiarato:      {TARGET_CONSUMPTION:.1f} L/100km")
print(f"Consumo NEDC Simulato:        {final_consumption:.1f} L/100km")
print(f"BSFC Medio Stimato (Costante): {optimal_bsfc:.1f} g/kWh")
print(f"Energia totale richiesta al motore: {((df_sim['t_engine_nm'] * df_sim['rpm']) / 9549.0).sum() / 3600:.2f} kWh")
print("="*50 + "\n")

# ==========================================
# 5. VISUALIZZAZIONE GRAFICA
# ==========================================
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 10), sharex=True)

# Grafico 1: Velocità e Marcia
ax1.plot(df_sim['time'], df_sim['v_kmh'], label='Velocità (km/h)', color='blue')
ax1.set_ylabel('Velocità (km/h)')
ax1.grid(True, alpha=0.3)
ax1.legend(loc='upper left')

# Grafico 2: Regime Motore
ax2.plot(df_sim['time'], df_sim['rpm'], label='RPM', color='red')
ax2.axhline(2200, color='red', linestyle='--', alpha=0.5, label='Soglia cambio su (simulata)')
ax2.set_ylabel('RPM')
ax2.grid(True, alpha=0.3)
ax2.legend(loc='upper left')

# Grafico 3: Coppia Motore Richiesta
ax3.plot(df_sim['time'], df_sim['t_engine_nm'], label='Coppia Motore Richiesta (Nm)', color='green')
# Sovrapposizione della curva di coppia massima OEM per contesto
# (Interpoliamo la curva massima per mostrarla come limite)
max_torque_at_rpm = np.interp(df_sim['rpm'], torque_curve['rpm'], torque_curve['torque_nm'])
ax3.plot(df_sim['time'], max_torque_at_rpm, label='Coppia Max OEM (limite)', color='black', linestyle=':', alpha=0.7)

ax3.set_xlabel('Tempo (secondi)')
ax3.set_ylabel('Coppia (Nm)')
ax3.grid(True, alpha=0.3)
ax3.legend(loc='upper left')

plt.tight_layout()
plt.show()