from alert_triage.runbooks import fetch_runbook, runbook_url


class _FakeResponse:
    text = "# billing-api runbook"

    def raise_for_status(self):
        pass


class _FakeSession:
    def __init__(self):
        self.calls = []

    def get(self, url, timeout):
        self.calls.append((url, timeout))
        return _FakeResponse()


def test_runbook_url():
    assert runbook_url("billing-api") == "https://runbooks.example.com/billing-api.md"


def test_fetch_runbook_uses_the_session_with_a_timeout():
    session = _FakeSession()
    assert fetch_runbook("billing-api", session=session) == "# billing-api runbook"
    assert session.calls == [("https://runbooks.example.com/billing-api.md", 10)]
