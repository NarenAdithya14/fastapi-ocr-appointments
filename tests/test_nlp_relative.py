from datetime import date
from src.pipelines.appointment_pipeline import AppointmentPipeline


def test_relative_next_friday():
    # Reference date chosen so that next Friday maps to 2025-09-26
    ref = date(2025, 9, 19)  # Friday is 2025-09-19, next Friday should be 2025-09-26
    pipeline = AppointmentPipeline()
    input_data = "Book dentist next Friday at 3pm"

    result = pipeline.run(input_data, ref_date=ref)

    assert result["status"] == "success"
    appt = result["appointment"]
    assert appt["department"] is None or appt["department"] in ("Dentistry", "dentistry")
    # date should be the next Friday
    assert appt["date"] == "2025-09-26"
    assert appt["time"] == "15:00"
