import random
from typing import Dict


def extract_with_docai(gcs_uri: str) -> Dict:
    """Stub: replace with real Document AI call."""
    return {
        "name": {"value": "Jane Doe", "confidence": random.uniform(0.9, 0.99)},
        "meternumber": {"value": "123456", "confidence": random.uniform(0.9, 0.99)},
    }
