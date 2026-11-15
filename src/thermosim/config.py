"""Caricamento e audit dei file di configurazione YAML."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


class ConfigurationError(ValueError):
    """Configurazione mancante, malformata o incoerente."""


def load_yaml(path: str | Path) -> dict[str, Any]:
    """Carica un file YAML e verifica che la radice sia una mappa."""
    file_path = Path(path)
    if not file_path.is_file():
        raise ConfigurationError(f"File non trovato: {file_path}")
    try:
        with file_path.open("r", encoding="utf-8") as stream:
            payload = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        raise ConfigurationError(f"YAML non valido in {file_path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise ConfigurationError(f"La radice di {file_path} deve essere una mappa YAML.")
    return payload


@dataclass(frozen=True)
class AuditItem:
    level: str
    path: str
    message: str


def _is_missing(value: Any) -> bool:
    return value is None or value == "" or value == []


def audit_vehicle_config(config_dir: str | Path) -> list[AuditItem]:
    """Controlla completezza minima; non assegna valori ai dati mancanti."""
    root = Path(config_dir)
    items: list[AuditItem] = []

    required_files = [
        root / "common" / "vehicle.yaml",
        root / "common" / "road_load.yaml",
        root / "114d" / "engine.yaml",
        root / "114d" / "transmission.yaml",
        root / "116d" / "engine.yaml",
        root / "116d" / "transmission.yaml",
        root / "118d" / "engine.yaml",
        root / "118d" / "transmission.yaml",
        root / "114d" / "vehicle.yaml",
        root / "116d" / "vehicle.yaml",
        root / "118d" / "vehicle.yaml",
    ]
    for file_path in required_files:
        if not file_path.is_file():
            items.append(AuditItem("ERROR", str(file_path), "File richiesto assente."))

    if any(item.level == "ERROR" for item in items):
        return items

    vehicle = load_yaml(root / "common" / "vehicle.yaml")
    if vehicle.get("drive_configuration") != "RWD":
        items.append(AuditItem("WARNING", "common/vehicle.yaml", "La configurazione attesa è RWD."))
    if vehicle.get("transmission_type") != "manual":
        items.append(AuditItem("WARNING", "common/vehicle.yaml", "La configurazione attesa è manuale."))
    if vehicle.get("transmission_gears") != 6:
        items.append(AuditItem("WARNING", "common/vehicle.yaml", "La configurazione attesa è a 6 marce."))

    road_load = load_yaml(root / "common" / "road_load.yaml")
    for key in ("drag_coefficient", "frontal_area_m2", "rolling_resistance_coefficient"):
        if _is_missing(road_load.get(key)):
            items.append(AuditItem("PENDING", "common/road_load.yaml", f"Dato da acquisire: {key}."))
    if _is_missing(road_load.get("road_load_coefficients_F0_F1_F2")):
        items.append(AuditItem("PENDING", "common/road_load.yaml", "Coefficienti road-load F0/F1/F2 non acquisiti."))

    for variant in ("114d", "116d", "118d"):
        engine_path = root / variant / "engine.yaml"
        transmission_path = root / variant / "transmission.yaml"
        engine = load_yaml(engine_path)
        transmission = load_yaml(transmission_path)
        vehicle = load_yaml(root / variant / "vehicle.yaml")

        if _is_missing(vehicle.get("nedc_test_mass_kg")):
            items.append(AuditItem("PENDING", f"{variant}/vehicle.yaml", "Massa di prova NEDC da acquisire; non dedurla automaticamente dalla massa EU."))
        if _is_missing(vehicle.get("wheel_dynamic_radius_m")):
            items.append(AuditItem("PENDING", f"{variant}/vehicle.yaml", "Raggio dinamico ruota/pneumatico da definire."))
        if _is_missing(engine.get("engine_code")):
            items.append(AuditItem("PENDING", f"{variant}/engine.yaml", "Codice motore da verificare tramite VIN/data produzione."))
        elif engine.get("engine_code_verification"):
            items.append(AuditItem("PENDING", f"{variant}/engine.yaml", "Codice/suffisso motore da confermare tramite VIN."))
        if _is_missing(engine.get("torque_curve_file")):
            items.append(AuditItem("PENDING", f"{variant}/engine.yaml", "Curva coppia/rpm non ancora importata."))
        if _is_missing(engine.get("bsfc_map_file")):
            items.append(AuditItem("PENDING", f"{variant}/engine.yaml", "Mappa BSFC non ancora importata; consumi non calcolabili in modo validato."))

        ratios = transmission.get("gear_ratios")
        if not isinstance(ratios, list) or len(ratios) != 6 or any(value is None for value in ratios):
            items.append(AuditItem("PENDING", f"{variant}/transmission.yaml", "Rapporti delle 6 marce da verificare e inserire."))
        if _is_missing(transmission.get("final_drive_ratio")):
            items.append(AuditItem("PENDING", f"{variant}/transmission.yaml", "Rapporto al ponte da verificare e inserire."))

    if not items:
        items.append(AuditItem("OK", str(root), "Configurazione completa rispetto ai controlli implementati."))
    return items
