"""Play log lines through the triage graph, traced to LangSmith, as if in production.

Each line becomes one trace in the LangSmith project (default: alert-triage-prod). A line
that crashes the graph shows up there as a failed run with its error and input, which is
what the SRE agent looks for.

    export LANGSMITH_API_KEY=...            # any key for your LangSmith workspace
    python scripts/simulate_traffic.py      # plays ops/traffic.log
    python scripts/simulate_traffic.py --file other.log --project alert-triage-staging

Set LANGSMITH_ENDPOINT for a region or self-hosted LangSmith other than the US cloud.
"""

import argparse
import os
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _commit() -> str:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        return out.stdout.strip() or "unknown"
    except OSError:
        return "unknown"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--file", default=str(ROOT / "ops" / "traffic.log"))
    parser.add_argument(
        "--project", default=os.environ.get("LANGSMITH_PROJECT", "alert-triage-prod")
    )
    args = parser.parse_args()

    if not os.environ.get("LANGSMITH_API_KEY"):
        sys.exit("Set LANGSMITH_API_KEY first.")
    # Set before importing LangGraph, which reads them when it starts tracing.
    os.environ["LANGSMITH_TRACING"] = "true"
    os.environ["LANGSMITH_PROJECT"] = args.project
    sys.path.insert(0, str(ROOT / "src"))

    from langchain_core.tracers.langchain import wait_for_all_tracers

    from alert_triage.graph import build_graph

    graph = build_graph()
    commit = _commit()
    source = Path(args.file).name
    lines = [line for line in Path(args.file).read_text().splitlines() if line.strip()]
    severities: Counter[str] = Counter()
    errors: Counter[str] = Counter()

    for line in lines:
        config = {
            "run_name": "triage",
            "tags": ["traffic-sim"],
            "metadata": {"service": "alert-triage", "commit": commit, "source": source},
        }
        try:
            result = graph.invoke({"line": line}, config)
            severities[result["severity"]] += 1
        except Exception as error:  # noqa: BLE001 - a crash is a result here; LangSmith records it
            errors[f"{type(error).__name__}: {error}"] += 1

    wait_for_all_tracers()

    print(f"Played {len(lines)} lines from {args.file} into LangSmith project '{args.project}'.")
    print("Triaged: " + (", ".join(f"{n} {s}" for s, n in severities.most_common()) or "none"))
    if errors:
        print(f"Failed: {sum(errors.values())}")
        for message, count in errors.most_common():
            print(f"  {count} x {message}")
    else:
        print("Failed: 0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
