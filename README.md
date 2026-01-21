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

2. **Create a virtual environment:**
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```
   uvicorn src.main:app --reload
   ```

## API Usage

### POST /appointments

This endpoint accepts appointment requests and processes them through the OCR and NLP pipeline.

**Request Body:**
- The request should contain the necessary details for the appointment, which will be validated and processed.

**Response:**
- On success, the response will include the scheduled appointment details.
- In case of validation errors, appropriate error messages will be returned.

## Architecture Overview

The application follows a modular architecture, separating concerns into different components such as services, pipelines, and validators. This design promotes maintainability and scalability.

## Pipeline Explanation

The appointment scheduling pipeline consists of the following stages:
1. **OCR Processing:** Extracts text from images using OCR.
2. **Entity Extraction:** Identifies relevant details such as date, time, and purpose of the appointment.
3. **Normalization:** Standardizes the extracted data for consistency.
4. **Validation:** Ensures that the input adheres to the specified rules.

## Guardrail Behavior

The application includes guardrails to handle ambiguous inputs and ensure that only valid appointment requests are processed. This helps in maintaining the integrity of the scheduling system.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.