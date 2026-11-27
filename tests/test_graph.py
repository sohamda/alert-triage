import pytest

from alert_triage.graph import triage


@pytest.mark.parametrize(
    ("line", "severity", "action"),
    [
        (
            "2026-11-21T02:03:07Z | ERROR | nightly export failed: disk quota exceeded",
            "high",
            "record",
        ),
        (
            "2026-11-21T02:03:08Z | CRITICAL | nightly export abandoned after 3 retries",
            "critical",
            "page on-call for unknown",
        ),
        (
            "2026-11-21T02:06:19Z | WARNING | cleanup job skipped 12 locked files",
            "medium",
            "record",
        ),
    ],
)
def test_scheduler_line_without_service(line, severity, action):
    state = triage(line)
    assert state["event"].service == "unknown"
    assert state["severity"] == severity
    assert state["action"] == action


def test_critical_line_pages_on_call():
    state = triage("2026-11-20T08:14:03Z | CRITICAL | billing-api | database unreachable")
    assert state["severity"] == "critical"
    assert state["action"] == "page on-call for billing-api"


def test_info_line_is_recorded():
    state = triage("2026-11-20T08:14:03Z | INFO | billing-api | started")
    assert state["severity"] == "low"
    assert state["action"] == "record"
