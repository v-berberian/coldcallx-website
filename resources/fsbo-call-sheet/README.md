# Printable FSBO call sheet

`fsbo-call-sheet.pdf` is the buyer-facing, two-page asset, published with its landing page `index.html` at `/resources/fsbo-call-sheet/`. The FSBO scripts guide (`blog/fsbo-scripts.html`) remains the accessible HTML source and is linked inside the PDF; its content is unchanged.

The PDF uses three openers, the day-4 follow-up call and four objection responses verbatim from `blog/fsbo-scripts.html`. The selection, print layout, note worksheet and source/app links are new; the underlying scripts were already written and reviewed.

## Build and verify

With the dependencies in `scripts/requirements-marketing-assets.txt` available:

```sh
python3 scripts/generate-fsbo-call-sheet.py
python3 scripts/generate-fsbo-call-sheet.py --check
python3 scripts/test-fsbo-call-sheet.py
node scripts/generate-privacy.mjs --check
```

The generator reads the reviewed HTML without modifying it. Output is deterministic; `--check` detects a stale PDF after source or layout changes. The committed PDF is served by the existing static deployment without requiring Python on the hosting service.

The file adds no forms, scripts, pricing claims or tracking. Its App Store link uses the campaign token `resource-fsbo-call-sheet`, shared with the landing page. File downloads, outbound links and PDF views are not app installs or purchase attribution. The PDF is text-selectable; it is not a fully tagged PDF/UA document. Readers can use the linked HTML guide for an accessible equivalent of the quoted scripts.

Print reliability: the PDF embeds ReportLab's bundled Bitstream Vera regular/bold fonts. Its permission/copyright notice is included in `FONT_LICENSE.txt` and attached inside the PDF, and a readable source URL remains on paper copies.
