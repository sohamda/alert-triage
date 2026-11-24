from alert_triage.graph import triage


def test_critical_line_pages_on_call():
    state = triage("2026-11-20T08:14:03Z | CRITICAL | billing-api | database unreachable")
    assert state["severity"] == "critical"
    assert state["action"] == "page on-call for billing-api"


def test_info_line_is_recorded():
    state = triage("2026-11-20T08:14:03Z | INFO | billing-api | started")
    assert state["severity"] == "low"
    assert state["action"] == "record"
