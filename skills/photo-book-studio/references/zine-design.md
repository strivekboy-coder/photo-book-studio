# Zine design language

Read for a zine request, a relevant visual reference or a substantial zine redesign. Local wording/crop revisions reuse the saved direction. This reference governs ordinary book composition; optional generated-art routes in zine-policy.md are a separate decision. Zine does not require torn paper, texture, stickers or image generation.

## Resolve the direction

If the supplied reference or brief is clear, infer and save the direction. If only “zine” is given, offer a short choice during the existing style question: editorial/minimal, saturated graphic collage, or tactile handmade. Recommend from the actual photographs when asked; do not repeat the intake or require a particular aesthetic. These are useful directions, not an exhaustive definition of zine.

## Principles shared with every style

Compose the event before the template. Identify the focal photograph or phrase, then balance scale, alignment, whitespace and reading order. Choose a small type system and coherent color relationships across neighboring spreads. Choose decoration together with the composition when it frames, connects, interrupts or sets rhythm; optional ornaments may be decided later. A blank region can connect two images or create a pause; it is not an invitation to fill it. Preserve every selected source and its meaning, even when a tiny fragment would look stylish.

## Editorial / minimal

- A warm white or clean pale field, sharply distinct image sizes, purposeful whitespace and mostly square-edged photographs.
- Establish a few recurring edges and intervals. An offset detail can share an edge, axis, varying interval or color relationship with another element. Controlled irregularity can organize a loose field around a center of gravity rather than a common straight edge.
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

Build a tactile language from the story: warm or cool paper, layered photographs, gentle offsets, selected fibrous edges, handwritten observations and source-linked ornaments. Use a few recurring material cues for continuity rather than applying tape/shadows to every photograph. Contrast a large sincere image with smaller collected fragments; leave paper visible between clusters. Borders and underprints should connect content or imply a memory insert, not hide faces or shrink every image.

Readable handwriting can carry personal remarks; dates and supporting facts may use quiet sans/serif type. Stickers should touch or relate to a group, phrase or margin rhythm. Match cat/coffee/wave/transport motifs to their actual event. CSS masks are non-destructive and require subject-safe edge review. A paper effect does not require a generated derivative; use the seven creative routes independently when a strong candidate warrants one.

## Spatial and decorative operations

Choose an operation for its narrative or visual job, then choose the motif. A star border is one instance of perimeter rhythm, not a default zine accessory. Related alternatives include dot/dash stitching, leaves around a garden memory, postage marks around a travel insert, waves guiding river photos, ticket fragments linking a journey, and bright underlines or blocks joining text. Use geometric CSS/SVG for simple native marks; use image tools for requested illustrated assets.

- **Loose fragment field:** vary size and position around a clear visual center. Balance mass and gaps, retain a few relationships, and let an offset fragment interrupt the grid deliberately. Not every frame needs a shared edge or uniform gap.
- **Photographs in a sentence:** images function as words, pauses or emphasis within large type. Build the reading sequence with actual text and image extents. Favor details that survive a short strip; keep faces/meaningful interactions in larger frames. Do not take a full-page screenshot as the only editable source.
- **Dense contact sheet or visual receipt:** repeat slots, thin dividers, index marks or row bands to make a cohesive field. Modulate one size or one gap to avoid a lifeless grid. Density is a valid beat, not a fault by itself; essential subjects must still read at the intended output size.
- **Silhouette group:** arrange multiple photographs into an implied heart, arc, diagonal or other meaningful silhouette. Favor the group's outline and clear subjects over a destructive per-photo mask. Important portraits remain large elsewhere only when duplication is explicitly allowed; otherwise design the group to keep them legible or choose another operation.
- **Screen-like or scrapbook stack:** use panels, small headers, overlapping edges, a deliberate cursor/selection-like accent or ticket layers to create a collected-memory feeling. Do not invent real chats, device metadata or private messages. Keep the motif subordinate to truthful content.
- **Ornament topology:** marks can run around the perimeter, orbit a subject, bridge frames, punctuate a phrase, fill an intentional patterned field or create a recurring rhythm. Decide where the eye should travel before selecting stars/flowers/dots/tape. Match scale, density, color and continuity to the photos; protect faces and readable copy.

Consider these operations when the brief/reference supports them; do not add all of them to every book or enforce a creativity quota. A plain spread and an expressive spread can belong to the same book. Audit whether the result has deliberate mass, flow, hierarchy and readable subjects, not whether it is regular or irregular.

## Adapt from a reference

Extract design relationships: focal scale, shape, alignment, palette, type roles and density. Recompose with the new photos; do not copy the reference's coordinates, captions, brand, illustrations or source photographs. When a user requires a specific reference and it cannot be viewed, report that before claiming to match it; honor any explicit stopping instruction.

Keep the layout data in book.json and any necessary styling in the workspace's src/styles.css. The bundled composed layout supports percentage frames and crop positions. Use separate manual notes for equal-level text: caption newlines may shrink later lines. Custom colors, masks and type roles need explicit CSS; never assume an unsupported JSON property works. Override only the intended selectors and inspect browser pixels. Recipes in zine-recipes.json are role-based suggestions, not executable presets.

## Review and learning

First ask how each element participates in the composition. Remove redundant decoration, but do not strip away structural ornaments just to satisfy a decoration-free test. Check the focal hierarchy, relationships between frames, useful whitespace, restrained type roles, palette continuity and whole-book rhythm. Then check faces, crops, contrast, normal-size text and gutter/trim safety. Inspect neighboring spreads and correct visible failures, without enforcing quotas or alternating templates mechanically.

For a new substantial style reference, compare two or three representative spreads before extending the book. To improve this reusable guidance, distinguish a transferable reason from a one-photo coordinate fix. Try the reason on materially different photos before generalizing it. A same-agent adaptation demonstrates a candidate rule; it does not prove independent models or users will reproduce the result.

## Worked studies and provenance

The independent studies use the same 12 authorized stock photos, each exactly once, with different spatial and color systems. Four other photos were used in two additional two-spread adaptation fixtures. All interiors were browser-rendered and visually inspected. Covers were generated after that review. The fictional travel/daily-life stories are demonstration copy.

Public examples: [editorial study](https://strivekboy-coder.github.io/photo-book-studio/showcase/zine-editorial/) [graphic collage study](https://strivekboy-coder.github.io/photo-book-studio/showcase/zine-collage/) and [handmade study](https://strivekboy-coder.github.io/photo-book-studio/showcase/zine-handmade/).

Visual reference: Flipin's publicly viewable [editorial examples](https://flipin.pages.dev/images/styles/style02all.jpg?v=an7) and [collage examples](https://flipin.pages.dev/images/styles/style01all.jpg?v=an7), reviewed 2026-10-07. No Flipin code, photos, templates or example screenshots are included in this skill. The public links are attribution and optional inspiration; all necessary guidance is above and ships locally.

The third handmade study uses the same 12 source IDs once each across four body spreads, with reused source-linked stickers and non-destructive paper-edge frames. Three worked directions demonstrate relationships; they are not fixed presets or a promise of identical results from every model.

Worked operations: the editorial study has an offset fragment field and photos embedded in a sentence; the graphic study has a perimeter rhythm and dense photo field; the handmade study uses selected paper frames, gently offset clusters and source-linked stickers. These are decision examples to adapt, not a fixed page sequence.
