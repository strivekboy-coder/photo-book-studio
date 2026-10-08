# Project and print configuration

The installed skill carries its own runtime. Resolve `scripts/studio.py` relative to the skill directory, not the user's current project. `init` copies the runtime into a new workspace and never overwrites an existing book. Complete the saved brief before calling inventory.

`project/inventory.json` stores the selected source IDs, dimensions after EXIF orientation, capture time and SHA256. Re-importing the same files is idempotent; a filename collision with different bytes fails without replacing an original. HEIC/HEIF needs conversion for the browser first; Pillow may also need an appropriate decoder. JPG/JPEG/PNG/WEBP/GIF/AVIF are the supported inputs; AVIF requires Pillow 11.3+ (standard supported wheels). Nested uploads may use `--recursive`, but duplicate basenames require explicit source-ID handling.

`project/book.json` carries content and layout; read the skill's schema reference. Explicit exclusions or repetitions may use `policy.authorizedOccurrences` (file ID → integer occurrence count), but the agent must record the user's authorization and must not populate this map on its own to make a failing audit pass.

Dimensions are `format.trimWidthMm`, `trimHeightMm`, `bleedMm`, `safeMarginMm`. Coordinate layouts remain subject to visual review after format changes. The main renderer supports arbitrary positive ratios; tested fixtures include square, landscape and portrait. Generalization of aesthetics to real photos still needs examples.

Optional `print` fields:

```json
{
  "pageIncrement": 4,
  "frontPad": true,
  "backPad": true,
  "frontText": "",
  "backText": "",
  "padColor": "#f5f0e7",
  "padInk": "#0b2442",
  "spineWidthMm": null
}
```

The defaults preserve original paired-spread parity by placing a single recto before the first left/right pair. Rear pages fill the requested increment. Confirm increment and blank-page placement with the printer. Covers and separately added endpapers are outside the interior count. A spine is exported only when `cover.spinePath` and the printer-confirmed width are supplied; raster artwork must match the intended ratio, and a PDF spine must match physical dimensions.

The output has MediaBox = trim plus bleed and an explicit TrimBox. Do not fit the entire bleed page into the trim dimensions. Edge extension lives outside the trim and does not enlarge interior photographs. Hardback board wrap, hinges and tolerances are a separate printer operation.

`preflight.json` reports page counts, export resolution, page rotation and small physical text warnings. It always leaves printReady false until a human/agent reviews the exported pixels and the printer-specific cover proof. It does not certify source photo sharpness, safe crops or color matching by itself.

Missing image-generation capabilities are not an installation failure. Use a photo or text cover unless the user wants to wait for another tool; mark generated-art limits honestly. Generate the final cover after the interior story has been reviewed, while planning its needed pixel dimensions at intake.


## Ordinary albums and opt-in Plog

New ordinary albums begin with the fixed intake questionnaire before inventory/layout/generation. Complete process and all questions: [PROCESS.md](PROCESS.md). Plog and scrapbook styling is opt-in; its produced HTML includes the optional local fine-tuning editor. Seven creative treatments are reviewed for new album/Plog sets, without a requirement to use one. Sharing images are PNG/JPG; PDF is only exported when requested. Editing backups are not final deliveries.
