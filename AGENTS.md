# Maintaining Photo Book Studio

This repository contains the reusable skill and engine, not a user's personal book. Keep source inventories, private photos, music, credentials, previews and project JSON in a separate workspace. Only explicitly approved example assets belong in the repository.

The installed unit is the entire skills/photo-book-studio directory. Preserve its runtime, font licenses and relative paths. Verify a fresh initialization instead of assuming the author's environment is available.

For a skill/workflow change, keep intake once per new book, source IDs and authorized occurrence counts, scoped revisions and browser review. Default final image-generated covers happen after the interior review; unavailable tools have an honest photo/text fallback. No third-party creative skill is a mandatory dependency.

For code changes, run python -m unittest discover -s tests -v. For renderer or export changes, inspect browser pixels and PDF dimensions with a clean fixture; tests alone do not certify aesthetics. Do not regenerate unrelated real books.

Read only the relevant references. Do not run the photo-book questionnaire for repository maintenance, installation or bug fixes. Real-photo examples require a source/permission manifest and must not be described as validated before visual review.
