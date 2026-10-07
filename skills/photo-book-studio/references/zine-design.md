# Zine design language

Read for a zine request, a relevant visual reference or a substantial zine redesign. Local wording/crop revisions reuse the saved direction. This reference governs ordinary book composition; optional generated-art routes in zine-policy.md are a separate decision. Zine does not require torn paper, texture, stickers or image generation.

## Resolve the direction

If the supplied reference or brief is clear, infer and save the direction. If only “zine” is given, offer a short choice during the existing style question: editorial/minimal, saturated graphic collage, or tactile handmade. Recommend from the actual photographs when asked; do not repeat the intake or require a particular aesthetic. These are useful directions, not an exhaustive definition of zine.

## Principles shared with every style

Compose the event before the template. Identify the focal photograph or phrase, then balance scale, alignment, whitespace and reading order. Choose a small type system and coherent color relationships across neighboring spreads. Design the composition before adding decoration. A blank region can connect two images or create a pause; it is not an invitation to fill it. Preserve every selected source and its meaning, even when a tiny fragment would look stylish.

## Editorial / minimal

- A warm white or clean pale field, sharply distinct image sizes, purposeful whitespace and mostly square-edged photographs.
- Establish a few recurring edges and intervals. An offset detail still shares an edge, axis or spacing relationship with another element. Avoid a scatter of arbitrary centered rectangles.
- A restrained sans-serif can be the primary face. Use clear event phrases, optional short commentary and small factual indexing. Handwriting and serif type are choices, not defaults for every zine.
- Useful compositions: a title with a lower hero opposite an offset pair; a tall hero opposite two separated details; a full-bleed detail opposite an open fragment field; a type-led pause. Adapt to source orientation and story, not a mandatory sequence.
- Small numbering provides continuity, never essential story copy. Make body text readable at actual output size. Avoid using tiny type merely to imitate an editorial reference.

## Saturated graphic collage

- Choose a limited book palette from source colors and intended mood: a bright structural field, a contrasting companion, a dark anchor and a neutral pause. Do not automatically reuse yellow/pink/blue from an example.
- The large color field is part of the hierarchy. Keep photographs legible against it; use a narrow keyline only when it separates the source from the field.
- Pair a hero with an offset group or a calm phrase. Mix dense and spacious regions within the spread. Bright backgrounds do not require every picture to rotate, overlap or have a sticker.
- An oval mask can suit a centered, compact subject with safe surrounding space. Keep hands, bodies and landmarks in rectangles when masking would remove meaning. Preserve the original file and implement masks non-destructively in CSS.
- Use bold display type for one emphasis; repeat quiet metadata consistently. Geometric accents need a source-related or structural role. Allow neutral pages when the palette would compete with the story.

## Tactile handmade

Keep the existing torn-photo, handwriting and source-related illustration approaches available. Use tactile edges to connect or frame content, rather than treating them as proof of zine style. Do not import this texture into the other directions automatically.

## Adapt from a reference

Extract design relationships: focal scale, shape, alignment, palette, type roles and density. Recompose with the new photos; do not copy the reference's coordinates, captions, brand, illustrations or source photographs. When a user requires a specific reference and it cannot be viewed, report that before claiming to match it; honor any explicit stopping instruction.

Keep the layout data in book.json and any necessary styling in the workspace's src/styles.css. The bundled composed layout supports percentage frames and crop positions. Use separate manual notes for equal-level text: caption newlines may shrink later lines. Custom colors, masks and type roles need explicit CSS; never assume an unsupported JSON property works. Override only the intended selectors and inspect browser pixels. Recipes in zine-recipes.json are role-based suggestions, not executable presets.

## Review and learning

First ask whether the composition works without optional decoration. Check the focal hierarchy, relationships between frames, useful whitespace, restrained type roles, palette continuity and whole-book rhythm. Then check faces, crops, contrast, normal-size text and gutter/trim safety. Inspect neighboring spreads and correct visible failures, without enforcing quotas or alternating templates mechanically.

For a new substantial style reference, compare two or three representative spreads before extending the book. To improve this reusable guidance, distinguish a transferable reason from a one-photo coordinate fix. Try the reason on materially different photos before generalizing it. A same-agent adaptation demonstrates a candidate rule; it does not prove independent models or users will reproduce the result.

## Worked studies and provenance

The independent studies use the same 12 authorized stock photos, each exactly once, with different spatial and color systems. Four other photos were used in two additional two-spread adaptation fixtures. All interiors were browser-rendered and visually inspected. Covers were generated after that review. The fictional travel/daily-life stories are demonstration copy.

Public examples: [editorial study](https://strivekboy-coder.github.io/photo-book-studio/showcase/zine-editorial/) and [graphic collage study](https://strivekboy-coder.github.io/photo-book-studio/showcase/zine-collage/).

Visual reference: Flipin's publicly viewable [editorial examples](https://flipin.pages.dev/images/styles/style02all.jpg?v=an7) and [collage examples](https://flipin.pages.dev/images/styles/style01all.jpg?v=an7), reviewed 2026-10-07. No Flipin code, photos, templates or example screenshots are included in this skill. The public links are attribution and optional inspiration; all necessary guidance is above and ships locally.
