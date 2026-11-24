# alert-triage

A small LangGraph service that turns log lines into alerts. Each line is parsed, given a severity, and either pages on-call (critical) or is recorded.

```
parse -> classify -> page   (critical)
                  -> record (everything else)
```

## Run it

```bash
pip install -e ".[dev]"
python -c "from alert_triage.graph import triage; print(triage('2026-11-20T08:14:03Z | CRITICAL | billing-api | database unreachable'))"
```

## Test it

```bash
ruff check .
pytest -q
```
