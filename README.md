# syslinuxos-conky-ring

Ring-style Conky theme for [SysLinuxOS](https://syslinuxos.com) with **automatic resolution scaling**.

Displays CPU, RAM, disks, network, clock and battery as animated rings drawn via Cairo.

## Credits / License

Fork of **Auzia Conky** by **Zineddine SAIBI** (GPL-3.0,
<https://github.com/SZinedine/auzia-conky>), itself based on the
**Namoudaj Conky** template by the same author.
The drawing code (`abstract.lua`, `colors.lua`, `rc/gauge.lua`, `start.lua`)
remains the work of Zineddine SAIBI.

Fork, auto-scaling and Debian packaging for SysLinuxOS by:

- **Franco Conidi** (aka *edmond*) — <fconidi@gmail.com>
- <https://syslinuxos.com> — <https://francoconidi.it>

Distributed under **GPL-3.0**, same as upstream. See `files/opt/Sys-ring-conky/LICENSE`.

## Features added over upstream

- **Auto-scaling** — `rc/scale.lua` detects the primary display resolution via
  `xrandr` (fallback: `xdpyinfo`) and computes:

  ```
  scale = min(width/1920, height/1080)   # clamped 0.5 .. 3.0
  ```

  `cairo_scale(cr, scale, scale)` is applied once in `start.lua`; every ring,
  stroke width, text position and font size scales uniformly.
  At 1920×1080 `scale = 1.0` — identical to the original layout.
  Override at any time with `CONKY_RING_SCALE=<n>`.

- **Accurate CPU temperature** — `cpu_temperature()` in `abstract.lua` reads
  `coretemp` (Intel `Package id 0`) or `k10temp` (AMD `Tctl`/`Tdie`) via
  `sensors`, falling back to `acpitemp` when `lm-sensors` is not available.

- **Auto-detected CPU core/thread count** — `check_cpu.service` runs
  `check_cpu.sh` at boot (and on install) to write the correct `cpu_cores`
  and active `net_interface` into `settings.lua`.

- **No-battery safeguard** — on computers without a battery the battery
  ring is suppressed (no misleading "100%" from an AC adapter).

- **Desktop menu integration** — `System Tools > Conky > Start Ring / Stop Ring` (localized when available).

## Installation

### Via SysLinuxOS APT repository (recommended)

```bash
curl -fsSL https://fconidi.github.io/SysLinuxOS-Tools/client/install-repo.sh | sudo bash
sudo apt install syslinuxos-conky-ring
```

### Direct .deb download

Download the latest `.deb` from [Releases](../../releases/latest) and install:

```bash
sudo apt install ./syslinuxos-conky-ring_<version>_all.deb
```

If the SysLinuxOS APT repository is not configured, also download and install
`syslinuxos-conky-menu` from the [Conky Window repository](https://github.com/fconidi/syslinuxos-conky-window).

When upgrading a downloaded package from the previous name, install both
`syslinuxos-conky-ring` and the transitional `syslinuxos-ring-conky` package
together so APT can complete the migration.

### Build from source

```bash
sudo apt install fakeroot dpkg-dev
git clone https://github.com/fconidi/syslinuxos-conky-ring.git
cd syslinuxos-conky-ring
bash build-deb.sh
bash build-transitional.sh
sudo apt install ./syslinuxos-conky-ring_*.deb ./syslinuxos-ring-conky_*.deb
```

## Dependencies

- `syslinuxos-conky-menu` (shared **System Tools > Conky** submenu)
- `conky-all`
- `x11-xserver-utils` (xrandr)
- `x11-utils` (xdpyinfo — optional fallback)
- `lm-sensors` (optional, for accurate CPU temperature)

## Files installed

| Path | Description |
|------|-------------|
| `/opt/Sys-ring-conky/` | Theme files (conkyrc, \*.lua, rc/) |
| `/opt/scripts/conky-ring-start.sh` | Start script |
| `/opt/scripts/conky-ring-stop.sh` | Stop script |
| `/opt/scripts/check_cpu.sh` | CPU/net detection script |
| `/lib/systemd/system/check_cpu.service` | Boot-time detection unit |

## Usage

```
Menu → System Tools → Conky → Start Ring   # start
Menu → System Tools → Conky → Stop Ring    # stop
```

Force a specific scale factor without changing resolution:

```bash
CONKY_RING_SCALE=1.5 /opt/scripts/conky-ring-start.sh
```

## Previous package name

The old `syslinuxos-ring-conky` package is retained as a transitional package.
An APT upgrade installs `syslinuxos-conky-ring` automatically. Existing theme
settings are preserved, and the start/stop script paths remain available.

Build the compatibility package with `bash build-transitional.sh`.
