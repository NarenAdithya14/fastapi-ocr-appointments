import pytest
from fastapi import HTTPException
from src.pipelines.appointment_pipeline import AppointmentPipeline

def test_appointment_pipeline_success():
    # Arrange
    input_data = "Schedule a meeting with John Doe on March 10th at 3 PM"
    pipeline = AppointmentPipeline()

    # Act
    result = pipeline.run(input_data)

    # Assert
    assert result['status'] == 'success'
    assert 'appointment' in result
    assert result['appointment']['name'] == 'John Doe'
    assert result['appointment']['date'] == '2023-03-10'
    assert result['appointment']['time'] == '15:00'

def test_appointment_pipeline_failure():
    # Arrange
    input_data = "Invalid appointment request"
    pipeline = AppointmentPipeline()

    # Act & Assert
    with pytest.raises(HTTPException) as exc_info:
        pipeline.run(input_data)
    assert exc_info.value.status_code == 400
    assert "Unable to extract appointment details" in str(exc_info.value.detail)