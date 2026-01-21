from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from typing import Dict, Any

router = APIRouter()


@router.post("/clarify", status_code=200)
async def clarify_appointment(payload: Dict[str, Any]):
    """Accept a pipeline + appointment object and a `corrections` dict.

    This endpoint is intentionally lightweight: it performs a shallow merge of
    the provided `corrections` into the appointment, validates basic shape,
    and returns the merged appointment. It's useful as a follow-up endpoint
    when the pipeline returns `needs_clarification`.
    """
    pipeline = payload.get("pipeline")
    appointment = payload.get("appointment")
    corrections = payload.get("corrections") or {}

    if not pipeline or not appointment:
        raise HTTPException(status_code=422, detail="pipeline and appointment required")

    if not isinstance(corrections, dict):
        raise HTTPException(status_code=422, detail="corrections must be a dict")

    # Shallow merge corrections into appointment
    merged = dict(appointment)
    for k, v in corrections.items():
        # Only allow certain fields to be corrected for safety
        if k in ("date", "time", "department", "name", "tz"):
            merged[k] = v

    # Return the merged appointment and echo the original pipeline for context
    return JSONResponse(status_code=200, content={"status": "ok", "pipeline": pipeline, "appointment": merged})
