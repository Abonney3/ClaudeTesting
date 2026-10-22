#!/usr/bin/env python3
"""Validate tools/*/tool.json and build the static site into dist/.

Every tools/<slug>/*.html is a fragment (no doctype/html/head/body); this wraps it.
Usage: python3 scripts/build.py [--check]   (--check = validate only, no output)
"""
import html, json, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOLS, DIST = ROOT / "tools", ROOT / "dist"
STATUSES = {"draft", "beta", "stable"}
REQUIRED = {"title": str, "description": str, "status": str, "tags": list}
FORBIDDEN = ("<!doctype", "<html", "<head>", "<body")

SKELETON = """<!doctype html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<style>:root{{color-scheme:light;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}}
body{{margin:0;font:14px system-ui,sans-serif}}img{{max-width:100%}}[hidden]{{display:none!important}}</style>
</head><body>
{body}
</body></html>
"""


def load_tools():
    tools, errors = [], []
    for d in sorted(p for p in TOOLS.iterdir() if p.is_dir() and not p.name.startswith("_")):
        meta_path, page = d / "tool.json", d / "index.html"
        if not meta_path.exists() or not page.exists():
            errors.append(f"{d.name}: needs tool.json and index.html")
            continue
        try:
            meta = json.loads(meta_path.read_text())
        except json.JSONDecodeError as e:
            errors.append(f"{d.name}/tool.json: {e}")
            continue
        for key, typ in REQUIRED.items():
            if not isinstance(meta.get(key), typ):
                errors.append(f"{d.name}/tool.json: '{key}' must be {typ.__name__}")
        if meta.get("status") not in STATUSES:
            errors.append(f"{d.name}/tool.json: status must be one of {sorted(STATUSES)}")
        for f in sorted(d.glob("*.html")):
            src = f.read_text()
            if any(tag in src[:2000].lower() for tag in FORBIDDEN):
                errors.append(f"{d.name}/{f.name}: must be a fragment (no doctype/html/head/body)")
            if "<title>" not in src[:8192]:
                errors.append(f"{d.name}/{f.name}: needs <title> near the top")
        tools.append((d, meta))
    return tools, errors


def card(slug, meta):
    e = html.escape
    tags = " · ".join([meta["status"], *meta["tags"]])
    return (f'<a class="tool" href="{e(slug)}/"><strong>{e(meta["title"])}</strong>'
            f'<span>{e(meta["description"])}</span><span class="tag">{e(tags)}</span></a>')


def build(tools):
    shutil.rmtree(DIST, ignore_errors=True)
    for d, meta in tools:
        if meta["status"] == "draft":
            continue
        out = DIST / d.name
        shutil.copytree(d, out, ignore=shutil.ignore_patterns("tool.json", "README.md"))
        for f in d.glob("*.html"):
            (out / f.name).write_text(SKELETON.format(body=f.read_text()))
    listed = [(d, m) for d, m in tools if m["status"] != "draft"]
    home = (ROOT / "site" / "home.html").read_text()
    home = home.replace("<!--TOOLS-->", "\n".join(card(d.name, m) for d, m in listed))
    (DIST / "index.html").write_text(SKELETON.format(body=home))
    (DIST / "tools.json").write_text(json.dumps({d.name: m for d, m in listed}, indent=2))
    print(f"built {len(listed)} tool(s) -> {DIST.relative_to(ROOT)}/")


if __name__ == "__main__":
    tools, errors = load_tools()
    if errors:
        print("\n".join("ERROR " + e for e in errors), file=sys.stderr)
        sys.exit(1)
    if "--check" in sys.argv:
        print(f"ok: {len(tools)} tool(s)")
    else:
        build(tools)
