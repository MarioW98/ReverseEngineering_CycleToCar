"""Dinamica longitudinale e resistenze all'avanzamento, in unità SI."""

from __future__ import annotations

from dataclasses import dataclass
import math


G0_M_S2 = 9.80665


@dataclass(frozen=True)
class VehicleParameters:
    mass_kg: float
    drag_coefficient: float
    frontal_area_m2: float
    rolling_resistance_coefficient: float
    air_density_kg_m3: float = 1.225
    gravity_m_s2: float = G0_M_S2
    rotating_mass_factor: float = 1.0

    def __post_init__(self) -> None:
        positive = {
            "mass_kg": self.mass_kg,
            "frontal_area_m2": self.frontal_area_m2,
            "air_density_kg_m3": self.air_density_kg_m3,
            "gravity_m_s2": self.gravity_m_s2,
            "rotating_mass_factor": self.rotating_mass_factor,
        }
        for name, value in positive.items():
            if value <= 0:
                raise ValueError(f"{name} deve essere > 0.")
        if self.drag_coefficient < 0:
            raise ValueError("drag_coefficient non può essere negativo.")
        if self.rolling_resistance_coefficient < 0:
            raise ValueError("rolling_resistance_coefficient non può essere negativo.")


@dataclass(frozen=True)
class ForceBalance:
    acceleration_force_n: float
    aerodynamic_force_n: float
    rolling_force_n: float
    grade_force_n: float
    total_force_n: float
    wheel_power_kw: float


def longitudinal_demand(
    speed_m_s: float,
    acceleration_m_s2: float,
    vehicle: VehicleParameters,
    *,
    grade_rad: float = 0.0,
    headwind_m_s: float = 0.0,
) -> ForceBalance:
    """Calcola le forze longitudinali richieste alle ruote.

    Convenzione: velocità positiva in avanti; headwind positivo contrario al moto.
    Il modello è quasi-statico e non include esplicitamente inerzie rotanti,
    salvo il fattore moltiplicativo applicato alla massa inerziale.
    """
    if speed_m_s < 0:
        raise ValueError("speed_m_s negativo: la versione iniziale gestisce marcia avanti.")

    effective_mass = vehicle.mass_kg * vehicle.rotating_mass_factor
    acceleration_force = effective_mass * acceleration_m_s2
    relative_air_speed = speed_m_s + headwind_m_s
    aero_force = (
        0.5
        * vehicle.air_density_kg_m3
        * vehicle.drag_coefficient
        * vehicle.frontal_area_m2
        * relative_air_speed
        * abs(relative_air_speed)
    )
    rolling_force = (
        vehicle.rolling_resistance_coefficient
        * vehicle.mass_kg
        * vehicle.gravity_m_s2
        * math.cos(grade_rad)
        if speed_m_s > 0.0
        else 0.0
    )
    grade_force = vehicle.mass_kg * vehicle.gravity_m_s2 * math.sin(grade_rad)
    total_force = acceleration_force + aero_force + rolling_force + grade_force
    wheel_power_kw = total_force * speed_m_s / 1000.0

    return ForceBalance(
        acceleration_force_n=acceleration_force,
        aerodynamic_force_n=aero_force,
        rolling_force_n=rolling_force,
        grade_force_n=grade_force,
        total_force_n=total_force,
        wheel_power_kw=wheel_power_kw,
    )
