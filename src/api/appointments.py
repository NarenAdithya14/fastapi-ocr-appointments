from fastapi import APIRouter, HTTPException, File, UploadFile, Request
from typing import Optional, Dict, Any
from uuid import uuid4
from datetime import datetime
from zoneinfo import ZoneInfo
from fastapi.responses import JSONResponse
from src.pipelines.appointment_pipeline import AppointmentPipeline
from src.services.nlp_service import (
    extract_entities,
    handle_ambiguity,
    normalize_entities,
    normalize_ocr_noise,
)
from src.services.ocr_service import OCRService
import base64

router = APIRouter()

# For compatibility, expose a clarify endpoint on the same /appointments router
try:
    from src.api.clarify import clarify_appointment as _clarify_handler

    @router.post("/clarify", status_code=200)
    async def clarify_proxy(payload: Dict[str, Any]):
        """Proxy to the lightweight clarify handler in `src.api.clarify`.

        This ensures `/appointments/clarify` is reachable whether the clarify
        router is mounted separately or not (helps tests/consumers).
        """
        return await _clarify_handler(payload)
except Exception:
    # If import fails, skip creating the proxy; the separate router may be used instead
    pass


@router.post("", status_code=200)
async def create_appointment(request: Request, image: Optional[UploadFile] = File(None)):
    """Accept exactly one of: text (JSON), image (multipart), image_base64 (JSON).

    Behavior compatibility notes:
    - When a JSON `text` is provided we return the simple response expected by tests: {appointment_id, appointment}
    - For image or base64 inputs the endpoint returns the full `pipeline` object + `appointment` per the assignment.
    """
    content_type = request.headers.get("content-type", "")
    is_json = "application/json" in content_type

    # Parse inputs
    payload_text = None
    payload_base64 = None
    ocr_info: Dict[str, Any] = {"raw_text": "", "confidence": 0.0}
    source_text: Optional[str] = None

    ocr_service = OCRService()

    if "multipart/form-data" in content_type:
        # form: text may be a form field and file in `image`
        form = await request.form()
        payload_text = form.get("text")
        if image is not None:
            allowed = {"image/png", "image/jpeg", "image/jpg"}
            if image.content_type not in allowed:
                return JSONResponse(status_code=400, content={"status": "error", "message": "Invalid input format"})
            content = await image.read()
            if len(content) > 5 * 1024 * 1024:
                return JSONResponse(status_code=400, content={"status": "error", "message": "Invalid input format"})
            ocr_info = ocr_service.extract_text_from_bytes(content)
            source_text = ocr_info.get("raw_text", "")
    else:
        # assume JSON
        try:
            body = await request.json()
        except Exception:
            body = {}
        # Distinguish presence of keys vs None/empty values to satisfy tests
        has_text_key = "text" in body
        has_base64_key = "image_base64" in body
        if is_json and not has_text_key and not has_base64_key:
            # API should return 422 Field required when JSON body has no relevant keys
            return JSONResponse(status_code=422, content={
                "detail": [{"loc": ["body", "text"], "msg": "Field required.", "type": "value_error"}]
            })
        payload_text = body.get("text")
        payload_base64 = body.get("image_base64")
        # store presence flags for later logic
        json_has_text = has_text_key
        json_has_base64 = has_base64_key

    # Exactly one input must be present
    if is_json:
        # Count keys provided in JSON (text or image_base64)
        provided_count = sum(1 for k in ("text", "image_base64") if k in (body if 'body' in locals() else {}))
    else:
        provided_count = sum(1 for v in (payload_text, payload_base64, image) if v)

    if provided_count != 1:
        return JSONResponse(status_code=400, content={"status": "error", "message": "Invalid input format"})

    # Handle the provided input
    if is_json:
        # JSON-specific presence handling to match tests
        if json_has_text:
            # text key present (may be empty)
            if not isinstance(payload_text, str) or not payload_text.strip():
                return JSONResponse(status_code=422, content={
                    "detail": [{"loc": ["body", "text"], "msg": "Text must not be empty.", "type": "value_error"}]
                })
            source_text = payload_text
            ocr_info = {"raw_text": source_text, "confidence": 1.0}
        elif json_has_base64:
            # base64 path (JSON)
            try:
                decoded = base64.b64decode(payload_base64)
            except Exception:
                return JSONResponse(status_code=400, content={"status": "error", "message": "Invalid input format"})
            if len(decoded) > 5 * 1024 * 1024:
                return JSONResponse(status_code=400, content={"status": "error", "message": "Invalid input format"})
            ocr_info = ocr_service.extract_text_from_bytes(decoded)
            source_text = ocr_info.get("raw_text", "")
        else:
            # Shouldn't reach here due to earlier checks
            return JSONResponse(status_code=400, content={"status": "error", "message": "Invalid input format"})
    else:
        # multipart/form-data path (image already handled above)
        pass

    # Normalize OCR noise
    cleaned = normalize_ocr_noise(source_text)

    # reference date for relative parsing (Asia/Kolkata)
    try:
        ref_dt = datetime.now(ZoneInfo("Asia/Kolkata")).date()
    except Exception:
        # If tz data not available, fall back to naive local date
        ref_dt = datetime.now().date()

    # Extract entities
    entities = extract_entities(cleaned)
    # Compute more granular confidences using heuristics in nlp_service
    try:
        from src.services.nlp_service import score_entities, score_normalization

        entities_confidence = score_entities(entities, ocr_info.get("confidence", 1.0))
    except Exception:
        # fallback to previous heuristic
        ent_conf_vals = [0.9 if entities.get(k) else 0.0 for k in ("date_phrase", "time_phrase", "department")]
        entities_confidence = round(sum(ent_conf_vals) / max(len(ent_conf_vals), 1), 2)

    # Guardrails
    try:
        handle_ambiguity(entities)
    except ValueError as e:
        # Unified response: return pipeline partial and needs_clarification for any input
        pipeline = {"ocr": ocr_info, "entities": {"entities": entities, "entities_confidence": entities_confidence}, "normalization": {}}
        return JSONResponse(status_code=400, content={
            "pipeline": pipeline,
            "status": "needs_clarification",
            "message": str(e),
        })

    # Normalization
    normalized = normalize_entities(entities, ref_date=ref_dt)
    try:
        norm_conf = score_normalization(entities, normalized)
    except Exception:
        norm_conf = 0.9 if normalized.get("date") and normalized.get("time") else 0.0

    pipeline = {
        "ocr": ocr_info,
        "entities": {"entities": entities, "entities_confidence": entities_confidence},
        "normalization": {"normalized": normalized, "normalization_confidence": norm_conf},
    }

    # Build final appointment
    if normalized.get("date") and normalized.get("time"):
        # department from extract_entities is already canonicalized when possible
        department = entities.get("department")
        appointment = {"department": department, "date": normalized.get("date"), "time": normalized.get("time"), "tz": normalized.get("tz")}
    else:
        # Shouldn't happen because guardrails would have caught earlier
        if payload_text and is_json:
            raise HTTPException(status_code=400, detail="Unable to extract appointment details")
        return JSONResponse(status_code=400, content={"status": "error", "message": "Unable to extract appointment details"})

    # Unified response for all input types: return pipeline + appointment + status
    return JSONResponse(status_code=200, content={"pipeline": pipeline, "appointment": appointment, "status": "ok"})