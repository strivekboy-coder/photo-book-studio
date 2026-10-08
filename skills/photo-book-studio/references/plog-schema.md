# Standalone Plog execution and layer schema

Read for Plog / digital scrapbook authoring. It is separate from printed spreads; no gutter or print cover unless requested. Composition guidance remains in plog-composition.md.

## Resolve and analyze

Read the saved brief for revisions. For a new standalone Plog, resolve missing story/location, output ratio, visual references, copy source, selection and treatment permissions. Save each value as explicit/inferred/unknown and set intakeComplete when resolved. Do not ask for a printer or run the printed-book questionnaire for a social collage.

Inventory all user-selected uploads. Inspect the contact sheet and full-size hero/crop-risk images. Group by event before allocating canvases. Dense pages are valid; source preservation, readability and reference fit determine whether to add a page. Review relevant concrete examples and available paper/sticker/font material before composition. Optional generated art and the seven creative routes are decisions, not quotas.

## Portable commands

Resolve paths relative to the installed skill. Python 3.10+ is required. Install requirements-plog.txt. Browser rendering uses Playwright with installed Edge/Chrome or its Chromium download.

    python <skill>/scripts/plog.py init <workspace> --title "旅行小记"
    # Save the minimum resolved project/brief.json.
    python <skill>/scripts/plog.py inventory --workspace <workspace> --photos <selected-folder>
    python <skill>/scripts/plog.py font --workspace <workspace> --name yozai
    python <skill>/scripts/plog.py font --workspace <workspace> --name xiaolai
    # Compose project/book.json from actual photographs.
    python <skill>/scripts/plog.py build --workspace <workspace>
    python <skill>/scripts/plog.py render --workspace <workspace> --browser <installed-browser>

Use --page N, repeatable, for scoped revisions. A successful build checks source IDs/counts, not taste. Inspect output/plog/page-NN.png and page-NN-phone.png. Record actual findings in visual-review.json; never mark a page approved without viewing. Build/render audits include the current book hash so old screenshots cannot be mistaken for a changed draft.

## Data model

Store the standalone layout in project/book.json with kind: plog. The inventory stores stable file IDs and original hashes. Sources are copied intact into assets/photos.

    {
      "kind": "plog",
      "title": "旅行小记",
      "photoRoot": "assets/photos/",
      "format": {"widthPx": 1200, "heightPx": 1600},
      "fonts": {
        "default": "assets/fonts/LXGWWenKaiLite-Regular.ttf",
        "hand": "assets/fonts/yozai.ttf"
      },
      "policy": {"allSelectedPhotosRequired": true, "authorizedOccurrences": {}},
      "pages": [{
        "title": "海边",
        "background": "#f3ecd9",
        "layers": [
          {"type": "photo", "file": "photo.jpg", "x": 60, "y": 180,
           "w": 640, "h": 900, "rotate": -3, "border": 8, "mat": "#fff7df"},
          {"type": "text", "text": "海风小记", "font": "hand",
           "x": 70, "y": 70, "w": 500, "h": 100, "size": 50, "color": "#476255"}
        ]
      }]
    }

This is a format example, not a preset. Every selected source must appear according to its authorized occurrence count.

Common layer fields: type, x/y/w/h in canvas pixels, rotate in degrees, z for stack order, opacity. List order supplies z if omitted.

- **photo:** file is a selected inventory ID. fit defaults to cover; contain is supported. position defaults to 50% 50%. border, mat and matBottom form a frame; shadow is optional. clip can be none, circle, rounded or torn. sourceBox is [x,y,width,height] in the orientation-corrected source; scaling is uniform and bounds are validated. Shape/crop safety still requires visual judgment.
- **Approved derivative:** keep file; set path and approvedDerivative: true. The brief must contain permissions.approvedDerivatives[file] = {"path": "...", "source": "explicit"}. Do not create this evidence without user authorization. Original hashes remain checked.
- **image:** path is a project-local decoration; decorative must be true and no file ID may be attached. fit defaults to contain, preserving the complete alpha silhouette. cover/fill can serve intentional material fields. Record source/license or generation prompt.
- **text:** text is escaped, retains newlines and wraps within w. font names a project font role. size, lineHeight, color, align, outline and outlineWidth are supported. Actual-copy missing characters block the build instead of silently mixing glyphs. Unsupported emoji can use suitable licensed decorative artwork rather than a missing glyph.
- **paper:** color plus optional grid/ruled/dots, gap and ink. Useful for spines/underprints without raster material.
- **path:** SVG path data d in the layer's own w/h viewBox, color, strokeWidth, fill and optional dash. Use for native lines and doodles.

