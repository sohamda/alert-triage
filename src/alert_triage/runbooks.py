"""Look up the runbook for a service."""

import requests

RUNBOOK_BASE_URL = "https://runbooks.example.com"


def runbook_url(service: str) -> str:
    return f"{RUNBOOK_BASE_URL}/{service}.md"


def fetch_runbook(service: str, session: requests.Session | None = None) -> str:
    """Download a service's runbook. Pass a session to reuse connections or to test."""
    session = session or requests.Session()
    response = session.get(runbook_url(service), timeout=10)
    response.raise_for_status()
    return response.text
