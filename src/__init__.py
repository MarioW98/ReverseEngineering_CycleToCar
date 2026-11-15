"""
ReverseEngineering_CycleToCar - Modulo principale
Package per il reverse engineering dei consumi automobilistici
a partire dai cicli di omologazione.
"""

from .models import (
    Engine,
    Transmission,
    Vehicle,
    DrivingCycle,
    EngineOperatingPoint
)

from .loaders import load_vehicle, load_cycle
from .dynamics import simulate_cycle, calculate_resistant_forces
from .engine import BSFCModel, ConstantBSFC
from .simulator import simulate_consumption
from .optimizer import calibrate_bsfc

__version__ = "0.1.0"
__all__ = [
    # Models
    'Engine', 'Transmission', 'Vehicle', 'DrivingCycle', 'EngineOperatingPoint',
    # Loaders
    'load_vehicle', 'load_cycle',
    # Dynamics
    'simulate_cycle', 'calculate_resistant_forces',
    # Engine
    'BSFCModel', 'ConstantBSFC',
    # Simulator
    'simulate_consumption',
    # Optimizer
    'calibrate_bsfc',
]