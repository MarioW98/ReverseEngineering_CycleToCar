"""
ReverseEngineering_CycleToCar - Entry Point
============================================

Workflow:
1. Carica i dati della BMW 116d F20
2. Calibra il BSFC costante sul ciclo NEDC (target: 4.3 L/100km)
3. Valida il modello sul ciclo EUDC (target: 4.0 L/100km)
4. Genera report e grafici comparativi

Usage:
    python main.py
"""

import sys
from pathlib import Path

# Aggiungi la root del progetto al path per importare src/
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.loaders import load_vehicle, load_cycle
from src.optimizer import calibrate_bsfc
from src.simulator import simulate_consumption
from src.visualization import plot_cycle_analysis, plot_comparison_report


def main():
    print("=" * 60)
    print("  REVERSE ENGINEERING: CYCLE TO CAR")
    print("  BMW 116d F20 (B37D15U0) - MY2016")
    print("=" * 60)
    
    # ==========================================
    # 1. CARICAMENTO DATI
    # ==========================================
    print("\n📥 [1/4] Caricamento dati veicolo e cicli...")
    
    vehicle = load_vehicle(
        yaml_path="data/cars/BMW/serie 1/116d.yaml",
        torque_csv_path="data/cars/BMW/serie 1/116d_torque_curve_oem_digitized.csv"
    )
    print(f"   ✓ Veicolo: {vehicle.name}")
    print(f"   ✓ Massa: {vehicle.mass_kg:.0f} kg | Cx·A: {vehicle.cx_a:.2f} m²")
    print(f"   ✓ Motore: {vehicle.engine.displacement_cc:.0f} cc, "
          f"{vehicle.engine.max_power_kw:.0f} kW, "
          f"{vehicle.engine.max_torque_nm:.0f} Nm")
    
    nedc = load_cycle("data/cycles/nedc.csv", "NEDC")
    eudc = load_cycle("data/cycles/eudc.csv", "EUDC")
    print(f"   ✓ Ciclo NEDC: {nedc.distance_km:.2f} km in {nedc.duration_s:.0f} s")
    print(f"   ✓ Ciclo EUDC: {eudc.distance_km:.2f} km in {eudc.duration_s:.0f} s")
    
    # Target dai dati di omologazione
    TARGET_NEDC_COMBINED = 4.3  # L/100km
    TARGET_EUDC = 4.0           # L/100km
    
    # ==========================================
    # 2. CALIBRAZIONE SU NEDC
    # ==========================================
    print("\n🧮 [2/4] Calibrazione BSFC su ciclo NEDC...")
    
    bsfc_model = calibrate_bsfc(vehicle, nedc, target_consumption=TARGET_NEDC_COMBINED)
    result_nedc = simulate_consumption(vehicle, nedc, bsfc_model)
    
    print(f"   ✓ BSFC calibrato: {bsfc_model.bsfc_g_kwh:.1f} g/kWh")
    print(f"   ✓ Consumo NEDC simulato: {result_nedc['consumption_l_100km']:.2f} L/100km")
    print(f"   ✓ Consumo NEDC target:   {TARGET_NEDC_COMBINED:.2f} L/100km")
    print(f"   ✓ Errore: {abs(result_nedc['consumption_l_100km'] - TARGET_NEDC_COMBINED):.3f} L/100km")
    
    # ==========================================
    # 3. VALIDAZIONE CROSS SU EUDC
    # ==========================================
    print("\n🧪 [3/4] Validazione cross su ciclo EUDC...")
    
    result_eudc = simulate_consumption(vehicle, eudc, bsfc_model)
    
    print(f"   ✓ Consumo EUDC simulato: {result_eudc['consumption_l_100km']:.2f} L/100km")
    print(f"   ✓ Consumo EUDC target:   {TARGET_EUDC:.2f} L/100km")
    delta = result_eudc['consumption_l_100km'] - TARGET_EUDC
    print(f"   ✓ Δ (simulato - target): {delta:+.2f} L/100km")
    
    # Diagnosi
    if abs(delta) < 0.2:
        print("   ✅ Modello coerente: BSFC costante sufficiente")
        model_verdict = "FLAT"
    elif delta > 0:
        print("   ⚠️  Modello sovrastima EUDC: BSFC reale più efficiente ad alti carichi")
        model_verdict = "NEEDS_2D_HIGH_LOAD"
    else:
        print("   ⚠️  Modello sottostima EUDC: verificare Cx·A o perdite meccaniche")
        model_verdict = "NEEDS_2D_AERO_CHECK"
    
    # ==========================================
    # 4. REPORT E VISUALIZZAZIONE
    # ==========================================
    print("\n📊 [4/4] Generazione report grafico...")
    
    # Plot dettagliato del ciclo NEDC
    plot_cycle_analysis(
        vehicle=vehicle,
        cycle=nedc,
        points=result_nedc['points'],
        save_path="output/nedc_analysis.png"
    )
    
    # Plot comparativo NEDC vs EUDC
    plot_comparison_report(
        results={
            'NEDC': result_nedc,
            'EUDC': result_eudc
        },
        targets={
            'NEDC': TARGET_NEDC_COMBINED,
            'EUDC': TARGET_EUDC
        },
        bsfc_model=bsfc_model,
        save_path="output/comparison_report.png"
    )
    
    print("   ✓ Grafici salvati in ./output/")
    
    # ==========================================
    # RIEPILOGO FINALE
    # ==========================================
    print("\n" + "=" * 60)
    print("  RIEPILOGO FINALE")
    print("=" * 60)
    print(f"  BSFC calibrato:        {bsfc_model.bsfc_g_kwh:.1f} g/kWh")
    print(f"  NEDC simulato/target:  {result_nedc['consumption_l_100km']:.2f} / {TARGET_NEDC_COMBINED:.2f} L/100km")
    print(f"  EUDC simulato/target:  {result_eudc['consumption_l_100km']:.2f} / {TARGET_EUDC:.2f} L/100km")
    print(f"  Verdetto modello:      {model_verdict}")
    print("=" * 60)
    print("\n💡 Prossimi step suggeriti:")
    if model_verdict != "FLAT":
        print("   → Implementare BSFCMap2D in src/engine.py")
    print("   → Aggiungere ciclo WLTP Class 3")
    print("   → Simulare stili di guida reali")
    print()


if __name__ == "__main__":
    main()