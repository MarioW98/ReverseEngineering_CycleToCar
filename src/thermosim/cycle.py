"""Lettura e controllo di profili velocità-tempo, inclusi i dati NEDC."""

from __future__ import annotations

from dataclasses import dataclass
import csv
from pathlib import Path


@dataclass(frozen=True)
class DrivingCycle:
    time_s: tuple[float, ...]
    speed_kmh: tuple[float, ...]
    name: str = "custom"

    def __post_init__(self) -> None:
        if len(self.time_s) < 2 or len(self.time_s) != len(self.speed_kmh):
            raise ValueError("Il ciclo deve contenere almeno due campioni tempo/velocità.")
        if self.time_s[0] != 0:
            raise ValueError("Il primo campione del ciclo deve essere a 0 secondi.")
        if any(right <= left for left, right in zip(self.time_s, self.time_s[1:])):
            raise ValueError("I tempi devono essere strettamente crescenti.")
        if any(speed < 0 for speed in self.speed_kmh):
            raise ValueError("Le velocità non possono essere negative.")

    @classmethod
    def from_csv(cls, path: str | Path, *, name: str | None = None) -> "DrivingCycle":
        file_path = Path(path)
        time_values: list[float] = []
        speed_values: list[float] = []
        with file_path.open("r", encoding="utf-8-sig", newline="") as stream:
            reader = csv.DictReader(stream)
            required = {"time_s", "speed_kmh"}
            if not reader.fieldnames or not required.issubset(reader.fieldnames):
                raise ValueError("Il CSV deve avere le colonne time_s,speed_kmh.")
            for line_number, row in enumerate(reader, start=2):
                try:
                    time_values.append(float(row["time_s"]))
                    speed_values.append(float(row["speed_kmh"]))
                except (TypeError, ValueError) as exc:
                    raise ValueError(f"Valore non numerico alla riga {line_number}.") from exc
        return cls(tuple(time_values), tuple(speed_values), name or file_path.stem)


def acceleration_trace(cycle: DrivingCycle) -> tuple[float, ...]:
    """Derivata numerica della velocità, con differenze finite in m/s²."""
    speeds = [value / 3.6 for value in cycle.speed_kmh]
    result: list[float] = []
    for index in range(len(speeds)):
        if index == 0:
            delta_v = speeds[1] - speeds[0]
            delta_t = cycle.time_s[1] - cycle.time_s[0]
        elif index == len(speeds) - 1:
            delta_v = speeds[index] - speeds[index - 1]
            delta_t = cycle.time_s[index] - cycle.time_s[index - 1]
        else:
            delta_v = speeds[index + 1] - speeds[index - 1]
            delta_t = cycle.time_s[index + 1] - cycle.time_s[index - 1]
        result.append(delta_v / delta_t)
    return tuple(result)
