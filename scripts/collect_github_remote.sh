#!/bin/zsh
# Mirror-clone every repo the account can access + issues/PRs/comments as JSON (read-only gh API).
D=~/Desktop/benchmark/benchmark-data/authentic/github/github.com
mkdir -p $D
while IFS=$'\t' read -r name priv fork size pushed created; do
  mkdir -p "$D/$(dirname $name)"
  if [ ! -d "$D/$name.git" ]; then git clone --mirror --quiet "https://github.com/$name.git" "$D/$name.git" || echo "CLONE_FAIL $name"; fi
  mkdir -p "$D/$name.meta"
  gh api "repos/$name" > "$D/$name.meta/repo.json" 2>/dev/null
  gh api --paginate "repos/$name/issues?state=all&per_page=100" > "$D/$name.meta/issues_and_prs.json" 2>/dev/null || echo "ISSUES_FAIL $name"
  gh api --paginate "repos/$name/issues/comments?per_page=100" > "$D/$name.meta/issue_comments.json" 2>/dev/null
  gh api --paginate "repos/$name/pulls/comments?per_page=100" > "$D/$name.meta/pr_review_comments.json" 2>/dev/null
  gh api --paginate "repos/$name/releases?per_page=100" > "$D/$name.meta/releases.json" 2>/dev/null
  echo "OK $name"
done < $1
echo ALLDONE
