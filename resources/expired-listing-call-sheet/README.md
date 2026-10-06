# Printable expired-listing call sheet

`expired-listing-call-sheet.pdf` is the buyer-facing, two-page asset. It is downloadable from one additive blog-index card. The existing expired-listing guide remains the accessible HTML source and is linked inside the PDF; its content and experiment are unchanged.

The PDF uses three openers and four objection responses verbatim from `blog/expired-listing-scripts.html`. The secondary marketing agent produced the selection, print layout, note worksheet and source/app links; the underlying scripts were already written and reviewed by the primary program.

## Build and verify

With the dependencies in `scripts/requirements-marketing-assets.txt` available:

```sh
python3 scripts/generate-expired-call-sheet.py
python3 scripts/generate-expired-call-sheet.py --check
python3 scripts/test-expired-call-sheet.py
node scripts/generate-privacy.mjs --check
```

The generator reads the reviewed HTML without modifying it. Output is deterministic; `--check` detects a stale PDF after source or layout changes. The committed PDF is served by the existing static deployment without requiring Python on the hosting service.

The file adds no forms, scripts, pricing claims or tracking. Its App Store link reuses the source guide's existing campaign parameters. File downloads, outbound links and PDF views are not app installs or purchase attribution. The PDF is text-selectable; it is not a fully tagged PDF/UA document. Readers can use the linked HTML guide for an accessible equivalent of the quoted scripts.

Print reliability: the PDF embeds ReportLab’s bundled Bitstream Vera regular/bold fonts. Its permission/copyright notice is included in `FONT_LICENSE.txt` and attached inside the PDF, and a readable source URL remains on paper copies. No new font or rendering software was installed.
