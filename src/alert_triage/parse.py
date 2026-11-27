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
    """Parse a log line, defaulting an omitted service to unknown."""
    fields = line.strip().split(" | ", 3)
    if len(fields) == 3:
        timestamp, level, message = fields
        service = "unknown"
    else:
        timestamp, level, service, message = fields
    return LogEvent(
        timestamp=timestamp.strip(),
        level=level.strip(),
        service=service.strip(),
        message=message.strip(),
    )
