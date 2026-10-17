# Printable circle prospecting call sheet

`circle-prospecting-call-sheet.pdf` is the buyer-facing, two-page asset, published with its landing page `index.html` at `/resources/circle-prospecting-call-sheet/`. The circle prospecting guide (`blog/circle-prospecting-scripts.html`) remains the accessible HTML source and is linked inside the PDF.

The PDF uses the four event scripts (just listed, open house, under contract, just sold), the between-listings market-update script and the four objection responses verbatim from `blog/circle-prospecting-scripts.html`. The selection, print layout, ring log and source/app links are new; the underlying scripts were already written and reviewed.

## Build and verify

With the dependencies in `scripts/requirements-marketing-assets.txt` available:

```sh
python3 scripts/generate-circle-call-sheet.py
python3 scripts/generate-circle-call-sheet.py --check
python3 scripts/test-circle-call-sheet.py
node scripts/generate-privacy.mjs --check
```

The generator reads the reviewed HTML without modifying it and maps each script block to its nearest h2/h3 heading (the market-update script sits under an h2). Output is deterministic; `--check` detects a stale PDF after source or layout changes. Editing a quoted script in the guide means regenerating the PDF.

The file adds no forms, scripts, pricing claims or tracking. Its App Store link uses the campaign token `resource-circle-call-sheet`, shared with the landing page. The PDF is text-selectable; it is not a fully tagged PDF/UA document. Readers can use the linked HTML guide for an accessible equivalent of the quoted scripts.

Print reliability: the PDF embeds ReportLab's bundled Bitstream Vera regular/bold fonts. Its permission/copyright notice is included in `FONT_LICENSE.txt` and attached inside the PDF, and a readable source URL remains on paper copies.
