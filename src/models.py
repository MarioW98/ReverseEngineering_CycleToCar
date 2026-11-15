from dataclasses import dataclass
from typing import List, Tuple
import numpy as np

@dataclass
class Engine:
    """Motore termico con curva di coppia."""
    displacement_cc: float
    max_power_kw: float
    max_torque_nm: float
    torque_curve_rpm: np.ndarray  # array RPM
    torque_curve_nm: np.ndarray   # array Nm
    fuel_type: str  # 'diesel' o 'petrol'
    
    def max_torque_at(self, rpm: float) -> float:
        """Interpola la coppia massima al regime dato."""
        return float(np.interp(rpm, self.torque_curve_rpm, self.torque_curve_nm))

@dataclass
class Transmission:
    """Cambio con rapporti."""
    gear_ratios: List[float]
    final_drive_ratio: float
    efficiency: float = 0.95
    
    @property
    def num_gears(self) -> int:
        return len(self.gear_ratios)

@dataclass
class Vehicle:
    """Veicolo completo."""
    name: str
    mass_kg: float
    cx_a: float  # Cx * Area frontale
    crr: float   # Coefficiente rotolamento
    wheel_radius_m: float
    gamma: float  # Fattore inerzia rotazionale
    engine: Engine
    transmission: Transmission

@dataclass
class DrivingCycle:
    """Ciclo di omologazione espanso a 1 Hz."""
    name: str
    time_s: np.ndarray
    speed_kmh: np.ndarray
    speed_ms: np.ndarray
    acc_ms2: np.ndarray
    
    @property
    def distance_km(self) -> float:
        return float(self.speed_ms.sum() / 1000)
    
    @property
    def duration_s(self) -> float:
        return float(self.time_s[-1])

@dataclass
class EngineOperatingPoint:
    """Punto di funzionamento motore in un istante."""
    time_s: float
    speed_kmh: float
    gear: int
    rpm: float
    torque_nm: float
    power_kw: float
    fuel_cut: bool  # True se DFCO attivo