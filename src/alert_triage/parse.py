"""Parse raw log lines.

Lines look like:

    2026-11-20T08:14:03Z | ERROR | billing-api | upstream timed out after 30s
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class LogEvent:
    timestamp: str
    level: str
    service: str
    message: str


def parse_log_line(line: str) -> LogEvent:
    """Split a pipe-separated log line into its four fields."""
    timestamp, level, service, message = line.strip().split(" | ", 3)
    return LogEvent(
        timestamp=timestamp.strip(),
        level=level.strip(),
        service=service.strip(),
        message=message.strip(),
    )
