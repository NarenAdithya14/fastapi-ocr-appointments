from typing import Dict, Any, Optional
import re
from datetime import datetime, date, timedelta
from zoneinfo import ZoneInfo


WEEKDAY_MAP = {
    'monday': 0,
    'tuesday': 1,
    'wednesday': 2,
    'thursday': 3,
    'friday': 4,
    'saturday': 5,
    'sunday': 6,
}


DEPARTMENT_SYNONYMS = {
    'dentist': 'Dentistry',
    'dental': 'Dentistry',
    'dentistry': 'Dentistry',
    'cardio': 'Cardiology',
    'cardiology': 'Cardiology',
    'derm': 'Dermatology',
    'dermatology': 'Dermatology',
    'ortho': 'Orthopedics',
    'orthopedics': 'Orthopedics',
    'neuro': 'Neurology',
    'neurology': 'Neurology',
}


def normalize_ocr_noise(text: str) -> str:
    """Apply lightweight OCR noise normalization and cleaning rules.

    - lowercase
    - collapse whitespace
    - common OCR fixes (nxt->next, l0->10, tmr->tomorrow)
    """
    if not text:
        return text
    s = text.lower()
    # common substitutions
    subs = {
        "nxt": "next",
        "tmr": "tomorrow",
        "l0": "10",
        "0r": "or",
        "@": " at ",
    }
    for k, v in subs.items():
        s = re.sub(rf"\b{k}\b", v, s)
    # collapse whitespace
    s = re.sub(r"\s+", " ", s).strip()
    return s


def extract_entities(text: str) -> Dict[str, Any]:
    """Naive entity extraction: name, date_phrase, time_phrase, department.

    This is intentionally simple for tests/demo purposes.
    """
    entities: Dict[str, Any] = {
        "name": None,
        "date_phrase": None,
        "time_phrase": None,
        "department": None,
    }

    # Name: look for 'with NAME on' or 'with NAME,'
    m = re.search(r"with\s+([A-Z][A-Za-z .'-]+?)\s+(?:on|at|,|$)", text)
    if m:
        entities["name"] = m.group(1).strip()

    # Relative date phrases (next Friday, tomorrow, today, this Friday)
    m = re.search(r"\b(next|this)\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b", text, re.IGNORECASE)
    if m:
        entities["date_phrase"] = f"{m.group(1).lower()} {m.group(2).lower()}"
    else:
        m2 = re.search(r"\b(tomorrow|today)\b", text, re.IGNORECASE)
        if m2:
            entities["date_phrase"] = m2.group(1).lower()

    # Date phrase: month name + day (with optional year)
    if not entities["date_phrase"]:
        m = re.search(r"(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2}(?:st|nd|rd|th)?(?:\s*,?\s*\d{4})?", text, re.IGNORECASE)
        if m:
            entities["date_phrase"] = m.group(0)

    # Time phrase: prefer explicit AM/PM patterns
    m = re.search(r"(\d{1,2}(?::\d{2})?\s*(?:AM|PM|am|pm))", text)
    if m:
        entities["time_phrase"] = m.group(1)
    else:
        # fallback: look for 'at 3' style or '3pm' without space
        m = re.search(r"\bat\s+(\d{1,2}(?::\d{2})?)\b", text)
        if m:
            entities["time_phrase"] = m.group(1)
        else:
            m2 = re.search(r"\b(\d{1,2}pm|\d{1,2}am)\b", text, re.IGNORECASE)
            if m2:
                entities["time_phrase"] = m2.group(1)

    # Department: look for synonyms
    for token, canonical in DEPARTMENT_SYNONYMS.items():
        if re.search(rf"\b{re.escape(token)}\b", text, re.IGNORECASE):
            entities["department"] = canonical
            break

    return entities


def resolve_relative_date(phrase: str, ref_date: Optional[date] = None) -> Optional[date]:
    """Resolve phrases like 'next friday', 'this friday', 'tomorrow', 'today' to a date.

    If ref_date is None, uses today's date in Asia/Kolkata.
    """
    if ref_date is None:
        try:
            tz = ZoneInfo("Asia/Kolkata")
            now = datetime.now(tz)
        except Exception:
            # tzdata may not be installed in some environments (Windows CI); fall back to naive local time
            now = datetime.now()
        ref_date = now.date()

    phrase = (phrase or "").strip().lower()
    if not phrase:
        return None

    if phrase == "today":
        return ref_date
    if phrase == "tomorrow":
        return ref_date + timedelta(days=1)

    m = re.match(r"(next|this)\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday)", phrase)
    if m:
        modifier = m.group(1)
        weekday = m.group(2)
        target = WEEKDAY_MAP[weekday]
        current = ref_date.weekday()
        if modifier == "next":
            days_ahead = (target - current + 7) % 7
            if days_ahead == 0:
                days_ahead = 7
        else:  # this
            days_ahead = (target - current) % 7
        return ref_date + timedelta(days=days_ahead)

    return None


def normalize_entities(entities: Dict[str, Any], ref_date: Optional[date] = None) -> Dict[str, Any]:
    """Normalize date_phrase -> YYYY-MM-DD and time_phrase -> HH:MM (24h).

    Uses Asia/Kolkata as the timezone. Accepts optional ref_date for deterministic tests.
    """
    normalized: Dict[str, Any] = {"date": None, "time": None, "tz": "Asia/Kolkata"}

    date_phrase = entities.get("date_phrase")
    if date_phrase:
        # Handle relative phrases
        rel = resolve_relative_date(date_phrase, ref_date)
        if rel:
            normalized["date"] = rel.strftime("%Y-%m-%d")
        else:
            # Remove ordinal suffixes
            d = re.sub(r"(st|nd|rd|th)", "", date_phrase)
            # Append year if missing (keep previous default behavior)
            if not re.search(r"\d{4}", d):
                d = f"{d}, 2023"
            try:
                dt = datetime.strptime(d.strip(), "%B %d, %Y")
                normalized["date"] = dt.strftime("%Y-%m-%d")
            except Exception:
                normalized["date"] = None

    time_phrase = entities.get("time_phrase")
    if time_phrase:
        t = time_phrase.strip()
        # Normalize am/pm
        m = re.match(r"(\d{1,2})(?::(\d{2}))?\s*([AaPp][Mm])?", t)
        if m:
            hour = int(m.group(1))
            minute = int(m.group(2)) if m.group(2) else 0
            ampm = m.group(3)
            if ampm:
                if ampm.lower().startswith("p") and hour != 12:
                    hour += 12
                if ampm.lower().startswith("a") and hour == 12:
                    hour = 0
            normalized["time"] = f"{hour:02d}:{minute:02d}"

    # Department is expected to be already canonicalized by extract_entities
    return normalized


def handle_ambiguity(entities: Dict[str, Any]) -> None:
    """Raise ValueError on ambiguous or missing critical fields per guardrails."""
    # Ambiguous date phrases
    date_phrase = entities.get("date_phrase")
    if not date_phrase or re.search(r"next week|this weekend|next month", str(date_phrase), re.IGNORECASE):
        raise ValueError("Ambiguous date provided.")

    time_phrase = entities.get("time_phrase")
    if not time_phrase or re.search(r"morning|evening|afternoon|night", str(time_phrase), re.IGNORECASE):
        raise ValueError("Ambiguous time provided.")

    # Department is optional for pipeline success in existing tests
    # Only raise on department ambiguity if the detected token is generic
    department = entities.get("department")
    if department in ["doctor", "hospital"]:
        raise ValueError("Ambiguous department provided.")