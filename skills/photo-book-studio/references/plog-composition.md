# Plog and scrapbook composition prototypes

Read when the user requests Plog, a digital scrapbook, a single-page travel journal or reference-led social collage. These are independent vertical canvases; a printed-book spread and its gutter are not the right default. Existing book workflows remain unchanged.

## Scope and persistence

Use the lightweight intake in intake-questionnaire.md: an optional invitation for style/reference/copy/stickers, with supplied facts and safe defaults sufficient for a first design. Do not interrogate every missing field; ask only what materially blocks this prototype. Record explicit/inferred/unknown preferences in the workspace brief before arranging. A standalone collage trial is not a new printed book and does not need the full print questionnaire. If the request becomes a new book, run its normal intake once.

Preserve all selected photographs across the main page set; use each once unless the user authorizes repeats or alternatives. A source photograph used as a background counts as a placement and must remain recognizably meaningful, not almost entirely hidden. Keep variants separately identified. Record source IDs, safe crops, positions, masks, captions and asset provenance. If EXIF is absent, preserve known order or group by visible scene without inventing a dated itinerary.

Standalone Plog layers have a separate portable renderer, scripts/plog.py; read [plog-schema.md](plog-schema.md) for its supported fields and commands. Keep the source inventory, brief, project/book.json, sample.html and browser review in the user's workspace. The renderer does not replace event composition, source reading or aesthetic judgment. Do not pass standalone layer fields into the printed-book renderer.

## Reference, material and font research

At style selection for a new Plog theme or substantial design exploration, proactively consult the [Plog library](plog-library.md) alongside the user's supplied references. Reuse relevant checked examples and assets; perform targeted research when the intended style, material or lettering is missing. Do not wait for the user to ask for source research each time. Local caption/crop/sticker corrections can reuse the chosen direction and do not require a fresh sweep of every website.

Inspect concrete work, not just a site's landing page. Extract a few relevant relationships: image/text scale, density, alignment, mask or cutout roles, material layering and writing behavior. Record which relationships are being tried and judge them in the render. A visited website is not an implemented reference, and a larger photograph is not automatically a better Plog.

Maintain distinct records for inspiration cases, usable material assets and fonts. Add a case's original page/creator when known, what was actually inspected, intended use, and observed trial result. Add downloaded assets with exact provenance and permitted use. Keep candidates, inaccessible items and rejected sources distinct from verified material. Render actual-copy font specimens when choosing a new lettering system. Broaden the library with different visual families; do not grow a list of interchangeable links merely to increase its size.

## Compose before decorating

1. Choose a focal memory and a readable eye path. A quiet full-scene background, a paper strip or a two-sided cluster may organize the page.
2. Establish a readable hierarchy among photographs, phrases and decoration clusters. A dense Plog can use many small photos; it need not have one oversized hero. Scale by narrative role and check that intentional subjects remain recognizable at the intended viewing size.
3. Use controlled irregularity around a few shared edges or a center of gravity. Rotation alone does not turn a card grid into sophisticated collage.
4. Mix rectangular snapshots with safe circular/details masks only when the actual subject permits it. A circular crop is not subject extraction. Preserve faces, hats, hands and important environmental context.
5. Use text as part of the rhythm: title, brief personal commentary and optional known place/date. Distinguish a legible handwriting role from factual microtype when useful. Do not fill space with invented diary events.
6. Pick material and ornament together with the layout. Tape can attach a photograph to paper; an arrow can connect a remark to its subject; a motif can echo an actual object. Remove ambiguous loops and unrelated clip art. Relate stroke, palette, edge treatment and scale to their roles. A deliberately bright heart or playful sticker may contrast with quiet photographs; do not automatically mute it or replace a useful motif to make every material uniform.

An elaborate page can work; a restrained page can work. Judge hierarchy and relationships, not a fixed quota of stickers, rotations or whitespace. Source-linked decoration should not imply an activity absent from the brief.

## Dense journal layouts and visual invention

Judge density separately from collisions. Small photographs, tight text-image gaps and abundant motifs can be the intended Plog language. Do not equate more space, larger photos or more pages with higher quality. Preserve faces, hands and meaningful content, but assess a small supporting image by its role and legibility rather than a fixed minimum size. Photo count and decoration count are not aesthetic scores.

Build relationships before adding variety. Useful candidates include a paper/label behind a photo with a note crossing its safe edge; an actual ticket or blank pocket connecting several snapshots; round details interrupting rectangular frames; a sequence of short handwritten notes running through a photo cluster; and a bright accent paired with quieter repeated motifs. A triangle, ring, timeline or zigzag is an optional eye path, not a required template. Rotation alone is insufficient.

Let an ornament do a specific job: introduce atmosphere, connect moments, underline a joke, lead the eye or provide a contrasting emotional accent. A separated bright heart can be a deliberate focal beat; it does not need to touch another object. Stars/moons suit a night memory without proving they were visible in the photograph. This symbolic freedom does not authorize invented factual events or relationships.

