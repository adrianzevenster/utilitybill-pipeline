import random
from typing import Dict


def local_ocr(gcs_uri: str) -> Dict:
    """Stub local OCR layer."""
    return {
        "name": {"value": "J. Doe", "confidence": random.uniform(0.6, 0.8)},
    }
