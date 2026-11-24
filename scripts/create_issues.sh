#!/usr/bin/env bash
# Create the three demo issues on GitHub, in order, so they get numbers 1, 2 and 3.
# Run from the repo root after the first push: ./scripts/create_issues.sh
# Needs the GitHub CLI (gh), signed in, with this repo as the default remote.
set -euo pipefail

for file in issues/01-bump-requests-cve.md issues/02-warn-level-misclassified.md issues/03-scheduler-lines-crash.md; do
  title="$(head -n 1 "$file")"
  body="$(tail -n +3 "$file")"
  gh issue create --title "$title" --body "$body"
done
