"""Map a log level to an alert severity."""

from alert_triage.parse import LogEvent

_SEVERITY_BY_LEVEL = {
    "CRITICAL": "critical",
    "ERROR": "high",
    "WARNING": "medium",
    "WARN": "medium",
    "INFO": "low",
    "DEBUG": "low",
}


def classify(event: LogEvent) -> str:
    """Return the alert severity for a log event. Unknown levels are low."""
    return _SEVERITY_BY_LEVEL.get(event.level.upper(), "low")
