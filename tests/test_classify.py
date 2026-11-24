import pytest

from alert_triage.classify import classify
from alert_triage.parse import LogEvent


def _event(level: str) -> LogEvent:
    return LogEvent(timestamp="t", level=level, service="svc", message="m")


@pytest.mark.parametrize(
    ("level", "severity"),
    [
        ("CRITICAL", "critical"),
        ("ERROR", "high"),
        ("WARNING", "medium"),
        ("WARN", "medium"),
        ("warn", "medium"),
        ("INFO", "low"),
        ("debug", "low"),
    ],
)
def test_known_levels(level, severity):
    assert classify(_event(level)) == severity


def test_unknown_level_is_low():
    assert classify(_event("TRACE")) == "low"
