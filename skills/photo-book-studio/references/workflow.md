# Production workflow and quality gates

Use the relevant section of this reference. A new book uses the intake and full batch pipeline. An established-book revision skips intake and reads only the applicable revision and visual gates.

## One-time new-book intake

Do not start arranging or generating as soon as a new user uploads photos. Use the complete numbered questionnaire in [intake-questionnaire.md](intake-questionnaire.md). Infer facts already supplied, ask only unresolved items, and keep the separate creative choices visible rather than compressing them into a single permission sentence.

Save the resolved answers to `project/brief.json` before layout begins. Read the brief at the start of every later turn involving this book. Update it whenever the user changes a preference. Run the intake once per new book and again only for an explicitly requested full redesign.

## Batch pipeline

1. For a new book, inventory all selected files, dimensions, orientation, EXIF time, and resolution. For a later batch, inventory only new files and reuse the existing source inventory.
2. Map the user's dated descriptions to files and treat those descriptions as authoritative.
3. Sort chronologically, allowing same-day reordering for visual flow.
4. Group by event and importance. Do not force one day into one spread.
5. Review every image at contact-sheet scale; inspect crop-sensitive and hero images at full resolution.
6. Allocate enough spreads before choosing templates. Prefer another spread over tiny meaningful photographs.
7. Establish focus, scale relationships, alignment, whitespace, typography and palette from the real aspect ratios, faces, gestures, scenery, and visual weight; then choose or adapt layouts. For a zine brief, read zine-design.md once when choosing the direction.
8. Write or polish concise event-level copy. Preserve facts, names, jokes, and emotional meaning.
9. Place text in rendered whitespace with readable contrast and natural line breaks.
10. Add source-related backgrounds, overlaps, and stickers only when they improve hierarchy or story.
11. Finish the normal layout, then review rare candidates under the seven-route creative policy.
12. Store auditable source IDs, generated paths, positions, captions, and provenance in `project/book.json`.
13. Build, render every changed spread in a browser, correct visible failures, and render again.
14. Confirm selected equals placed and omitted equals zero before reporting completion.

## Page-numbered revisions

- Resolve the current viewer page by number, date, captions, and photo IDs before editing.
- Complete local layout and copy changes before insertions, deletions, splits, or merges.
- Perform structural page changes last and remap all later references by event identity.
- Never assume a previous array index still represents the same viewer page.

## Proportional revision mode

- A new batch in an established book reuses the saved brief and cached analysis, inventories only new photos, and reviews changed plus neighboring spreads.
- A local correction reads only the referenced pages and affected assets.
- Do not rerun the full EXIF scan, full contact sheets, or seven-route creative review for a simple text, color, crop, or sticker change.
- Always rebuild once for completeness; render changed spreads only unless page structure changed.

### Fast batch path

When the saved brief is stable and a clear new batch contains roughly forty photos or fewer:

1. Inventory and contact-sheet only the new files.
2. Reuse approved page families and inspect full resolution only for hero, crop-risk, ambiguous, or low-quality images.
3. Assess all seven creative routes and event-linked stickers once. Generate only strong candidates or requested assets; log a concise reason when none is suitable.
4. Apply the entire batch before building.
5. Build once and render the changed spreads together in one browser session where possible.
6. Correct only failures visible in the render, then run the final selected/placed/omitted checks. Defer full print-DPI preflight until the layout is stable or print export is requested.

## Visual gate

Inspect rendered pixels for face and landmark crops, tiny images, accidental black borders, text contrast, orphaned short lines, sticker collisions, excessive overlap, gutter safety, background dominance, and spread-to-spread rhythm. JSON coordinates and automated placement scores are proposals, not proof. Also judge whether each element contributes to mass, flow or hierarchy, whether offset frames share intentional relationships, and whether type/palette support the saved direction.

For a new book, batch or substantial redesign, compare consecutive rendered spreads in groups of roughly four to six. Look for repeated frame silhouettes, backgrounds competing with photographs, decorative art duplicating an adjacent image, and captions that all shrink into bottom annotations. Check whether one intended focus dominates each spread and whether distinct events have an appropriate opening. Change only clear weaknesses; do not add chapter pages, rotate templates, generate art or enforce variety for its own sake. New batches need their changed pages and immediate neighbors; local revisions do not trigger a whole-book review.

## Content invariant

Every manually selected photograph is intentional. Never silently remove, rank out, or omit one. Approved generated replacements must retain the source `file` ID with the derivative in `path`; purely decorative assets use `decorative: true`.

## Identity and revision evidence

Freeze a feedback map (current viewer number → event, side, source IDs) before multi-page corrections. Carry stickers and photo-linked copy with their images when moving them. After structural changes, resolve remaining feedback against that map.

Check source identity, not totals alone: selected and placed must contain the same IDs, each with its authorized occurrence count. Equal counts can hide one missing photo and one duplicate. Check existence of approved derivatives, backgrounds, covers, fonts and audio as well as source photos; decorations never inflate completeness.
