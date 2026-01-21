from typing import Dict, Any
from fastapi import HTTPException
from src.services.nlp_service import extract_entities, normalize_entities, handle_ambiguity


class AppointmentPipeline:
    """Minimal pipeline used by tests.

    run(text: str) -> Dict[str, Any]
    """

    def run(self, text: str) -> Dict[str, Any]:
        if not isinstance(text, str) or not text.strip():
            raise HTTPException(status_code=422, detail="Text must not be empty.")

        # Step 1: (text input) — already text
        raw_text = text.strip()

        # Step 2: entity extraction
        entities = extract_entities(raw_text)

        # Guardrails: ambiguous or missing required entities
        try:
            handle_ambiguity(entities)
        except ValueError:
            # Tests expect a generic failure message for inability to extract details
            raise HTTPException(status_code=400, detail="Unable to extract appointment details")

        # Step 3: normalization
        normalized = normalize_entities(entities)

        # Build appointment
        appointment = {
            "name": entities.get("name"),
            "date": normalized.get("date"),
            "time": normalized.get("time"),
            "tz": normalized.get("tz"),
        }

        return {"status": "success", "appointment": appointment}