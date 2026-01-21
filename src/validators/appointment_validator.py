from pydantic import BaseModel, ValidationError, model_validator
from typing import Optional

class AppointmentRequest(BaseModel):
    date: Optional[str] = None
    time: Optional[str] = None
    description: Optional[str] = None
    contact_info: Optional[str] = None

    @model_validator(mode='before')
    @classmethod
    def check_at_least_one_field(cls, data: any):
        if not isinstance(data, dict):
            return data
        if not any(data.get(field_name) for field_name in ['date', 'time', 'description', 'contact_info']):
            raise ValueError('At least one of date, time, description, or contact_info must be provided.')
        return data

def validate_appointment_request(data: dict) -> AppointmentRequest:
    try:
        return AppointmentRequest(**data)
    except ValidationError as e:
        raise ValueError(f"Validation error: {e.errors()}")