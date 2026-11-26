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

## Production traffic

`ops/traffic.log` is a sample of what the service sees in production. `scripts/simulate_traffic.py` plays it through the graph with LangSmith tracing on, one trace per line, into the project `alert-triage-prod`:

```bash
export LANGSMITH_API_KEY=...
python scripts/simulate_traffic.py
```

Lines that crash the graph show up in LangSmith as failed runs, with the input and the traceback. The `traffic` workflow does the same from `main` every six hours (and on demand from the Actions tab) when the repository secret `LANGSMITH_API_KEY` is set.
