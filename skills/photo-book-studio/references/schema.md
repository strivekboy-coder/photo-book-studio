# Project contract

`project/book.json` is the source of truth.

`project/brief.json` is the persistent source of truth for user intent and design permissions. Read it before `book.json` work. Each stored preference should include a `value` and `source` of `explicit`, `recommended_accepted`, `inferred`, or `unknown`. Update it in the same turn whenever the user changes a preference.

## Brief fields

- `intakeComplete`: whether the fixed first-use questionnaire has been resolved sufficiently to begin a sample.
- `story`: recipient, subject, date range, purpose, and any title direction.
- `output`: print/web targets, printer, format, orientation, and whether the format is locked.
- `selection`: all-selected requirement, upload strategy, expected photo count, and page-density preference.
- `visual`: style keywords and reference assets.
- `copy`: source policy, language, tone, and permission for agent-written drafts.
- `permissions`: crop, tonal correction, stickers, generated cover, torn-paper treatment, artistic derivatives, derivative replacement, and photo simplification.
- `updatedAt`: ISO timestamp for the latest preference change.

## Book-level fields

- `photoRoot`: project-relative directory containing selected photo copies.
- `policy.allSelectedPhotosRequired`: normally `true`.
- `policy.allowUnusedPhotos`: normally `false`.
- `format`: trim width/height, bleed, safe margin, and lock state.
- `designSystem.rhythm`: intended percentage of editorial, collage, and expressive pages.

## Page fields

- `layout`: concrete CSS layout name.
- `family`: `editorial`, `poem`, `collage`, or `zine`.
- `tone`: optional background color token.
- `photos`: all selected and decorative images used on the page.
- `caption`: page-level copy.
- `captionPlacement`: `auto` searches actual rendered whitespace; `manual` preserves CSS or JSON coordinates.
- `captionPrefer`: optional `top`, `bottom`, `left`, `right`, or a combination such as `bottom-left`.
- `captionDesign`: optional free-position typography settings.
- `notes`: optional array of smaller scattered text fragments; each note can use `placement` and `prefer` with the same rules.

`captionDesign` and each note's `design` may define `x`, `y`, `right`, `bottom`, `width`, `font`, `size`, `color`, `align`, `lineHeight`, `letterSpacing`, `writingMode`, `background`, `padding`, and `rotate`.

Font roles are `poem`, `serif`, `playful`, `sans`, and `latin`.

## Photo fields

- `file`: filename under `photoRoot` for a selected photo.
- `path`: project-relative path for a generated or decorative asset.
- `decorative`: must be `true` for generated art, textures, or ornaments.
- `fit`: `contain` or `cover`.
- `position`: CSS object position used for subject-aware cropping.
- `dateOverride`: ISO date supplied by the user when screenshots, exports, or converted RAW files have misleading or missing EXIF.
- `caption`: optional photo-specific factual note.
- `frame`: optional individually composed frame with percentage `x`, `y`, `width`, `height`, plus `rotate` and `z`; use a renderer layout that supports these fields.

## Required checks

- Every file under `photoRoot` appears in the layout exactly once unless the user explicitly requests repetition.
- Every referenced asset exists.
- Decorative assets are excluded from the selected-photo count.
- Aim for 240–300 effective DPI where practical for print photographs. Review lower resolution at actual placed size; do not shrink or replace intentional photos without considering narrative role and user preference. Include covers and full-page backgrounds, not only photo frames. Report unresolved limits; see [finishing.md](finishing.md).
- Faces and important subjects remain inside the trim-safe area.
- Captions do not cross the gutter or sit inside the trim danger zone.

## Rendered typography

Escape double quotes in generated HTML style attributes so font-family values do not invalidate later color, size, angle, or writing-mode declarations. `captionDesign.wrap: "nowrap"` keeps each explicitly supplied line intact; use only when browser measurement confirms it fits. Keep any orphan protection short, and verify actual line endings rather than treating it as a guarantee. `plainBackground: true` disables the page texture without removing source-derived background art.

### Full-spread photograph background

`spread.backgroundPhoto` stores source `file`, rendered `path`, optional CSS `filter`, `position`, `alt`, and provenance. Keep exactly one non-decorative entry with the same `file` and `backgroundOnly: true` in a page photos array. It is counted as selected content but rendered once by the spread background image, rather than as an additional foreground frame.

`policy.authorizedOccurrences` records explicitly approved exclusions/repetitions by source file ID. Its default is one occurrence per selected file. The build checks each identity, not only totals. `print` controls padding, paper color, page increment and optional confirmed spine width.
