from typing import List, Dict
import pytesseract
from PIL import Image
import numpy as np
from io import BytesIO

class OCRService:
    def __init__(self):
        pass

    def extract_text(self, image: Image.Image) -> str:
        """Extract text from an image using pytesseract."""
        return pytesseract.image_to_string(image)

    def extract_text_with_confidence(self, image: Image.Image) -> Dict[str, any]:
        """Extract text and compute a simple confidence score using pytesseract's image_to_data."""
        data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
        texts = []
        confs = []
        for t, c in zip(data.get('text', []), data.get('conf', [])):
            if t and t.strip():
                texts.append(t)
                try:
                    confs.append(int(c))
                except Exception:
                    pass
        raw_text = " ".join(texts)
        confidence = (sum(confs) / len(confs) / 100.0) if confs else 0.0
        return {"raw_text": raw_text, "confidence": round(confidence, 2)}

    def normalize_noise(self, image: Image.Image) -> Image.Image:
        """Normalize noise in the image for better OCR results."""
        # Convert image to grayscale
        gray_image = image.convert('L')
        # Apply thresholding or other noise reduction techniques if necessary
        # For simplicity, we will return the grayscale image
        return gray_image

    def process_image(self, image_path: str) -> str:
        """Process the image to extract text."""
        image = Image.open(image_path)
        normalized_image = self.normalize_noise(image)
        extracted_text = self.extract_text(normalized_image)
        return extracted_text

    def extract_text_from_bytes(self, image_bytes: bytes) -> Dict[str, any]:
        """Open image from bytes and return extracted text and confidence."""
        image = Image.open(BytesIO(image_bytes)).convert("RGB")
        normalized_image = self.normalize_noise(image)
        # Try to get text with confidence
        try:
            result = self.extract_text_with_confidence(normalized_image)
            if result["raw_text"].strip():
                return result
        except Exception:
            pass
        # Fallback to plain extraction
        text = self.extract_text(normalized_image)
        return {"raw_text": text, "confidence": 0.0}