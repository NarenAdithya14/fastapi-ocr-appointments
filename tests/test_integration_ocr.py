import base64
import tempfile
import os
import pytest

try:
    import pytesseract
    from pytesseract import TesseractNotFoundError
    from PIL import Image
except Exception:
    pytesseract = None
    TesseractNotFoundError = None


def _write_sample_png(path: str):
    # A tiny 1x1 PNG (black) encoded in base64
    data_b64 = (
        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR4nGNgYAAAAAMA" 
        "ASsJTYQAAAAASUVORK5CYII="
    )
    with open(path, "wb") as f:
        f.write(base64.b64decode(data_b64))


@pytest.mark.skipif(pytesseract is None, reason="pytesseract or PIL not installed")
def test_integration_ocr_on_fixture():
    """Attempt to run pytesseract on a tiny fixture image.

    This test is intentionally tolerant: it will only assert that OCR runs
    without raising an exception. In CI environments without Tesseract
    binary installed this test will be skipped.
    """
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "sample.png")
        _write_sample_png(p)
        # Ensure the tesseract binary is available; if not, skip the test
        try:
            _ = pytesseract.get_tesseract_version()
        except Exception:
            pytest.skip("Tesseract binary not available on PATH; skipping integration OCR test")

        img = Image.open(p)
        # Run OCR (may return empty string) but should not raise
        text = pytesseract.image_to_string(img)
        assert isinstance(text, str)
