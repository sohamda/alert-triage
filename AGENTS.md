# AGENTS.md

Instructions for coding agents working in this repository.

## Setup

```bash
pip install -e ".[dev]"
```

## Before you commit

Run both, and fix anything they report:

```bash
ruff check .
pytest -q
```

## Conventions

- Code lives in `src/alert_triage/`, tests in `tests/`, one test file per module.
- Every bug fix comes with a test that fails before the fix and passes after it.
- Keep the graph in `graph.py` deterministic: no model calls, no network.
- Tests must not touch the network. Pass a fake session to `fetch_runbook`.
- Dependencies are pinned in `pyproject.toml`. When you bump one, say why in the PR description and link the advisory if there is one.
- Open pull requests as drafts.
