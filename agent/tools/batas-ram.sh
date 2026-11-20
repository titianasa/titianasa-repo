#!/usr/bin/env bash
# Runs a command in its own memory-capped scope, so a runaway process (next dev, tsc, a big bun script) is killed alone
# instead of the OOM killer taking the whole terminal, the Claude session and its agents with it (2026-11-19).
#   agent/tools/batas-ram.sh 3G bunx tsc --noEmit -p .
#   agent/tools/batas-ram.sh 5G bun --bun next dev --webpack -p 3000
set -euo pipefail
max="$1"; shift
exec systemd-run --user --scope --quiet --same-dir -p MemoryMax="$max" -p MemorySwapMax=512M -- "$@"
