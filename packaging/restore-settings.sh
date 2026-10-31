#!/bin/sh
set -e

if [ -f /var/lib/syslinuxos-conky-ring/legacy-settings.lua ]; then
    install -m 644 /var/lib/syslinuxos-conky-ring/legacy-settings.lua \
        /opt/Sys-ring-conky/settings.lua
    rm -f /var/lib/syslinuxos-conky-ring/legacy-settings.lua
    rmdir /var/lib/syslinuxos-conky-ring 2>/dev/null || true
fi
