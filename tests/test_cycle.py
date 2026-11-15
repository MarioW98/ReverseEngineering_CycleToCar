import pytest

from thermosim.cycle import DrivingCycle, acceleration_trace
from thermosim.simulation import simulate_wheel_demand
from thermosim.vehicle import VehicleParameters


def test_cycle_loader_and_acceleration(tmp_path):
    path = tmp_path / "cycle.csv"
    path.write_text("time_s,speed_kmh\n0,0\n1,3.6\n2,7.2\n", encoding="utf-8")
    cycle = DrivingCycle.from_csv(path)
    assert acceleration_trace(cycle) == pytest.approx((1.0, 1.0, 1.0))


def test_cycle_requires_increasing_time():
    with pytest.raises(ValueError):
        DrivingCycle((0, 2, 1), (0, 1, 2))


def test_wheel_demand_has_one_sample_per_cycle_point():
    cycle = DrivingCycle((0, 1, 2), (0, 10, 20))
    vehicle = VehicleParameters(1500, 0.3, 2.14, 0.012)
    result = simulate_wheel_demand(cycle, vehicle)
    assert len(result) == 3
    assert result[-1].power_wheel_kw > 0
