Log lines with level WARN are classified as low instead of medium

Some services log `WARN` rather than `WARNING`. Those lines come out as `low`, so they never show up in the medium-severity view.

**Repro**

```python
from alert_triage.classify import classify
from alert_triage.parse import parse_log_line

event = parse_log_line("2026-11-20T08:14:03Z | WARN | billing-api | retrying payment provider")
print(classify(event))  # low, expected medium
```

**What done looks like**

- `WARN` is treated the same as `WARNING`
- A test that fails before the fix and passes after it
