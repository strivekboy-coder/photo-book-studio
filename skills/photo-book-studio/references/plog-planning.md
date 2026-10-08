# Plog planning and completion evidence

Read before composing a new standalone Plog or a substantial redesign. Local corrections reuse the saved plan and research, update affected evidence, and inspect only changed canvases. This guide decides page allocation; optional artwork is assessed under the single seven-route policy in `zine-policy.md`.

## Decide density from memories, not photo count alone

1. Resolve purpose, aspect ratio, supplied copy, reference density and any user priorities from the brief. Ask only an uncertainty that materially changes the first design. When the user says “由你推荐”, choose a compact first design and save that inference; do not demand another questionnaire.
2. Read every source and assign a provisional visual role: focus, supporting, detail, or sequence. Record why, source IDs and legibility/crop risks. These roles allocate space, never authorize exclusion or declare a memory unimportant. User-designated importance overrides your visual inference.
3. Group photographs by shared story, action, scene or visual relationship. Multiple nearby moments can share a page. Similar images can form a small sequence instead of receiving separate hero pages. Unknown chronology stays unknown.
4. Estimate the smallest comfortable page set that preserves the requested density, readable copy and meaningful subjects. A Plog page often holds 3–5 photographs, sometimes 6–8 simple details, or 1–2 unusually important/complex images. These are starting candidates, not quotas. A hero is optional; dense equal-size fragments may be intentional.
5. For 6–12 mixed everyday photographs with short copy and no sparse-reference request, compare a compact 2–4-page candidate first. Ten photos do not automatically require ten, seven, or three pages. A dense one-page request may also be valid: judge its rendered legibility. An album's expansive rhythm is not a standalone Plog default.
6. Add a page only for a concrete reason: distinct story requiring separation, user-designated emphasis, extended authentic copy, a meaningful sequence, unsafe crop or genuinely unreadable subjects at phone size, or an explicit sparse/gallery reference. Before adding, try regrouping, removing decorative bulk, shortening agent draft copy, and changing frame proportions. Never remove selected sources to solve density.
7. If six or more photographs average fewer than two photographs per page, record why a compact alternative is unsuitable. Treat this as an expansion review, not a ban on sparse Plog. For 10 photographs / 7 pages, name the independent story or legibility need on the sparse pages; “variety”, “each image gets space”, or “more white space” alone is insufficient.
8. Ask one short choice only if unresolved priorities lead to materially different results: “这组更想要紧凑的生活拼贴，还是每个重要片段单独展开？” Offer a recommendation grounded in the actual photos. Do not ask again after the user delegates judgment. Preserve their explicit page count unless impossible; explain a real legibility conflict with a concrete sample.

## Rendered acceptance

Inspect every page at final export size and roughly 390px viewing width. Can a viewer identify the intended subject and action without zooming? A meal detail can be small; a face, multi-person interaction, menu or landmark may need more room. Keep faces, hands, significant background and text safe. Dense is not the same as overlapping essential content. Sparse is not automatically better. Compare neighboring pages and the compact alternative before expanding.

## Resource and decoration decisions

Consult `plog-library.md` during initial style selection. Record at least one concrete case or a user reference and the composition relationship actually inspected; a homepage or unviewed URL is not evidence. The bundled observations can support an offline first sample, labeled as cached observations rather than newly browsed work. When no reference is accessible, honestly record the access limitation and the locally drawn/native fallback. Inspect the fallback in the output.

Record material needs and the reuse/draw/generate/skip decision. No external purchase or download is mandatory. Original SVG doodles are fully valid: derive a recognizable motif, contour, gesture or joke from this batch, specify its composition role, and render it. Generic hearts or stars can be accents, but should not be presented as bespoke photo-derived illustration. Register successful motifs with source, method, palette, transparency, paths and suitable pages. Imagegen is for a real raster/texture/illustration need, not a mandatory demonstration of creativity. Preserve approved assets.

For a new lettering direction, compare at least two locally available, licensed font specimens using the actual title and notes; inspect both at intended sizes. A user-fixed font or an already approved system can be reused with its reason and character coverage check. Do not label a Kai font as natural handwriting without examining it. Record the chosen role and why it works with these photographs. Retain license notices.

## Single seven-route assessment

Record routes 1–7 from `zine-policy.md` with individual use/skip/candidate decisions, source-linked reason, and tool/permission constraints. Zero uses is valid. Do not use an older subset or split the assessment into separate groups. A candidate not used in the final output needs its outcome recorded. Imagegen use must record the real tool, filled prompt, inputs, outputs and reviewed deviations; an SVG drawing records its actual vector provenance instead.

## Portable completion record

Initialization creates `project/plog-review.json` with unresolved fields. Fill it from real work; never fabricate research, font comparisons, rendered inspections or tool calls. After `plog.py build`, rendering and human/model pixel inspection, run:

`python <skill>/scripts/plog.py check --workspace <workspace>`

The check verifies missing workflow evidence, source roles/page identity, all seven decisions and current-build review identity. It does not measure aesthetic quality or prove an agent's claims. Build remains usable for intermediate drafts. On a local revision reuse research/route decisions; carry unchanged inspected page IDs forward only after checking their layers are unchanged, update the current book hash, and inspect every changed page.

Record format:

```json
{
  "version": 1,
  "planning": {
    "photos": [{"file": "source.jpg", "role": "focus", "reason": "User-designated birthday portrait"}],
    "pages": [{"page": 1, "files": ["source.jpg"], "reason": "Explicit one-photo poster request"}],
    "densityReason": "Requested one-photo poster",
    "expandedReason": ""
  },
  "resources": {
    "inspiration": [{"source": "User reference or exact local/remote case", "observed": "Relationship inspected", "application": "How tried here"}],
    "materials": {"decision": "draw", "reason": "Native tape and original source-linked doodles suffice"},
    "fonts": {"mode": "compare", "candidates": ["font A", "font B"], "actualCopy": "Actual title and note", "reason": "Rendered comparison result"}
  },
  "decoration": {"method": "svg", "reason": "Source-linked motif and its layout role"},
  "creativeReview": [{"route": 1, "decision": "skip", "reason": "Specific reason"}],
  "visual": {"bookSha256": "current build-audit hash", "pages": [{"page": 1, "inspected": true, "phoneInspected": true, "notes": "Actual pixel findings"}]}
}
```

The example shows one photo/page and one route only to illustrate entry fields; a real record must cover every selected source, every page, and all seven routes.
