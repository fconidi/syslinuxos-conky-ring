#!/bin/bash
# Build the compatibility package for the previous APT package name.
set -euo pipefail
PKG_NAME=syslinuxos-ring-conky
PKG_VERSION=0.2.0
WORKDIR="$(cd "$(dirname "$0")" && pwd)"
STAGING="$(mktemp -d)"
chmod 755 "$STAGING"
trap 'rm -rf "$STAGING"' EXIT
mkdir -p "$STAGING/DEBIAN"
cp "$WORKDIR/packaging/preinst" "$STAGING/DEBIAN/preinst"
chmod 755 "$STAGING/DEBIAN/preinst"
cat > "$STAGING/DEBIAN/control" <<CONTROL
Package: $PKG_NAME
Version: $PKG_VERSION
Section: oldlibs
Priority: optional
Architecture: all
Depends: syslinuxos-conky-ring (>= $PKG_VERSION)
Maintainer: Franco Conidi <fconidi@gmail.com>
Homepage: https://github.com/fconidi/syslinuxos-conky-ring
Installed-Size: 1
Description: transitional package for syslinuxos-conky-ring
 Installs the renamed SysLinuxOS Conky Ring package.
 This compatibility package can be removed after the upgrade.
CONTROL
dpkg-deb --root-owner-group --build "$STAGING" "$WORKDIR/${PKG_NAME}_${PKG_VERSION}_all.deb"
