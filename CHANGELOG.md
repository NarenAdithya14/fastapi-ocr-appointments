# Changelog

All notable changes to this project are documented in this file.

## v0.2.0 - 2026-01-21

- NLP: improved relative date parsing ("next Friday", "tomorrow", etc.) using `dateparser` with deterministic RELATIVE_BASE support for tests.
- Timezones: added `tzdata` and return timezone-aware ISO-8601 datetimes (Asia/Kolkata) when normalization succeeds.
- Department normalization: expanded synonyms and canonicalization (e.g., "dentist" -> "Dentistry").
- Confidence scoring: per-field confidences (date/time/department) and overall entity confidence returned by the pipeline.
- API: unified response schema — endpoint returns `pipeline` and `appointment` objects for all inputs.
- Tests: updated tests to be deterministic (provided `ref_date` where needed) and added relative-date tests.
- Docs & demo: added `docs/` demo skeleton, demo recording scripts, and README improvements.
