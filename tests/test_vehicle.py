import pytest

from thermosim.vehicle import VehicleParameters, longitudinal_demand


def test_rolling_and_aero_force_at_constant_speed():
    vehicle = VehicleParameters(
        mass_kg=1500,
        drag_coefficient=0.30,
        frontal_area_m2=2.14,
        rolling_resistance_coefficient=0.012,
    )
    result = longitudinal_demand(20.0, 0.0, vehicle)
    assert result.acceleration_force_n == pytest.approx(0.0)
    assert result.rolling_force_n == pytest.approx(0.012 * 1500 * 9.80665)
    assert result.aerodynamic_force_n > 0
    assert result.total_force_n == pytest.approx(
        result.rolling_force_n + result.aerodynamic_force_n
    )


def test_invalid_mass_is_rejected():
    with pytest.raises(ValueError):
        VehicleParameters(0, 0.3, 2.1, 0.01)
