Triage crashes on log lines from the scheduler

Since the scheduler started forwarding its logs, triage fails on some lines. Excerpt from the service log:

```
2026-11-21T02:00:01Z | INFO | scheduler | nightly export started
2026-11-21T02:00:04Z | ERROR | nightly export failed: disk quota exceeded
Traceback (most recent call last):
  File "/app/src/alert_triage/graph.py", line 23, in _parse
    return {"event": parse_log_line(state["line"])}
                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/app/src/alert_triage/parse.py", line 21, in parse_log_line
    timestamp, level, service, message = line.strip().split(" | ", 3)
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ValueError: not enough values to unpack (expected 4, got 3)
```

Some scheduler lines have no service field. We lose exactly the errors we most want to see.

**What done looks like**

- Lines with three fields parse, with the service set to `unknown`
- The ERROR line above is still classified as `high`
- A test for the three-field case