A decorative PNG's layer box is not its writable region. Inspect its contain-scaled shape, including holes, folds, scallops and transparent padding. Keep notes in the visible safe region. An intentional partial headline underprint differs from a caption accidentally spilling out of a label.

## Lightweight material use

The skill includes twelve small original SVG utilities at assets/plog-starter, copied during initialization. They are supporting material, not a mandatory style. The provider index ships with the skill. Larger raster packs are optional and cached in each user's project.

    python <skill>/scripts/plog.py material-pack --workspace <workspace> \
      --archive <pack.zip> --name paper-pack --sha256 <verified-hash>

The importer checks archive paths/file types and refuses to overwrite a pack. It does not establish artwork rights: record source/licensing before use. Font downloads are pinned author releases with OFL notices and cache reuse. Follow current landing pages for other providers; do not hardcode expiring download tokens or invent an API.

The author's private photos, practice folders and old layouts are not dependencies or shipped templates.

## Development evidence and limits

Three one-canvas studies were made sequentially: a private night journal, a six-photo food journal and an unrelated six-photo stock street/food/attraction collage. Each was inspected at full and phone size and corrected. They exercised whole-sticker containment, visible writing regions, bright accents, dense clustering and source-dependent geometry.

Fresh-copy and content-invariant tests verify the tool path. A fresh installation can use the same schema/instructions without this chat or the author's folders. These are human-review candidate results, not a guarantee of identical aesthetic decisions by every model. Seek human review before declaring the style mature.


## Browser fine-tuning

Plog `sample.html` includes the local editor by default unless the user requests static/image-only delivery. It opens in preview mode and editing remains optional: click **微调排版**, select a photo/text/sticker, drag, resize from the lower-right handle, or rotate from the upper handle. Photos and decorative images keep their aspect ratio; resize recomputes sourceBox placement without altering source bytes. A layer selector reaches covered paper and doodles; text controls edit copy, font role, size and color. Undo/redo and keyboard arrow nudges are supported. The initial view remains a clean preview.

Drafts are browser-local and keyed to this workspace and book revision; a rebuild with changed book content gets a new key. Save/download before moving browsers or clearing site data. **编辑备份 → 备份布局 · JSON** exports `book-edited.json`: review it, retain the previous book as a backup, then apply it to `project/book.json` and run build/render to enforce source counts and font coverage. Editing a new character in the browser can trigger font fallback; CLI build remains the glyph gate. **编辑备份 → 备份页面 · HTML** saves the visible edited HTML with editor state embedded; put it alongside the existing `assets/` folder. It is not an asset-embedded portable package. Its export view contains saved edits. Draft edits in localStorage do not affect automated export of the original sample; use downloaded HTML or apply the layout first. The editor never silently overwrites local source/project files. Render and inspect any final edited layout before claiming it passed the normal completion gate.

SVG doodles should be separate semantic layers with a tight `viewBox: [x,y,width,height]`, local bounding box and optional `label`. Related strokes such as an arrow shaft and head can use `parts: [{d, dash?}, ...]` within one layer. This preserves independent selection and meaningful scale/rotation handles. Invisible expanded stroke targets exist only in the editor and never in final export.

## Final sharing files

Use `python <skill>/scripts/plog.py render --workspace <workspace> --browser <installed-browser> --jpg` to create full-resolution PNGs and quality-95 JPGs. Add `--pdf` only when explicitly requested or specified in the saved brief to create an ordered reading PDF. `--page` limits both rendering and these deliveries; a partial PDF's filename names the selected pages. Omit `--pdf` when only social-sharing images are needed. Review the actual rendered pages before delivery. This path renders `project/book.json`; it does not read a user's browser-local draft. Apply the user's edited layout first when exporting their adjustments. The backup controls in the HTML are secondary editing handoffs; final files should be linked directly in the conversation. Reading PDF output does not replace the regular book's print preflight/export path.
