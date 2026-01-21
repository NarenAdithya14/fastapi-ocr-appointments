from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AppointmentRequest(BaseModel):
    text: str

class AppointmentResponse(BaseModel):
    appointment_id: str
    date: datetime
    time: str
    description: Optional[str] = None
    status: str

class ErrorResponse(BaseModel):
    detail: str