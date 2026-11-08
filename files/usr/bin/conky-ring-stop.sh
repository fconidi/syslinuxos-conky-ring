#!/bin/sh
set -eu
for pid in $(pgrep -x conky 2>/dev/null || true); do
    if [ "$(readlink "/proc/$pid/cwd" 2>/dev/null || true)" = "/usr/share/conky/syslinuxos-ring" ]; then
        kill "$pid" 2>/dev/null || true
    fi
done
