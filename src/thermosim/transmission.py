"""Relazioni cinematiche per una trasmissione manuale."""

from __future__ import annotations

from dataclasses import dataclass
import math


@dataclass(frozen=True)
class ManualTransmission:
    gear_ratios: tuple[float, ...]
    final_drive_ratio: float
    wheel_radius_m: float
    efficiency: float

    def __post_init__(self) -> None:
        if len(self.gear_ratios) != 6:
            raise ValueError("Questa configurazione iniziale richiede esattamente 6 rapporti.")
        if any(ratio <= 0 for ratio in self.gear_ratios):
            raise ValueError("Tutti i rapporti del cambio devono essere > 0.")
        if self.final_drive_ratio <= 0:
            raise ValueError("final_drive_ratio deve essere > 0.")
        if not 0 < self.efficiency <= 1:
            raise ValueError("efficiency deve appartenere all'intervallo (0, 1].")
        if self.wheel_radius_m <= 0:
            raise ValueError("wheel_radius_m deve essere > 0.")

    def engine_speed_rpm(self, vehicle_speed_m_s: float, gear: int) -> float:
        """Regime motore per velocità veicolo e marcia (gear da 1 a 6)."""
        self._validate_gear(gear)
        if vehicle_speed_m_s < 0:
            raise ValueError("La velocità non può essere negativa in questa versione.")
        wheel_rpm = vehicle_speed_m_s / (2.0 * math.pi * self.wheel_radius_m) * 60.0
        return wheel_rpm * self.gear_ratios[gear - 1] * self.final_drive_ratio

    def engine_torque_for_wheel_force(self, wheel_force_n: float, gear: int) -> float:
        """Coppia motore richiesta per ottenere una forza longitudinale alle ruote."""
        self._validate_gear(gear)
        wheel_torque = wheel_force_n * self.wheel_radius_m
        total_ratio = self.gear_ratios[gear - 1] * self.final_drive_ratio
        return wheel_torque / (total_ratio * self.efficiency)

    def wheel_force_from_engine_torque(self, engine_torque_nm: float, gear: int) -> float:
        """Forza di trazione alle ruote generata dalla coppia motore."""
        self._validate_gear(gear)
        total_ratio = self.gear_ratios[gear - 1] * self.final_drive_ratio
        wheel_torque = engine_torque_nm * total_ratio * self.efficiency
        return wheel_torque / self.wheel_radius_m

    @staticmethod
    def _validate_gear(gear: int) -> None:
        if not 1 <= gear <= 6:
            raise ValueError("gear deve essere compreso tra 1 e 6.")
