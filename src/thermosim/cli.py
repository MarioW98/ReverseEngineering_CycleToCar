"""Interfaccia a riga di comando di THERMOSIM."""

from __future__ import annotations

import argparse
from pathlib import Path

from .config import ConfigurationError, audit_vehicle_config
from .cycle import DrivingCycle


def _audit_command(config_dir: str) -> int:
    items = audit_vehicle_config(config_dir)
    print(f"Audit configurazione: {config_dir}")
    counts = {level: sum(item.level == level for item in items) for level in ("ERROR", "PENDING", "WARNING", "OK")}
    for item in items:
        print(f"[{item.level:7}] {item.path}: {item.message}")
    print(
        "Riepilogo: "
        + ", ".join(f"{level}={count}" for level, count in counts.items())
    )
    return 1 if counts["ERROR"] else 0


def _cycle_check_command(csv_path: str) -> int:
    cycle = DrivingCycle.from_csv(csv_path)
    duration = cycle.time_s[-1] - cycle.time_s[0]
    max_speed = max(cycle.speed_kmh)
    print(f"Ciclo valido: {cycle.name}")
    print(f"Campioni: {len(cycle.time_s)}")
    print(f"Durata: {duration:.1f} s")
    print(f"Velocità massima: {max_speed:.2f} km/h")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="thermosim", description="Strumenti THERMOSIM v0.1.0")
    subparsers = parser.add_subparsers(dest="command", required=True)

    audit_parser = subparsers.add_parser("audit", help="Controlla completezza dei dati veicolo")
    audit_parser.add_argument("--config-dir", required=True, help="Cartella della famiglia veicolo")

    cycle_parser = subparsers.add_parser("cycle-check", help="Valida un CSV tempo/velocità")
    cycle_parser.add_argument("csv_path", help="CSV con colonne time_s,speed_kmh")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        if args.command == "audit":
            return _audit_command(args.config_dir)
        if args.command == "cycle-check":
            return _cycle_check_command(args.csv_path)
    except (ConfigurationError, ValueError, OSError) as exc:
        parser.exit(2, f"Errore: {exc}\n")
    return 0