Explore style relationships across the user's actual outing: city walks, seaside, parks, meals, museums, movies, live shows and games. These events can each be paper-like, graphic, neon, photographic or playful; do not impose one style per activity. Consult the [travel and entertainment case studies](plog-library.md#travel-and-entertainment-research) when relevant. New tutorial-derived operations remain candidates until a rendered adaptation shows that they help. During skill development, change a useful relationship and compare the result; do not claim that a visited site or a new material pack proves improved Plog quality.

## Natural handwriting

For a reference resembling iPad pen writing, compare the actual Chinese copy at title and annotation sizes. A neatly typeset Kai face is not automatically a convincing casual handwriting face. Look for monoline/pen rhythm, loose character proportions, natural spacing, rounded or angular endings and small-size legibility. Titles and personal notes may use different handwriting families when their roles are clear; varied fonts should express those roles, not become random decoration.

Choose from verified author/vendor sources and record licensing. Render a specimen and inspect it beside the actual photos before committing. Check every used character against the font cmap; a thin traditional font mixed with silent simplified-Chinese fallback ruins the intended handwriting language. Avoid artificial per-character jitter as a substitute for a suitable typeface. Modest note angle, line spacing, an outline emphasis or a phrase-shaped arrangement can supply natural variation without sacrificing readability.

