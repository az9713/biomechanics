# Shipping: live page + README + GitHub

Only do this when the user asks to publish. Confirm before creating a public repo
or enabling Pages (it publishes the content).

## Make it render live (GitHub Pages)
1. The doc is a self-contained HTML file, so Pages serves it as-is.
2. Add an `index.html` redirect so the Pages root opens the tutorial:
   ```html
   <!doctype html><html lang="en"><head><meta charset="utf-8">
   <meta http-equiv="refresh" content="0; url=DOC.html">
   <link rel="canonical" href="DOC.html"></head>
   <body><a href="DOC.html">Open the tutorial →</a></body></html>
   ```
3. Enable Pages on `main`/root (after the first push):
   ```bash
   gh api -X POST repos/OWNER/REPO/pages -f "source[branch]=main" -f "source[path]=/"
   ```
   Live at `https://OWNER.github.io/REPO/`. Build status:
   `gh api repos/OWNER/REPO/pages/builds/latest --jq .status`

## README: you cannot embed live HTML or an MP4 player
GitHub Markdown sanitizes iframes/scripts and won't play a committed MP4 inline.
The idiom that works:
- **Clickable preview screenshot → live page** (this is how to "render the page"
  in a README):
  ```bash
  python scripts/shoot.py https://OWNER.github.io/REPO/DOC.html preview.png --size 1280x820
  ```
  ```markdown
  [![preview](preview.png)](https://OWNER.github.io/REPO/)
  ```
- **GIF for motion** (Markdown renders `![](clip.gif)`); link the MP4 for full quality.
- **Unicode math** in the README body (see gotcha #3), not `$…$`.

## Commit only deliverables
`.gitignore`:
```
node_modules/
remotion/node_modules/
*.bak
# (your local screenshots / drafts folder)
```
Stage the HTML, README, `index.html`, preview image, gif/mp4, and any Remotion
source — not `node_modules`, scratch scripts, or working screenshots.

## Repo + push (gh CLI)
```bash
gh auth status                                  # confirm logged in
git init -b main && git add . && git commit -m "..."
gh repo create OWNER/REPO --public --source=. --remote=origin --push --description "..."
```
- Media push (gif+mp4) can exceed a 2-min foreground limit — push in the
  background if it times out, then verify: `git ls-remote --heads origin`.
- Set the homepage: `gh repo edit OWNER/REPO --homepage https://OWNER.github.io/REPO/`.

## Verify the live site
```bash
curl -s -o /dev/null -w "%{http_code}\n" https://OWNER.github.io/REPO/DOC.html   # expect 200
python scripts/verify_dom.py https://OWNER.github.io/REPO/DOC.html               # 0 mjx-merror, links OK
```

Commit-message trailers (per this environment's convention):
```
Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>
Claude-Session: <session url>
```
