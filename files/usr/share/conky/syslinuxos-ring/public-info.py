#!/usr/bin/python3
"""Refresh the public address and provider shown by Ring."""

import fcntl
import ipaddress
import json
import os
from pathlib import Path
import re
import time
from urllib.request import Request, urlopen


def fetch_url(url):
    try:
        request = Request(url, headers={'User-Agent': 'SysLinuxOS-Conky-Ring/0.2.3'})
        with urlopen(request, timeout=3) as response:
            return response.read(256).decode('utf-8', errors='replace').strip()
    except (OSError, ValueError):
        return ''


def clean_isp(text):
    text = re.sub(r'^AS\d+\s+', '', text.strip())
    text = ' '.join(text.split())
    return ''.join(char for char in text if char.isprintable() and char not in '$\\{}')[:24].strip()


def refresh(path, now=None, fetch=fetch_url):
    now = time.time() if now is None else now
    path.parent.mkdir(parents=True, exist_ok=True)
    metadata = path.with_suffix('.json')
    try:
        state = json.loads(metadata.read_text())
        if not isinstance(state, dict):
            state = {}
    except (OSError, ValueError):
        state = {}

    try:
        ip, isp = path.read_text().splitlines()[:2]
    except (OSError, ValueError):
        ip, isp = 'N/A', 'N/A'

    if now >= state.get('ip_expires', 0):
        try:
            ip = str(ipaddress.IPv4Address(fetch('https://api.ipify.org')))
            delay = 300
        except ValueError:
            delay = 60
        state['ip_expires'] = now + delay

    if now >= state.get('isp_expires', 0):
        value = clean_isp(fetch('https://ipinfo.io/org'))
        if value:
            isp = value
        state['isp_expires'] = now + (3600 if value else 60)

    temporary = path.with_name('.public-info-' + str(os.getpid()))
    temporary.write_text(ip + '\n' + isp + '\n')
    temporary.replace(path)
    temporary_meta = metadata.with_name('.public-info-' + str(os.getpid()) + '.json')
    temporary_meta.write_text(json.dumps(state))
    temporary_meta.replace(metadata)


if __name__ == '__main__':
    cache = Path.home() / '.cache' / 'syslinuxos-conky-ring'
    cache.mkdir(parents=True, exist_ok=True)
    with (cache / 'public-info.lock').open('w') as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            pass
        else:
            refresh(cache / 'public-info')
