from alert_triage.graph import triage


def test_critical_line_pages_on_call():
    state = triage("2026-11-20T08:14:03Z | CRITICAL | billing-api | database unreachable")
    assert state["severity"] == "critical"
    assert state["action"] == "page on-call for billing-api"


def test_error_without_service_is_recorded_as_high():
    state = triage("2026-11-21T02:03:07Z | ERROR | nightly export failed: disk quota exceeded")
    assert state["event"].service == "unknown"
    assert state["severity"] == "high"
    assert state["action"] == "record"


def test_critical_without_service_pages_on_call():
    state = triage("2026-11-21T02:03:08Z | CRITICAL | nightly export abandoned after 3 retries")
    assert state["event"].service == "unknown"
    assert state["severity"] == "critical"
    assert state["action"] == "page on-call for unknown"


def test_info_line_is_recorded():
    state = triage("2026-11-20T08:14:03Z | INFO | billing-api | started")
    assert state["severity"] == "low"
    assert state["action"] == "record"
