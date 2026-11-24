Bump requests: 2.31.0 is affected by CVE-2024-35195

`requests` is pinned to `2.31.0` in `pyproject.toml`. Versions before 2.32.0 are affected by [CVE-2024-35195](https://osv.dev/vulnerability/CVE-2024-35195) ([GHSA-9wx4-h78v-vm56](https://github.com/advisories/GHSA-9wx4-h78v-vm56)): once a `Session` makes a request with `verify=False`, later requests to the same host keep skipping certificate verification, even when `verify` is turned back on.

`fetch_runbook` uses a `Session`, so this service is exposed.

**What done looks like**

- `requests` bumped to the latest patched release
- `ruff check .` and `pytest -q` pass
- The PR description links the advisory
