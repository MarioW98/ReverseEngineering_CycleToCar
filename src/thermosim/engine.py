"""Importazione di curve motore da CSV, senza estrapolazione silenziosa."""

from __future__ import annotations

from dataclasses import dataclass
import csv
from pathlib import Path


@dataclass(frozen=True)
class TorqueCurve:
    rpm: tuple[float, ...]
    torque_nm: tuple[float, ...]

    def __post_init__(self) -> None:
        if len(self.rpm) < 2 or len(self.rpm) != len(self.torque_nm):
            raise ValueError("La curva deve contenere almeno due coppie rpm/coppia.")
        if any(right <= left for left, right in zip(self.rpm, self.rpm[1:])):
            raise ValueError("I valori rpm devono essere strettamente crescenti.")
        if any(value < 0 for value in self.torque_nm):
            raise ValueError("La coppia non può essere negativa.")

    @classmethod
    def from_csv(cls, path: str | Path) -> "TorqueCurve":
        rows: list[tuple[float, float]] = []
        with Path(path).open("r", encoding="utf-8-sig", newline="") as stream:
            reader = csv.DictReader(stream)
            required = {"rpm", "torque_nm"}
            if not reader.fieldnames or not required.issubset(reader.fieldnames):
                raise ValueError("Il CSV deve avere le colonne rpm,torque_nm.")
            for line_number, row in enumerate(reader, start=2):
                try:
                    rows.append((float(row["rpm"]), float(row["torque_nm"])))
                except (TypeError, ValueError) as exc:
                    raise ValueError(f"Valore non numerico alla riga {line_number}.") from exc
        rows.sort(key=lambda item: item[0])
        return cls(tuple(row[0] for row in rows), tuple(row[1] for row in rows))

    def torque_at(self, rpm: float) -> float:
        """Interpolazione lineare; fuori dal dominio genera ValueError."""
        if rpm < self.rpm[0] or rpm > self.rpm[-1]:
            raise ValueError(
                f"{rpm:g} rpm fuori dal dominio della curva "
                f"[{self.rpm[0]:g}, {self.rpm[-1]:g}] rpm."
            )
        for index, (left, right) in enumerate(zip(self.rpm, self.rpm[1:])):
            if left <= rpm <= right:
                fraction = (rpm - left) / (right - left)
                return self.torque_nm[index] + fraction * (
                    self.torque_nm[index + 1] - self.torque_nm[index]
                )
        return self.torque_nm[-1]

    def power_kw_at(self, rpm: float) -> float:
        torque = self.torque_at(rpm)
        return torque * (2.0 * 3.141592653589793 * rpm / 60.0) / 1000.0
