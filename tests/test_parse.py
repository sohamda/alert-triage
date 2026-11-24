from alert_triage.parse import LogEvent, parse_log_line


def test_parses_four_fields():
    event = parse_log_line("2026-11-20T08:14:03Z | ERROR | billing-api | upstream timed out")
    assert event == LogEvent(
        timestamp="2026-11-20T08:14:03Z",
        level="ERROR",
        service="billing-api",
        message="upstream timed out",
    )


def test_message_may_contain_the_separator():
    event = parse_log_line("2026-11-20T08:14:03Z | INFO | api | a | b")
    assert event.message == "a | b"
