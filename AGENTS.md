# AGENTS.md — repo map for agents (terse by design)

PURPOSE: collection of small, self-contained browser tools. Phone-first. No build deps (python3 stdlib only).
BRANCHES: main = default + Pages deploy source. Work on feature branches, merge to main.

LAYOUT
- tools/<slug>/*.html      every page = HTML FRAGMENT (index.html = entry) (no doctype/html/head/body). <title> first. Inline CSS+JS.
- tools/<slug>/tool.json   {title, description, status: draft|beta|stable, tags: []}. draft = not published.
- tools/<slug>/*           extra assets OK; copied to dist (tool.json/README.md excluded).
- tools/_template/         scaffold source. `_`-prefixed dirs ignored by build.
- site/home.html           index fragment; `<!--TOOLS-->` replaced with tool cards.
- scripts/build.py         validate + wrap fragments in skeleton -> dist/. `--check` = validate only.
- scripts/new_tool.py      `python3 scripts/new_tool.py <kebab-slug> "<Title>"`.
- .github/workflows/pages.yml  CI build on every push/PR; deploy dist/ to GitHub Pages from default branch only.

WHY FRAGMENTS: same file publishes as a claude.ai Artifact (host adds skeleton) and as Pages site (build.py adds skeleton). Keep this contract.

TOOL RULES
- Works at 390px width, no horizontal page scroll. Side gutter: padding-left/right max(16px, env(safe-area-inset-*)).
- Colors as :root tokens + dark overrides (prefers-color-scheme guarded by :not([data-theme=light]) AND [data-theme=dark]).
- External: scripts only from cdnjs/jsdelivr/unpkg pinned exact versions; fonts only Google Fonts. No fetch to other hosts.
- localStorage only in try/catch, convenience only. No alert/confirm/prompt.
- Open in a working state (sample values), not empty.

WORKFLOW
1. new_tool.py -> edit index.html -> set status beta -> `python3 scripts/build.py` (must pass).
2. Local view: `python3 -m http.server -d dist 8000`.
3. Phone test: publish fragment as Artifact (fast) or push default branch -> Pages URL.
4. Add row to TOOLS INDEX below.

TOOLS INDEX
| slug | status | summary |
|---|---|---|
| field-units | beta | oilfield unit converter (psi/kPa/MPa, bbl/min, ppg/SG, lb/tonne, ft/m, °F/°C) + hydrostatic P=0.052*ppg*TVD |
| card-courier | beta | magic trick. index=magician panel (setup, QR hand-off -> sms:mine?body=CARD, 4 cue texts via sms: links from magician's own phone). track.html=fake courier page, state in query (s=1-4,k,n,c,t). No server: texts come from magician's number; auto-reply needs SMS backend (e.g. Twilio) = future. Needs Pages host (sms: links unreliable in Artifact). |
