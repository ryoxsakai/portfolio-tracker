# AGENTS.md

## Cursor Cloud specific instructions

This repository is a single, **dependency-free static client-side web app**: a Japanese
investment portfolio tracker. The entire app is `index.html` (HTML + CSS + vanilla JS
inline). There is **no backend, no build step, no package manager, and no tests/linters
configured**. Data is persisted in the browser's `localStorage`.

### Running the app (the only "service")
Serve the repo root over HTTP and open it in a browser:

```
python3 -m http.server 8000
# open http://localhost:8000/index.html
```

There is no hot-reload tooling — development = edit `index.html` and refresh the browser.
`test.html` is a tiny manual JS/localStorage smoke-check page, not a real product.

### Notes / gotchas
- No lint/test/build commands exist anywhere in the repo. Manual browser testing is the
  only verification method.
- Live market data (prices/charts) is fetched at runtime from third-party APIs
  (Yahoo Finance, J-Quants, 投資信託協会) directly from the browser, often via public CORS
  proxies (`corsproxy.io`, `api.allorigins.win`). These require internet access and are
  best-effort; the app's core UI, holdings entry, and persistence all work without them.
- J-Quants is an optional premium price source; a key is entered at runtime via the in-app
  settings modal (none is committed). The app falls back to Yahoo Finance without it.
- To reset app state during testing, run `localStorage.clear()` in the browser console and
  reload.
- `generate_ios_icons.py` is a one-off asset script (needs `pip install Pillow`) used to
  regenerate the already-committed icons in `ios_icons/`. It is not needed at runtime.
