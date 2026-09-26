#!/bin/sh
# Reproduce every number in PAPER.md.  Pure CPU, no GPU, no network, ~1 minute.
set -e
for s in fano.py associator.py closure.py cqft.py hardware.py; do
    printf '\n########## %s ##########\n\n' "$s"
    python3 "$s"
done
