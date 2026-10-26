#!/bin/sh
# Pre-commit confidentiality check for this public repository.
# Fails (exit 1) if staged changes contain local paths, usernames, email addresses,
# or wording that suggests an employer or internal team. Lines that state the
# confidentiality rule itself are allowed and listed as "rule text".
# Usage: sh scripts/confidentiality-check.sh   (run after git add)
set -u
pattern='/Users/|@[a-z0-9-]+\.(com|org|eu|net)|employer|committee|our firm|our bank|internal team|internal figure'
rule_text='no employer name|no real employer|No employer name|no employer names|No real employer|no internal team|internal figures or internal team names|employer names, internal figures'
hits=$(git diff --cached -U0 -- . ':(exclude)scripts/confidentiality-check.sh' | grep '^+' | grep -v '^+++' | grep -i -E "$pattern" || true)
[ -z "$hits" ] && { echo "confidentiality check: clean"; exit 0; }
real=$(printf '%s\n' "$hits" | grep -v -i -E "$rule_text" || true)
if [ -n "$real" ]; then
  echo "confidentiality check: BLOCKED. Review these lines:"; printf '%s\n' "$real"; exit 1
fi
echo "confidentiality check: clean (only rule text matched)"; exit 0
