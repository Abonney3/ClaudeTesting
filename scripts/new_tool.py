#!/usr/bin/env python3
"""Scaffold a tool from tools/_template. Usage: python3 scripts/new_tool.py <slug> "<Title>" """
import re, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if len(sys.argv) != 3 or not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", sys.argv[1]):
    sys.exit('usage: new_tool.py <kebab-slug> "<Title>"')
slug, title = sys.argv[1], sys.argv[2]
dest = ROOT / "tools" / slug
if dest.exists():
    sys.exit(f"{dest} exists")
shutil.copytree(ROOT / "tools" / "_template", dest)
for f in dest.iterdir():
    f.write_text(f.read_text().replace("TOOL_TITLE", title))
print(f"created tools/{slug}/ (status=draft; set to beta to publish)")
