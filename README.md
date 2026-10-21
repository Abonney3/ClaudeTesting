# ClaudeTesting tools

Small single-page browser tools, built to work on a phone.

- Live site: GitHub Pages (enable once: Settings → Pages → Source: **GitHub Actions**). URL: `https://abonney3.github.io/ClaudeTesting/`
- Add a tool: `python3 scripts/new_tool.py my-tool "My Tool"`, edit `tools/my-tool/index.html`, set `status` to `beta` in `tool.json`, run `python3 scripts/build.py`.
- Preview locally: `python3 -m http.server -d dist 8000`.

Agent/contributor details: [AGENTS.md](AGENTS.md).

## Tools
- **Field Units** (`tools/field-units`): oilfield unit converter plus hydrostatic pressure calc.
