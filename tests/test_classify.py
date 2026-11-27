import pytest

from alert_triage.classify import classify
from alert_triage.parse import LogEvent, parse_log_line


def _event(level: str) -> LogEvent:
    return LogEvent(timestamp="t", level=level, service="svc", message="m")


@pytest.mark.parametrize(
    ("level", "severity"),
    [
        ("CRITICAL", "critical"),
        ("ERROR", "high"),
        ("WARNING", "medium"),
        ("INFO", "low"),
        ("debug", "low"),
    ],
)
def test_known_levels(level, severity):
    assert classify(_event(level)) == severity


@pytest.mark.parametrize("level", ["WARN", "warn", "WaRn", "WARNING"])
def test_warning_log_line_is_medium(level):
    event = parse_log_line(
        f"2026-11-20T08:14:03Z | {level} | billing-api | retrying payment provider"
    )
    assert classify(event) == "medium"


def test_unknown_level_is_low():
    assert classify(_event("TRACE")) == "low"
