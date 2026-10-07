# Release validation

Validated locally on Windows, Python 3.12, Node 22 and installed Edge:

- Eleven workflow tests covering source preservation, idempotent import, occurrence checks, missing assets, fresh initialization and configurable dimensions, Chinese filenames and EXIF rotation.
- Full installed skill directory initializes a separate workspace without reading the author's project.
- A three-spread geometric book exports reading, interior and cover PDFs. Four body faces become eight print faces after parity/increment padding. All page rotations are zero; square media is 216mm and trim is 210mm with 3mm bleed.
- Browser screenshots are inspected, including phone reading and portrait/landscape ratios. Raster export warnings remain distinct from source-quality or aesthetic approval.

GitHub Actions passed the basic workflow checks on Windows and Linux. Browser/PDF smoke tests are separate and require print dependencies. Four curated stock-photo showcase books (cat, couple, Munich and Chengdu) have been rendered and visually reviewed, including 50 selected photos placed with zero omissions. Dog and child-growth scenarios remain untested. Technical checks alone do not certify aesthetics.

Additional browser compatibility check: Chinese filenames, spaces, hash, ampersand and apostrophe all load successfully.

AVIF imports are now covered by a workflow test and require Pillow 11.3+. The Chengdu showcase uses English captions and cover lettering.

Zine design studies (2026-10-07): two portrait-format books, each placing the same 12 authorized stock photos once across four body spreads. Editorial/minimal and saturated graphic collage interiors were rendered and visually reviewed. Two additional four-photo fixtures were recomposed into two spreads each to check adaptation with different subjects. This is a same-agent design check, not an independent-user or cross-model evaluation. No print export is claimed for these web design samples. External Flipin references were publicly viewable; no external templates/code were incorporated.

The v0.4.0 archive was extracted into a separate directory and initialized successfully. Workspace AGENTS.md now copies during init; a regression test covers that contract. Eleven workflow tests pass locally.

The v0.4.1 studies were recomposed into three body spreads each, still 12 selected/12 placed/0 omitted. New reviewed operations include a loose fragment field, images interwoven with a sentence, a seven-photo contact field and a decorative perimeter. The heart/arc silhouette and screen-stack operations are documented candidates, not claimed as rendered samples.
