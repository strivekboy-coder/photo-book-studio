# Plog planning and lightweight completion evidence

Use `plog-workflow.md` for the five-stage standalone pipeline. Allocate pages from memories, source roles and phone legibility, not printed-book rhythm. For 6–12 everyday photos with short notes, compare compact options first; two, three or four pages are candidates, never quotas. If a sparse result needs more pages, record its story/emphasis/copy/readability reason. Never omit a source to solve space.

Keep groups provisional while matching suitable creative methods. An envelope or layered cluster can gather several photos as one local component. Its mapped source IDs count once, not again as surrounding snapshots. Dense or sparse may work; hierarchy and recognizable subjects decide. The original photos may supply the direction without fresh external research.

## New review record: version 2

Initialization supplies a short record. Fill actual planning, chosen production method, generation provenance when used, and one current final-page full/phone review. Per-generation enlarged/pixel/source comparisons and intermediate inspection notes are not required. Resources are conditional: no mandatory website visit, download or two-font comparison. Imagegen handwriting is a valid text method; native exact-copy fonts may need comparison/coverage checks. `creativeReview` records only selected candidates and important rejection reasons. Zero uses and an empty shortlist are valid.

```json
{
  "version": 2,
  "planning": {
    "photos": [{"file":"source.jpg","role":"focus","reason":"Visible gesture carries the memory"}],
    "pages": [{"page":1,"files":["source.jpg"],"reason":"One-photo request"}],
    "densityReason":"User-requested single photo",
    "expandedReason":""
  },
  "production": {"method":"integrated","reason":"Photo and paper need joint generation"},
  "resources": {"inspiration":[],"materials":{},"fonts":{}},
  "decoration": {"method":"imagegen","reason":"Integrated paper and pen texture","generations":[
    {"tool":"actual image tool","prompt":"filled prompt","inputs":["assets/photos/source.jpg"],"sourceFiles":["source.jpg"],"outputs":["assets/result.png"],"inspection":"Compared face and pose; details reported"}
  ]},
  "creativeReview": [],
  "visual": {"bookSha256":"current build hash","pages":[{"page":1,"inspected":true,"phoneInspected":true,"notes":"Actual findings and any limitations"}]}
}
```

The example has one source only for clarity. Real records cover every selected source and current page. Pure materials/symbolic artwork may have no photo input; photo-derived records name actual references and covered source IDs. Keep input paths/prompts/output/inspection in actual records, not fabricated prose.

For native/generated-layer projects, build, render and inspect, then run `plog.py check --workspace <workspace>`. `artwork` layers have source maps and generation records; counting does not prove that the generated image truly retained those subjects. Unchanged-source hashes and current visual records remain mandatory. The legacy version-1 checker remains available to established projects, but new projects do not inherit its mandatory research/font/seven-route bureaucracy. On revisions update only affected planning/visual evidence; reuse unchanged page findings only after verifying the layers/assets are unchanged.
