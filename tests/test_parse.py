import pytest

from alert_triage.parse import LogEvent, parse_log_line


@pytest.mark.parametrize(
    ("level", "message"),
    [
        ("ERROR", "nightly export failed: disk quota exceeded"),
        ("CRITICAL", "nightly export abandoned after 3 retries"),
        ("WARNING", "cleanup job skipped 12 locked files"),
    ],
)
def test_parses_three_fields(level, message):
    event = parse_log_line(f"2026-11-21T02:03:08Z | {level} | {message}")
    assert event == LogEvent("2026-11-21T02:03:08Z", level, "unknown", message)


@pytest.mark.parametrize("line", ["", "timestamp", "timestamp | ERROR"])
def test_rejects_fewer_than_three_fields(line):
    with pytest.raises(ValueError):
        parse_log_line(line)


def test_strips_three_fields():
    event = parse_log_line("  timestamp  |  ERROR  |  failed  ")
    assert event == LogEvent("timestamp", "ERROR", "unknown", "failed")


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
