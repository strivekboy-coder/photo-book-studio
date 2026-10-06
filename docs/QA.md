# Release validation

Validated locally on Windows, Python 3.12, Node 22 and installed Edge:

- Nine workflow tests covering source preservation, idempotent import, occurrence checks, missing assets, fresh initialization and configurable dimensions, Chinese filenames and EXIF rotation.
- Full installed skill directory initializes a separate workspace without reading the author's project.
- A three-spread geometric book exports reading, interior and cover PDFs. Four body faces become eight print faces after parity/increment padding. All page rotations are zero; square media is 216mm and trim is 210mm with 3mm bleed.
- Browser screenshots are inspected, including phone reading and portrait/landscape ratios. Raster export warnings remain distinct from source-quality or aesthetic approval.

GitHub Actions runs the basic workflow checks on Windows and Linux. Browser/PDF smoke tests are separate and require print dependencies. Real-photo examples for dogs, children and couples are pending; technical tests do not certify their aesthetic results.
