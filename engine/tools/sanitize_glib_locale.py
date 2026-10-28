#!/usr/bin/env python3
"""Avoid embedding the developer's prefix in GLib's Windows locale suffix.

The pinned GLib ggettext.c derives only the final /share/locale suffix on
Windows. This is applied to the generated build configuration, not source.
"""
import argparse
from pathlib import Path
import re

parser = argparse.ArgumentParser()
parser.add_argument('config', type=Path, help='Meson-generated GLib config.h')
args = parser.parse_args()
source = args.config.read_text(encoding='utf-8')
pattern = r'(?m)^#define GLIB_LOCALE_DIR "([^"\r\n]*)"$'
matches = list(re.finditer(pattern, source))
if len(matches) != 1 or not matches[0].group(1).replace('\\', '/').endswith('/share/locale'):
    raise SystemExit('Unexpected GLib locale configuration; no file changed')
updated = re.sub(pattern, '#define GLIB_LOCALE_DIR "/build/share/locale"', source, count=1)
args.config.write_text(updated, encoding='utf-8', newline='')
print('Preserved the Windows /share/locale suffix and removed the build prefix.')
