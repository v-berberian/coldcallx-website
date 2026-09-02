# ColdCallX video (Remotion)

Programmatic video for marketing assets, built with [Remotion](https://remotion.dev).
This folder is self-contained and is not part of the static site published to GitHub Pages.

## Setup

```bash
cd video
npm install
```

## Studio

```bash
npm run dev
```

Opens the Remotion Studio at http://localhost:3000 to preview and tweak props live.

## Render

```bash
npm run render          # -> out/promo.mp4
```

## Compositions

- `Promo` (1920x1080, 30fps, 5s) — title/subtitle intro card. Props are
  validated with a Zod schema, so they're editable in the Studio sidebar.

## Chromium note

Remotion downloads its own Chrome Headless Shell on first render. If that
download is blocked (restricted network egress), point it at a local Chromium:

```bash
REMOTION_BROWSER_EXECUTABLE=/path/to/chrome npm run render
```

`remotion.config.ts` picks that env var up automatically.
