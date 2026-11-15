from pathlib import Path

from thermosim.config import audit_vehicle_config


def test_bmw_config_is_parseable_and_reports_pending_data():
    project_root = Path(__file__).resolve().parents[1]
    items = audit_vehicle_config(project_root / "config" / "BMW_F20_2016")
    assert not any(item.level == "ERROR" for item in items)
    assert any("NEDC" in item.message for item in items)
    assert any("114d" in item.path and "Rapporti" in item.message for item in items)
