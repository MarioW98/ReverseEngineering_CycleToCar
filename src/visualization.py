"""
Modulo di visualizzazione per il reverse engineering.
Genera grafici analitici e report comparativi.
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from .models import Vehicle, DrivingCycle, EngineOperatingPoint
from .engine import BSFCModel


def plot_cycle_analysis(vehicle: Vehicle, cycle: DrivingCycle, 
                        points: list[EngineOperatingPoint], 
                        save_path: str = None):
    """
    Plot analitico dettagliato di un ciclo di omologazione.
    Mostra: velocità, marcia, RPM, coppia richiesta vs coppia max OEM.
    """
    time = np.array([p.time_s for p in points])
    v_kmh = np.array([p.speed_kmh for p in points])
    gear = np.array([p.gear for p in points])
    rpm = np.array([p.rpm for p in points])
    torque = np.array([p.torque_nm for p in points])
    fuel_cut = np.array([p.fuel_cut for p in points])
    
    # Coppia max OEM interpolata
    max_torque_oem = np.interp(rpm, vehicle.engine.torque_curve_rpm, 
                                vehicle.engine.torque_curve_nm)
    
    fig, axes = plt.subplots(4, 1, figsize=(14, 12), sharex=True)
    fig.suptitle(f'Analisi Ciclo {cycle.name} - {vehicle.name}', 
                 fontsize=14, fontweight='bold')
    
    # 1. Velocità
    axes[0].plot(time, v_kmh, 'b-', linewidth=1.5, label='Velocità')
    axes[0].set_ylabel('Velocità [km/h]')
    axes[0].grid(True, alpha=0.3)
    axes[0].legend(loc='upper right')
    axes[0].set_ylim(bottom=0)
    
    # 2. Marcia
    axes[1].plot(time, gear, 'k-', linewidth=1.5, label='Marcia inserita')
    axes[1].set_ylabel('Marcia')
    axes[1].set_yticks(range(1, vehicle.transmission.num_gears + 1))
    axes[1].grid(True, alpha=0.3)
    axes[1].legend(loc='upper right')
    axes[1].set_ylim(0, vehicle.transmission.num_gears + 1)
    
    # 3. RPM
    axes[2].plot(time, rpm, 'r-', linewidth=1.2, label='RPM motore')
    axes[2].axhline(800, color='gray', linestyle='--', alpha=0.6, label='Minimo / soglia DFCO')
    axes[2].set_ylabel('RPM')
    axes[2].grid(True, alpha=0.3)
    axes[2].legend(loc='upper right')
    
    # 4. Coppia
    axes[3].plot(time, torque, 'g-', linewidth=1.2, label='Coppia richiesta')
    axes[3].plot(time, max_torque_oem, 'k:', linewidth=1.0, alpha=0.7, 
                 label='Coppia max OEM')
    # Evidenzia zone DFCO
    axes[3].fill_between(time, 0, -50, where=fuel_cut, 
                         color='orange', alpha=0.3, label='DFCO attivo')
    axes[3].set_xlabel('Tempo [s]')
    axes[3].set_ylabel('Coppia [Nm]')
    axes[3].grid(True, alpha=0.3)
    axes[3].legend(loc='upper right')
    
    plt.tight_layout()
    
    if save_path:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"   ✓ Salvato: {save_path}")
    else:
        plt.show()
    
    plt.close()


def plot_comparison_report(results: dict, targets: dict, 
                           bsfc_model: BSFCModel,
                           save_path: str = None):
    """
    Report comparativo tra cicli diversi (es. NEDC vs EUDC).
    Mostra consumo target vs simulato e statistiche operative.
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle(f'Report Comparativo - BSFC calibrato: {bsfc_model.bsfc_g_kwh:.1f} g/kWh',
                 fontsize=13, fontweight='bold')
    
    # 1. Bar chart consumi
    cycle_names = list(results.keys())
    simulated = [results[k]['consumption_l_100km'] for k in cycle_names]
    target_vals = [targets[k] for k in cycle_names]
    
    x = np.arange(len(cycle_names))
    width = 0.35
    
    bars1 = axes[0].bar(x - width/2, target_vals, width, 
                        label='Target omologazione', color='steelblue', alpha=0.8)
    bars2 = axes[0].bar(x + width/2, simulated, width, 
                        label='Simulato', color='coral', alpha=0.8)
    
    axes[0].set_ylabel('Consumo [L/100km]')
    axes[0].set_title('Consumi: Target vs Simulato')
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(cycle_names)
    axes[0].legend()
    axes[0].grid(True, alpha=0.3, axis='y')
    
    # Aggiungi valori sulle barre
    for bar in bars1:
        axes[0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
                     f'{bar.get_height():.2f}', ha='center', va='bottom', fontsize=9)
    for bar in bars2:
        axes[0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
                     f'{bar.get_height():.2f}', ha='center', va='bottom', fontsize=9)
    
    # 2. Statistiche operative
    stats_data = []
    for name, result in results.items():
        points = result['points']
        active_points = [p for p in points if not p.fuel_cut]
        dfco_points = [p for p in points if p.fuel_cut]
        
        avg_rpm = np.mean([p.rpm for p in active_points]) if active_points else 0
        avg_torque = np.mean([p.torque_nm for p in active_points]) if active_points else 0
        dfco_pct = 100 * len(dfco_points) / len(points) if points else 0
        
        stats_data.append({
            'name': name,
            'avg_rpm': avg_rpm,
            'avg_torque': avg_torque,
            'dfco_pct': dfco_pct
        })
    
    # Plot statistiche
    ax_stats = axes[1]
    ax_stats.axis('off')
    
    table_data = [['Ciclo', 'RPM medi', 'Coppia media [Nm]', '% DFCO']]
    for s in stats_data:
        table_data.append([
            s['name'],
            f"{s['avg_rpm']:.0f}",
            f"{s['avg_torque']:.1f}",
            f"{s['dfco_pct']:.1f}%"
        ])
    
    table = ax_stats.table(cellText=table_data, loc='center', cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.8)
    
    # Evidenzia header
    for i in range(len(table_data[0])):
        table[0, i].set_facecolor('#4472C4')
        table[0, i].set_text_props(color='white', fontweight='bold')
    
    ax_stats.set_title('Statistiche operative motore')
    
    plt.tight_layout()
    
    if save_path:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"   ✓ Salvato: {save_path}")
    else:
        plt.show()
    
    plt.close()