import numpy as np
from .models import EngineOperatingPoint

class BSFCModel:
    """Modello astratto per il consumo specifico."""
    
    def bsfc_at(self, rpm: float, torque_nm: float) -> float:
        """Restituisce il BSFC in g/kWh al punto dato."""
        raise NotImplementedError
    
    def fuel_consumption(self, points: list[EngineOperatingPoint], distance_km: float) -> float:
        """Calcola il consumo L/100km dato un BSFC model."""
        total_energy_kwh = sum(p.power_kw for p in points if not p.fuel_cut) / 3600.0
        total_fuel_g = sum(
            (p.power_kw / 3600.0) * self.bsfc_at(p.rpm, p.torque_nm)
            for p in points if not p.fuel_cut
        )
        total_fuel_l = total_fuel_g / 832.0  # Diesel density
        return (total_fuel_l / distance_km) * 100

class ConstantBSFC(BSFCModel):
    """BSFC costante (modello semplificato)."""
    
    def __init__(self, bsfc_g_kwh: float):
        self.bsfc_g_kwh = bsfc_g_kwh
    
    def bsfc_at(self, rpm: float, torque_nm: float) -> float:
        return self.bsfc_g_kwh

# TODO: class BSFCMap2D(BSFCModel) — la prossima evoluzione