Candidates, not mandatory defaults:
- [Yozai](https://github.com/lxgw/yozai-font): OFL handwriting family; its Medium weight was useful for pen-like annotations in a tested coastal redesign.
- [Xiaolai](https://github.com/lxgw/kose-font): OFL handwriting derived from SetoFont; a rounded emphasis option.
- [LXGW Marker Gothic](https://github.com/lxgw/LxgwMarkerGothic): OFL marker-style alternative; assess the actual glyphs rather than assuming its name means casual pen writing.
- [ChenYuluoyan](https://github.com/Chenyu-otf/chenyuluoyan_thin): natural fine handwriting, but the tested 2.0 Thin file lacked several simplified characters in this pilot. Verify coverage before choosing; do not silently change the user's script.
- [ELEYANG Plog](https://www.eleyang.com/zh/font-plog): commercial handwriting reference; no downloaded or bundled font. Its official specimen is not proof that a particular blogger uses it.

Keep any fonts and their license notices in the user's project. Do not imply commercial fonts are included or needed. A font can approximate handwriting; it cannot guarantee the individuality of a person's actual pen writing.

## Asset choice and acquisition

For the user's Plog direction, prefer photo/story-specific original motifs over repeatedly searching generic sticker kits: first identify the actual objects, gestures, atmosphere and small jokes that deserve emphasis, then choose how to draw them. Use original SVG for expressive line doodles, arrows, stars, simple object outlines and flat graphic marks. Use an available image-generation tool for a concrete watercolor, textured, illustrated or otherwise raster-specific need; write a source/story-linked prompt describing motif, palette, stroke/material, intended placement and transparent-background requirement. A prompt does not replace rendering and inspecting the actual SVG or generated pixels. Existing suitable materials remain useful; retain approved ornaments and use verified libraries for paper, tickets, pockets or other ready-made assets when they improve the composition. This is a practical preference, not a quota requiring both SVG and imagegen on every page.

Keep the inspiration library for relationships: eye path, layering, handwritten-note rhythm, shape contrasts and expressive accents. Keep a small reusable asset library for proven motifs and structural materials, but do not grow a generic collection at the expense of story-specific creative work. Newly successful original motifs can be registered for later reuse after a real rendered trial.

Record a short `decorationReview` in the brief: story-linked motif ideas, retained assets, the remaining expressive or structural need, and `imagegenDecision` (generate/reuse/skip) with a concrete reason. Reusing earlier generated artwork is different from generating a new asset. Check playful emphasis and source-related doodles as well as paper utility; a generic "not needed" is insufficient when the page still lacks character. Generation permission makes the option available; it does not justify replacing good existing stickers. Keep original photographs embedded truthfully, register decorative provenance, and never repaint portraits to create an entire collage.

For recurring motifs, a transparent sheet can keep palette, line weight and material treatment consistent. Extract reusable PNGs while preserving alpha, inspect them on the actual light/dark backgrounds, and register the tool/prompt, source sheet, extraction regions, theme, colors and suitable pages. Copy any used asset into the consuming project. Generated motifs and illustrations are decorative by default; they do not replace selected photographs or count toward source completeness. A motif that overlaps a face, hand, caption or essential subject must be moved or removed.

For paper, tape, tickets, pockets and label needs, consult the [paper/ephemera provider notes](plog-library.md#paper-pockets-and-ephemera-providers). Prefer a verified current product download or a suitable existing material for repeatable ordinary needs. A free paper library may permit finished designs but forbid bundling raw assets; source routing belongs in the skill, while restricted downloads remain project-local. Generate a reusable structural sheet when a specific style or function is missing, then inspect alpha and extraction boundaries before registering its pieces.

For every external asset record its landing page, author if available, exact license, download date and whether raw-file redistribution is allowed. A free preview, Pinterest pin or downloadable JPG is not a reuse grant. A paid asset may be usable in an output but forbidden inside the distributed skill. Separate finished-output rights from distributing raw assets.

- [ambientCG](https://ambientcg.com/view?id=Paper001): Paper001's Color map is a useful paper substrate; assets are CC0 according to its [license](https://docs.ambientcg.com/license/). Normal/displacement maps are not background images.
- [SVG Repo](https://www.svgrepo.com/): choose suitable individual assets and verify each license. Do not assume one license covers the whole site.
- Stock and scrapbook kits: verify the individual asset and intended output; do not package a downloaded kit just because it permits personal design use.
- Existing generated sticker assets: retain original generation provenance, check theme fit and copy project-used assets into the consuming workspace.

If download fails, try normal browser access and official download routes. A screenshot can support visual study, but it does not grant reuse rights and is a poor substitute for alpha-capable PNG/SVG. If the browser only shows a verification page, record that limitation and continue with accessible alternatives. Plugins do not guarantee access through third-party website checks.

## Inspiration directory

Reviewed 2026-10-08. The following are sources for design relationships; no general open-asset license was established. Do not download their artwork as reusable stickers or bundle screenshots into this skill.

| Source | Useful study | Access / reuse evidence |
|---|---|---|
| [It's Nice That](https://www.itsnicethat.com/) | Collage, publications, typography and graphic design; extract focal scale, color relationships and material layering | Home and a collage feature readable; the feature credits copyrighted artwork |
| [Agent 002](https://www.agent002.com/) | Illustrators' visual languages and coherent motif families; travel and lettering categories | Public talent/theme listings readable; reuse authorization not established |
| [KIBLIND](https://www.kiblind.com/) | Contemporary illustration, magazine direction and risograph material cues | Official site describes magazine, illustration agency, prints and festival; reuse authorization not established |
| [Pinterest](https://www.pinterest.com/) | Discover scrapbook references, then follow the creator's original page | A public beach-scrapbook board loaded in a browser with a login modal in the follow-up trial; access beyond the visible board was not verified; pins are not evidence of licensing |
| [DoBeDo Represents](https://www.dobedorepresents.com/) | Photographic storytelling and image relationships | Official agency/artist content readable; reuse authorization not established |
| [TOILETPAPER](https://www.toiletpapermagazine.org/) | Bold visual emphasis and unusual object relationships, when appropriate to the brief | Homepage image listings readable; reuse authorization not established |

A useful concrete study is [Sveinung Sudbø's Bang Cook Book feature](https://www.itsnicethat.com/articles/sveinung-sudbos-illustration-publication-project-300926): its food-related collage connects material and color to the experience being described. This is inspiration, not a downloadable ingredient library. Do not copy its artwork, captions or coordinates.

## Review at the intended reading size

Render every canvas in a real browser and inspect both full resolution and roughly phone-sized viewing. Audit completeness separately from aesthetics.

Ask:
- Does the eye reach the focal memory before the title or decoration?
- Is the person/subject still large enough at normal viewing size?
- Does the background preserve atmosphere while leaving text readable?
- Do different shapes and photo sizes form a deliberate rhythm?
- Do material edges and doodles belong to one visual language?
- Does each caption refer to its nearby photo without crossing a subject or frame awkwardly?
- Are masks truthful, margins safe and small images still meaningful?

A first three-canvas coastal trial established feasible scene-background, dark snapshot and paper-strip compositions. It does not prove expert-level aesthetic quality or independent-agent reproducibility. Early author review proposed checking busy title backgrounds, portrait scale relationships and small food details. The user subsequently preferred the original night page and explicitly approved its bright watercolor heart with cream line doodles. Do not treat mixed materials or similar portrait scales as automatic defects, mute the approved accent, or let an early candidate critique override later user approval. Assess the rendered relationships in context; retain successful choices without freezing that palette or geometry as a universal template.

No private source photographs or trial outputs ship with this reference.

Three later sequential one-page studies checked the ordinary workflow through the portable Plog tool on night, food and unrelated stock-city content. They confirmed that whole-decoration containment and visible-writing-region checks prevent practical failures while expressive accents and dense photo groups remain. Those checks verify practical rendering relationships; the user later judged the stock-city demonstration weaker than the approved first version. They do not establish aesthetic improvement or identical quality from every model. Preserve recorded user-approved versions and assess actual results rather than counting trials, pages or new materials.

## Seven creative treatments inside Plog

Read `zine-policy.md` after the ordinary photo/text/material composition of a new Plog set or substantial redesign. Evaluate all seven routes, including the three in `creative-prompts.md`, with the saved permissions and source roles. An envelope insert, a contour breaking a photo window or a quiet three-photo paper cluster may help; they are optional treatments. Do not turn every Plog into an imagegen poster or impose the new paper-collage route's 45% occupancy on a dense scrapbook. Preserve original photo layers and meaningful handwriting/doodles where they carry the page. Generated derivatives remain additional unless a specific replacement is authorized and auditable.
