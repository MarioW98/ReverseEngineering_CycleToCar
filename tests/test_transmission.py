import pytest

from thermosim.transmission import ManualTransmission


def test_manual_transmission_kinematics():
    gearbox = ManualTransmission(
        gear_ratios=(4.002, 2.130, 1.396, 1.0, 0.781, 0.668),
        final_drive_ratio=3.077,
        wheel_radius_m=0.30,
        efficiency=0.95,
    )
    rpm = gearbox.engine_speed_rpm(10.0, 6)
    assert rpm > 0
    wheel_force = gearbox.wheel_force_from_engine_torque(200.0, 3)
    recovered_torque = gearbox.engine_torque_for_wheel_force(wheel_force, 3)
    assert recovered_torque == pytest.approx(200.0)


def test_manual_requires_six_gears():
    with pytest.raises(ValueError):
        ManualTransmission((4.0, 2.0, 1.0), 3.0, 0.30, 0.95)
