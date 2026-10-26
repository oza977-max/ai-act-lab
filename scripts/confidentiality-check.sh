#!/bin/sh
# Confidentiality guard for this public repository (spec: cross-cutting ADR-007).
# Runs as a git pre-commit hook (install with: sh scripts/install-hooks.sh).
# Blocks a commit when staged changes contain:
#   - local paths, email addresses, or employer-style wording;
#   - any term in the owner's private list .private/deny-terms.txt (git-ignored, one term per line);
#   - spreadsheet files (.xlsx, .numbers), or a staged file name that matches the above.
# Lines that state the confidentiality rule are allowed only in CLAUDE.md, README.md, docs/ and specs/.
set -u
pattern='/Users/|@[a-z0-9-]+\.(com|org|eu|net)|employer|committee|our firm|our bank|internal team|internal figure'
rule_text='no employer name|no real employer|no employer names|no internal team|internal figures or internal team names|employer names, internal figures|employer-style wording'
deny=".private/deny-terms.txt"
self='scripts/confidentiality-check.sh'
blocked=0
report() { echo "confidentiality check: BLOCKED ($1)"; printf '%s\n' "$2"; blocked=1; }

# Clean copy of the private list: no blank lines (an empty pattern matches
# everything) and no Windows carriage returns (which would match nothing).
terms=""
if [ -s "$deny" ]; then
  terms=$(mktemp)
  trap 'rm -f "$terms"' EXIT
  tr -d '\r' < "$deny" | grep -v -e '^[[:space:]]*$' > "$terms" || true
  [ -s "$terms" ] || { rm -f "$terms"; terms=""; }
fi

files=$(git -c core.quotepath=off diff --cached --name-only --diff-filter=ACMR)
bad_types=$(printf '%s\n' "$files" | grep -i -E '\.(xlsx|xls|numbers)$' || true)
[ -n "$bad_types" ] && report "spreadsheet files must be CSV" "$bad_types"
bad_names=$(printf '%s\n' "$files" | grep -i -E "$pattern" || true)
[ -n "$bad_names" ] && report "file name" "$bad_names"
if [ -n "$terms" ] && printf '%s\n' "$files" | grep -q -i -F -f "$terms"; then
  report "a staged file name contains a term from the private list" "(name withheld)"
fi

while IFS= read -r f; do
  [ -z "$f" ] && continue
  [ "$f" = "$self" ] && continue
  # Added lines: every "+" line after the first hunk header, so a line that
  # itself starts with "++" is still scanned.
  added=$(git diff --cached -U0 --no-color -- "$f" | awk '/^@@/{h=1; next} h && /^\+/{print}' || true)
  [ -z "$added" ] && continue
  hits=$(printf '%s\n' "$added" | grep -i -E "$pattern" || true)
  case "$f" in
    CLAUDE.md|README.md|docs/*|specs/*) hits=$(printf '%s\n' "$hits" | grep -v -i -E "$rule_text" || true) ;;
  esac
  [ -n "$hits" ] && report "$f" "$hits"
  if [ -n "$terms" ]; then
    priv=$(printf '%s\n' "$added" | grep -i -F -f "$terms" || true)
    [ -n "$priv" ] && report "$f: a term from the private list" "(line withheld; the term is on your private list)"
  fi
done <<EOF_FILES
$files
EOF_FILES

if [ "$blocked" -eq 1 ]; then exit 1; fi
echo "confidentiality check: clean"; exit 0
