import pytest

from thermosim.engine import TorqueCurve


def test_torque_curve_interpolation_and_power(tmp_path):
    csv_path = tmp_path / "curve.csv"
    csv_path.write_text("rpm,torque_nm\n1000,100\n2000,200\n", encoding="utf-8")
    curve = TorqueCurve.from_csv(csv_path)
    assert curve.torque_at(1500) == pytest.approx(150)
    assert curve.power_kw_at(2000) == pytest.approx(41.8879, rel=1e-4)
    with pytest.raises(ValueError):
        curve.torque_at(500)
