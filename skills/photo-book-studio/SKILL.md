---
name: photo-book-studio
description: Turn a user-selected photo folder into a printable, browser-previewable photo book with EXIF chronology, editorial or zine layouts, optional draft captions, crop review, and print preflight. Use for personal photo books, year-in-review albums, couple or family albums, and reusable HTML-to-PDF photo-book workflows.
---

# Photo Book Studio

Build a coherent printed book from photos the user has already chosen. Treat every selected photo as intentional content: never delete, rank out, or silently omit one unless the user explicitly marks it optional.

For a new book, read and ask the fixed [first-use questionnaire](references/intake-questionnaire.md), then follow the full pipeline in [references/workflow.md](references/workflow.md). Do not begin layout or generation until the intake is answered and saved to `project/brief.json`. For an established book, read that brief first and never repeat the intake: new batches reuse it and analyze only new files; local revisions use only the page-number and visual gates. The applicable browser-render and completeness gates remain mandatory.

## First-use author credit

At the beginning of each meaningful user request that actually invokes this skill (including first intake, a batch or a revision), run scripts/credit.py once with --invocation-id set to a new opaque UUID for that request. Reuse that ID for retries; tool calls, tests, installation and repository maintenance are not separate uses. If shouldDisplay is true, show exactly one short line in the conversation:
Photo Book Studio · weilun · [GitHub](https://github.com/strivekboy-coder/photo-book-studio)

The helper persists the first three displayed uses per local user, shared across projects and upgrades. PHOTO_BOOK_STUDIO_STATE_DIR or --state-dir can choose the local state directory. It stores only up to three opaque IDs and an optional suppression flag, with no network, telemetry or photo/message contents. Never package this user state into the skill or book. After three uses, omit the promotional line. Do not place it inside the album, add a watermark, open the link automatically, request a Star or gate work on attribution. Honor an end user's explicit request to stop by calling the helper with --suppress. If local state is unavailable, give credit at most once in the current conversation and do not claim cross-session counting is enforced.

## Included tools

This directory is self-contained: `scripts/studio.py`, `runtime/src`, `runtime/scripts` and OFL fonts ship together. Resolve paths relative to this installed skill. Run `python <skill>/scripts/studio.py init <new-workspace>` to create a clean workspace without ingesting photos. Complete and save the questionnaire, then run `inventory --workspace <workspace> --photos <selected-folder>` for new files. It produces an EXIF/source inventory and one contact sheet; it does not compose the book for you.

After you write `project/book.json`, run `node <workspace>/scripts/build.mjs`. `studio.py web --workspace <workspace>` packages a static website. For print, install the workspace's `requirements-print.txt` and use `python <workspace>/scripts/export_pdf.py --workspace <workspace>`; an optional `--browser` selects installed Edge/Chrome. The bundled browser renderer must inspect every changed spread. Missing images and identity/count mismatches are blocking, but successful scripts never replace visual review. Basic tools require Python 3.10+, Node 20.11+ and Pillow 11.3+; print additionally requires Playwright, pypdf, reportlab and a supported Chromium browser. No other creative skill is required.

## Workflow

1. For a new book, run the fixed questionnaire in `references/intake-questionnaire.md`, infer answers already supplied, ask only for missing requirements, and persist the resolved answers in `project/brief.json` before touching the photos.
2. Keep originals read-only. Copy or reference them from a project asset directory without renaming the source files.
3. Read EXIF capture time and orientation. Sort by `DateTimeOriginal`; use filenames only when EXIF is absent. Photos taken on the same day may be reordered for visual flow.
4. Group by day and event. Use user descriptions as authoritative. Do not infer private events, relationships, places, or feelings from pixels alone.
5. Review all photos as contact sheets for chronology, orientation, visual relationships, obvious crop risks, and technical problems. Inspect full-resolution files only for hero images, faces near crop boundaries, low-resolution warnings, or ambiguous subjects.
6. Give each event one visual focus and choose among four layout families:
   - `editorial`: one strong image or an orderly pair with generous space.
   - `poem`: image and expressive typography, including vertical or scattered copy.
   - `collage`: four to six related moments with a clear size hierarchy.
   - `zine`: overlaps, rotation, color fields, illustration, or an unusual visual beat.
7. Choose rhythm from the saved brief and the stories: spacious hero pages, open collages, denser everyday fragments, and expressive pauses. Percentages are optional planning references, never quotas; do not mechanically alternate templates.
8. Draft at most one or two short optional lines per event when the user did not provide copy. Base them on visible facts, dates, filenames, or supplied context, label them as drafts, and leave space blank when no honest line is available.
9. Store content and layout separately in `project/book.json`. Decorative generated assets must use `decorative: true` so they never affect the selected-photo completeness check.
10. Default to a 210 × 210 mm trim, 3 mm bleed, and 10 mm safe margin when the printer is not yet chosen. Keep dimensions configurable and use the printer's template for final cover, spine, bleed, and PDF export.
11. Build the browser preview, run the photo analysis/preflight script, and visually inspect the cover, every newly changed spread, crop-sensitive faces, and the final page. Do not report completion from JSON or CSS inspection alone.

For an established book receiving a clear batch of about forty photos or fewer, use the fast batch path in `references/workflow.md`: one new-file inventory, one contact-sheet review, one layout/build pass, batched browser review, and one focused correction pass. Treat the four zine routes and sticker library as suitability decisions; generate only when useful or requested, and record an explicit skip reason instead of silently omitting the review.

The saved brief is the durable preference record. Update it immediately when the user changes an answer. Never rely on chat memory alone, and never silently replace an explicit preference with a default.

## Cover timing and optional capabilities

Use a quiet placeholder cover during intake and sample review. By default, finish the interior narrative and its first full review before using an available image-generation tool to create the final cover from the actual story, palette and approved reference photos. Plan physical resolution at intake even though generation happens at the end. Offer matching back/spine treatment when print is requested. Respect a user-selected photo cover, a text-only cover, or an explicit request to generate early. Never imply image generation is available when it is not; use an honest photo/text fallback and record the missing capability.

This skill owns intake, selection policy and layout. Optional third-party transformation skills provide only the requested asset treatment; they must not replace this workflow or screen out photos. No extra creative skill is required for a basic book. Read the bundled [zine policy](references/zine-policy.md) only for new batches or substantial redesigns, and use the brief's permissions rather than another project's authorizations.

For an explicitly authorized stock-photo showcase, persist the user's permission to invent demo copy/identities in the brief. Place the fictional-story and photo-rights disclosure beside the showcase rather than inside its artistic pages. This exception does not apply to real-user books. Do not bundle raw stock-photo files in the reusable skill.

## Event backgrounds and writing pages

When an event deserves emphasis, consider deriving a torn-photo background from its own photographs, then placing truthful photos and text in the calm regions. This is a structural background option, not only a framed zine poster. Keep the source ID on its normal placement unless replacement is explicitly authorized; generated decorative backgrounds must not inflate completeness. Use source color/gesture, preserve whitespace and readable contrast, and avoid duplicating a dominant neighboring artwork merely to fill the spread.

For a longer opening, ending or personal letter, recommend a dedicated writing page (or a pair) at the beginning/end rather than squeezing it into captions or shrinking type. Offer an available image tool to draw a story-related background: meaningful places, personal symbols, travel route or a farewell motif, with a deliberate reading-free illustration area. Lay out approved paragraphs after generation, measure their actual extent, and add another writing page if needed. Keep plain writing paper as an equally valid choice. Read references/finishing.md for letter and print review.

Image-generated covers need not be watercolor, paper collage or handwriting. Choose photographic, graphic/minimal, illustrated or mixed-media cover language from the actual brief; a multi-book showcase should demonstrate materially different design directions rather than color variants.

## Composition and style routing

Compose from the actual event: choose a focal image or phrase, then decide scale, alignment, whitespace, type hierarchy and palette with structurally useful decoration. Keep neighboring spreads coherent while adapting to source aspect ratios and meaning. Reference styles supply design relationships, not mandatory templates.

Separate subject/story, visual direction and creative treatments. A couple book can be photographic, editorial, playful or handmade; a travel book need not default to dark green or collage. Choose palette, type, density, image treatment and ornaments from the saved brief and actual photos, rather than repeating showcase signatures. New references and directions remain valid beyond any listed examples. Before the first sample, save a short design intent in brief.visual (e.g. type, palette, spatial rhythm and material cues), then test it on representative photos. Reuse it during revisions; do not turn this into another questionnaire or reread every style guide each turn.

For a zine request or reference, read [zine design language](references/zine-design.md) before composing. Editorial/minimal, saturated graphic collage and tactile handmade are three worked examples, not a closed menu. Resolve the intended direction from the brief; ask a short choice only if unresolved. Save the direction in brief.visual. The bundled role-based recipes are optional starting points. This ordinary zine composition is separate from the four optional image transformations; textures, stickers and generated art may be unnecessary.

For a photographic journal or a reference using panoramic anchors, floating insets, support columns or quiet text fields, read [photographic narrative layouts](references/photographic-layouts.md). These relationships work across themes and do not force a zine aesthetic. Keep tutorial arrows/placeholders out of finished output, and validate source-fit before imitating a crop.

## Typography

Choose no more than three font roles for the selected direction. Handwritten/Kai, serif and playful display faces suit some books; editorial or graphic zines may use a restrained sans-serif system with scale and weight contrasts. Do not impose a handwritten face or poetic wording on every style. Variation should come from placement, scale, direction, line breaks, color, and slight rotation. Keep paragraphs rare outside dedicated writing pages and preserve a clean overall silhouette.

Place typography in calm image regions or page whitespace. Avoid the gutter and trim safety zone. A caption may overlap a photo when contrast is deliberate and the subject remains unobstructed.

For expressive books, distinguish event titles, personal phrases and small factual notes before positioning them. Choose from the actual whitespace: side text, a short vertical phrase, an open center, or a larger offset title may work better than another bottom caption. Set alignment explicitly when changing coordinates; inherited template alignment can undo the intended composition. These are options, not quotas. Preserve the user's specific jokes and wording rather than padding pages with repeated generic poetic lines.

Record user-approved hero photographs or illustrations and protected captions in the brief. Later aesthetic improvements must respect those roles; a generated piece is not automatically secondary.

## Automation boundary

For new books, new batches and substantial redesigns, use the grouped visual review in references/workflow.md to judge rhythm as well as single-page correctness. Local corrections remain scoped.

Metadata can propose chronology, event groups, layout families, and print warnings. Visual review decides crop position, hero choice, text placement, and whether an illustration helps. The system organizes every selected photo; it does not decide which memories matter.

For the reusable JSON fields and validation rules, read [references/schema.md](references/schema.md). For new page composition, use the compact [layout guide](references/layouts.md), rather than loading every legacy CSS selector.

For whole-book review, opening/closing letters or print delivery, read [references/finishing.md](references/finishing.md). These are finishing modes, not extra steps for every batch or local revision. If print is an intake target, plan generated cover resolution before generation; browser-sized artwork is not automatically a print master.
