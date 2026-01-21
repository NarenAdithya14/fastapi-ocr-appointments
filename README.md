# FastAPI OCR Appointment Scheduling Service

This project is a backend service for scheduling appointments using Optical Character Recognition (OCR) and Natural Language Processing (NLP). It provides an API endpoint to handle appointment requests and processes them through a defined pipeline.

## Project Structure

```
fastapi-ocr-appointments
├── src
│   ├── main.py                # Entry point of the FastAPI application
│   ├── api
│   │   └── appointments.py     # Defines the POST /appointments endpoint
│   ├── core
│   │   └── config.py          # Configuration settings for the application
│   ├── models
│   │   └── schemas.py         # Pydantic models for request and response schemas
│   ├── services
│   │   ├── ocr_service.py      # Implements OCR functionality
│   │   └── nlp_service.py      # Functions for entity extraction and normalization
│   ├── pipelines
│   │   └── appointment_pipeline.py # Orchestrates the appointment scheduling pipeline
│   ├── validators
│   │   └── appointment_validator.py # Validation logic for input
│   └── utils
│       └── parsing.py         # Utility functions for parsing data
├── tests
│   ├── test_appointments.py    # Unit tests for the appointment API
│   └── test_pipeline.py        # Tests for the appointment pipeline
├── requirements.txt            # Lists project dependencies
├── pyproject.toml              # Project dependencies and configurations
├── Dockerfile                  # Instructions for building a Docker image
└── README.md                   # Project documentation
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd fastapi-ocr-appointments
   ```

[![CI](https://github.com/Narenadithya14/fastapi-ocr-appointments/actions/workflows/ci.yml/badge.svg)](https://github.com/Narenadithya14/fastapi-ocr-appointments/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](./LICENSE)

# OCR-based NLP Appointment Scheduling Service

This repository implements a FastAPI backend that accepts typed text or images (OCR) and extracts appointment details using lightweight NLP. The service normalizes dates/times, applies guardrails for ambiguous inputs, and returns a structured appointment JSON suitable for a demo submission.

Quick links
- Docs (local): http://127.0.0.1:8000/docs
- Postman collection: `docs/postman_collection.json`

Why this repo
- Clear, testable pipeline: OCR → entity extraction → normalization → guardrails
- Designed for a demo / SDE intern assignment: easy to run locally, tests included, and a short demo flow

Repository layout (important files)

```
src/
   main.py                # FastAPI app (entry)
   api/appointments.py    # Router & API input handling
   services/ocr_service.py
   services/nlp_service.py
   pipelines/appointment_pipeline.py
tests/                   # pytest tests
requirements.txt
Dockerfile
README.md
scripts/                 # demo & publish helpers
```

Quickstart (Windows - PowerShell)

1) Create venv and install deps
```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install --upgrade pip
.\.venv\Scripts\python -m pip install -r requirements.txt
```

2) Install Tesseract (required for `pytesseract`):
- Chocolatey: `choco install tesseract -y` or download installers from https://github.com/tesseract-ocr/tesseract/releases

3) Run server
```powershell
.\.venv\Scripts\python -m uvicorn src.main:app --reload --host 127.0.0.1 --port 8000
```

Try it (sample requests)

- Typed text (JSON)
```powershell
curl -X POST http://127.0.0.1:8000/appointments `
   -H "Content-Type: application/json" `
   -d '{"text":"Book cardiology appointment next Friday at 10 am"}'
```

- Image upload (multipart)
```powershell
curl -X POST http://127.0.0.1:8000/appointments `
   -F "image=@C:\path\to\example.jpg"
```

- Base64 image (JSON)
```powershell
curl -X POST http://127.0.0.1:8000/appointments `
   -H "Content-Type: application/json" `
   -d '{"image_base64":"<BASE64_STRING>"}'
```

API contract (high level)
- POST /appointments accepts exactly one input type: `text` OR `image` (multipart) OR `image_base64`.
- Returns either:
   - status `ok` with `pipeline` and `appointment` when successful, or
   - status `needs_clarification` with `pipeline` and `message` when guardrails detect ambiguity, or
   - structured 422/400 errors for invalid inputs (kept compatible with test suite expectations).

Pipeline overview (ASCII)

```
Client -> API -> [OCR (pytesseract)] -> [NLP extraction] -> [Normalization (YYYY-MM-DD + HH:MM)] -> [Guardrails]
                                                                                                                      \-> needs_clarification
                                                                                                                      \-> appointment (ok)
```

Testing

Run the test-suite locally:
```powershell
.\.venv\Scripts\python -m pytest -q
```

Demo assets & publishing
- `scripts/demo_run.ps1` — runs the server and two sample requests and saves outputs.
- `scripts/record_demo.ps1` — ffmpeg-based recording helper (Windows).
- `scripts/publish_to_github.ps1` — helper to push to GitHub (can attempt to create repo via `gh` if installed).

Contributing & support
- See `CONTRIBUTING.md` for contribution guidelines.

Next improvements (ideas)
- Add small demo images and automated integration tests for OCR flows.
- Generate a small animated GIF showing a successful and ambiguous request for the README banner.
- Add a Docker image and publish to GitHub Packages for quick demo deployment.

License
- This project is licensed under the MIT License (see `LICENSE`).

---

If you want, I can also:
- Add a short GIF (30s) to the README, or host a docs page via GitHub Pages that points to the README.
- Add a CONTRIBUTING.md, ISSUE templates, and PR template (I will add them now unless you prefer different wording).