#!/bin/sh
# Installs the confidentiality guard as this repository's git pre-commit hook,
# and creates the owner's private name list if it does not exist.
set -eu
root=$(git rev-parse --show-toplevel)
printf '#!/bin/sh\nexec sh "%s/scripts/confidentiality-check.sh"\n' "$root" > "$root/.git/hooks/pre-commit"
chmod +x "$root/.git/hooks/pre-commit"
mkdir -p "$root/.private"
[ -f "$root/.private/deny-terms.txt" ] || : > "$root/.private/deny-terms.txt"
echo "pre-commit hook installed; private list at .private/deny-terms.txt (one term per line, never committed)"
