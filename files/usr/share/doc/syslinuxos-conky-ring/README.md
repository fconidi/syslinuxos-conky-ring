# syslinuxos-conky-ring

Tema Conky "ad anelli" di SysLinuxOS con **auto-scaling in base alla
risoluzione dello schermo**.

## Crediti / licenza

Fork di **Auzia Conky** di **Zineddine SAIBI** (GPL-3.0,
<https://github.com/SZinedine/auzia-conky>), a sua volta basato sul template
**Namoudaj Conky** dello stesso autore. Il codice di disegno (`abstract.lua`,
`colors.lua`, `rc/gauge.lua`, `start.lua`) resta opera di Zineddine SAIBI.

Fork, auto-scaling e packaging per SysLinuxOS a cura di:

- **Franco Conidi** (aka *edmond*) — <fconidi@gmail.com>
- <https://syslinuxos.com>
- <https://francoconidi.it>

Distribuito sotto **GPL-3.0**, come l'upstream. Vedi `LICENSE`.

## Cosa fa

La sezione Internet mostra sempre IP esterno e ISP. Il recupero HTTPS avviene
in background: IP aggiornato ogni cinque minuti, ISP ogni ora. Durante
un'interruzione di rete resta visibile l'ultimo valore disponibile.

Il tema e' autorato per una finestra di 1240x720 su schermo 1920x1080, con
coordinate/raggi/font assoluti. Per supportare risoluzioni diverse senza
ridisegnare tutto, `rc/scale.lua` rileva la risoluzione (xrandr, fallback
xdpyinfo) e calcola:

    scale = min(larghezza/1920, altezza/1080)   # clamp 0.5 .. 3.0

- `conkyrc` dimensiona la finestra (`minimum_width/height`, `gap_y`) con `scale`.
- `start.lua` applica `cairo_scale(cr, scale, scale)`: anelli, spessori,
  posizioni del testo e font scalano in modo uniforme.

A 1920x1080 `scale = 1.0`, quindi il layout e' identico all'originale.

## File

- `/usr/share/conky/syslinuxos-ring/`        tema (conkyrc, *.lua, rc/scale.lua, rc/gauge.lua)
- `/usr/bin/conky-ring-start.sh` / `conky-ring-stop.sh`  avvio/arresto
- `/usr/lib/syslinuxos-conky-ring/check_cpu.sh`   imposta `cpu_cores` in settings.lua
- `/lib/systemd/system/check_cpu.service`  esegue check_cpu.sh al boot
- voci di menu: System Tools > Conky (Start Conky-Ring / Stop Conky-Ring)

## Uso

    Menu  ->  System Tools  ->  Conky  ->  Start Conky-Ring   # avvia
    Menu  ->  System Tools  ->  Conky  ->  Stop Conky-Ring    # arresta

## Dipendenze

syslinuxos-conky-menu, conky-all, x11-xserver-utils (xrandr), python3.
x11-utils (xdpyinfo) come fallback.
