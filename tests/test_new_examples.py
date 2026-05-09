import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def test_hcs_signal_watcher_module_exists():
    import examples.hcs_signal_watcher as hcs_watcher
    assert hcs_watcher.main is not None


def test_treasury_monitor_module_exists():
    import examples.treasury_monitor as treasury_monitor
    assert treasury_monitor.main is not None


def test_dashboard_export_module_exists():
    import examples.dashboard_export as dashboard_export
    assert dashboard_export.main is not None
