# A290 Wiki favicon/search-result icon update

## Goal
Make Google/search result snippets for `a290.wiki` more likely to show a small branded site icon next to the site name/URL.

## Context
The site currently has `/images/favicon.svg` linked as an SVG favicon. Google Search often prefers crawlable square PNG/ICO favicon assets and may ignore/lag SVG-only favicons. The screenshot from Rich shows the search result header area where the favicon/site icon should appear.

## Requirements
- Keep the existing visual identity: blue background, white circular mark, `a290` text.
- Add PNG favicon assets in standard sizes, at minimum 48x48 and 192x192.
- Add `/favicon.ico` or equivalent fallback at the site root.
- Update the home page `<head>` to include standard favicon links:
  - `rel="icon"` for ICO fallback
  - `rel="icon" type="image/png" sizes="48x48"`
  - `rel="icon" type="image/png" sizes="192x192"`
  - keep SVG where useful
  - optional `apple-touch-icon`
- Fix any obviously malformed metadata in the head while touching it, without changing page content.
- Do not add external dependencies.

## Verification
- Files exist and are valid images.
- `index.html` head contains favicon links.
- Local git diff is cleanly reviewable.
- No deployment unless explicitly requested.
