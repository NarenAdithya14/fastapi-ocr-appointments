# Release instructions

1. Build & test locally

## v0.2.0 — Release notes

- Date: 2026-01-21
- Highlights:
   - NLP: improved relative date parsing ("next Friday", "tomorrow", etc.) using `dateparser` with a deterministic RELATIVE_BASE for tests.
   - Timezones: added `tzdata` and return timezone-aware ISO-8601 datetimes (Asia/Kolkata) when normalization succeeds.
   - Department normalization: expanded synonyms and canonicalization (e.g., "dentist" -> "Dentistry").
   - Confidence scoring: per-field confidences (date/time/department) and overall entity confidence are now returned by the pipeline.
   - API: unified response schema — endpoint always returns `pipeline` and `appointment` objects.
   - Tests: updated tests to be deterministic (explicit years in fake OCR where needed) and added relative-date tests.
   - Docs & demo: added `docs/` demo skeleton, demo recording scripts, and README improvements.

## How to create the GitHub Release (recommended)

1. Tag the release (already done for this repo):

    ```powershell
    git tag -a v0.2.0 -m "v0.2.0: relative date parsing, tzdata, department normalization, confidence scoring"
    git push origin v0.2.0
    ```

2. Draft a release on GitHub and copy these release notes into the release description.

3. Share

   - Share the repo link and the release link as your submission.

# Release instructions

1. Build & test locally

   ```powershell
   .\.venv\Scripts\python -m pip install --upgrade pip
   .\.venv\Scripts\python -m pip install -r requirements.txt
   .\.venv\Scripts\python -m pytest -q
   ```

2. Create GitHub repo and push

   - Create a repository named `fastapi-ocr-appointments` under user `Narenadithya14`.
   - Run `scripts\publish_to_github.ps1` (it will prompt you to authenticate if needed).

4. Create a Release

   - Go to GitHub > Your repo > Releases > Draft a new release and paste these release notes.
5. Share

   - Share the repo link and the release link as your submission.
