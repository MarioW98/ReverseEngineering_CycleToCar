"""Calcolo della domanda alle ruote su un ciclo di guida (backward, base)."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import csv
from pathlib import Path

from .cycle import DrivingCycle, acceleration_trace
from .vehicle import VehicleParameters, longitudinal_demand


@dataclass(frozen=True)
class DemandSample:
    time_s: float
    speed_kmh: float
    acceleration_m_s2: float
    force_wheel_n: float
    power_wheel_kw: float


def simulate_wheel_demand(
    cycle: DrivingCycle,
    vehicle: VehicleParameters,
    *,
    grade_rad: float = 0.0,
    headwind_m_s: float = 0.0,
) -> tuple[DemandSample, ...]:
    """Restituisce forza e potenza richieste alle ruote campione per campione."""
    accelerations = acceleration_trace(cycle)
    samples: list[DemandSample] = []
    for time_s, speed_kmh, acceleration in zip(
        cycle.time_s, cycle.speed_kmh, accelerations, strict=True
    ):
        balance = longitudinal_demand(
            speed_kmh / 3.6,
            acceleration,
            vehicle,
            grade_rad=grade_rad,
            headwind_m_s=headwind_m_s,
        )
        samples.append(
            DemandSample(
                time_s=time_s,
                speed_kmh=speed_kmh,
                acceleration_m_s2=acceleration,
                force_wheel_n=balance.total_force_n,
                power_wheel_kw=balance.wheel_power_kw,
            )
        )
    return tuple(samples)


def export_demand_csv(samples: tuple[DemandSample, ...], path: str | Path) -> None:
    """Esporta la domanda alle ruote in CSV."""
    if not samples:
        raise ValueError("Nessun campione da esportare.")
    with Path(path).open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(asdict(samples[0]).keys()))
        writer.writeheader()
        writer.writerows(asdict(sample) for sample in samples)
