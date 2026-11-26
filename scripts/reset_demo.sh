#!/usr/bin/env bash
# Reset the demo repo between rehearsals, so the next run starts clean.
#
# It closes every open PR, deletes every branch except main, closes every open issue,
# and creates the three demo issues again. The new issues get new numbers (4, 5, 6, then
# 7, 8, 9...): a new number means a new agent thread, with no memory of the last rehearsal.
# The script prints the new numbers; use them in the prompts.
#
# It doesn't touch main. If a rehearsal merged a PR, main has changed; the script warns you
# (it compares main with the tag demo-baseline when there is one).
#
# Run from the repo root: bash scripts/reset_demo.sh   (add --yes to skip the prompt)
# Needs the GitHub CLI (gh), signed in, with this repo as the default remote.
set -euo pipefail

repo="$(gh repo view --json nameWithOwner -q .nameWithOwner)"
prs="$(gh pr list --state open --json number -q '.[].number')"
issues="$(gh issue list --state open --json number -q '.[].number')"
branches="$(gh api "repos/$repo/branches" --paginate -q '.[].name' | grep -v '^main$' || true)"
main_sha="$(gh api "repos/$repo/commits/main" -q .sha)"
# The tag demo-baseline marks main as it should be for a demo (README: "Production traffic").
baseline_sha="$(gh api "repos/$repo/commits/demo-baseline" -q .sha 2>/dev/null | grep -E '^[0-9a-f]{40}$' || true)"
commits_on_main="$(gh api "repos/$repo/commits?sha=main&per_page=100" -q 'length')"

echo "Repo:              $repo"
echo "Open PRs to close: ${prs:-none}" | tr '\n' ' '; echo
echo "Branches to delete: ${branches:-none}" | tr '\n' ' '; echo
echo "Issues to close:   ${issues:-none}" | tr '\n' ' '; echo
if [ -n "$baseline_sha" ] && [ "$main_sha" != "$baseline_sha" ]; then
  echo "Warning: main has moved past the tag demo-baseline. A rehearsal may have merged a PR; reset main yourself if so."
elif [ -z "$baseline_sha" ] && [ "$commits_on_main" -gt 1 ]; then
  echo "Warning: main has $commits_on_main commits. A rehearsal may have merged a PR; reset main yourself if so."
fi

if [ "${1:-}" != "--yes" ]; then
  read -r -p "Go ahead? [y/N] " answer
  [ "$answer" = "y" ] || { echo "Nothing changed."; exit 0; }
fi

for number in $prs; do
  gh pr close "$number" --comment "Closed by reset_demo.sh before a rehearsal."
done
for branch in $branches; do
  gh api -X DELETE "repos/$repo/git/refs/heads/$branch" >/dev/null && echo "Deleted branch $branch"
done
for number in $issues; do
  gh issue close "$number" --comment "Closed by reset_demo.sh before a rehearsal."
done

echo "Creating the demo issues again:"
bash "$(dirname "$0")/create_issues.sh"
