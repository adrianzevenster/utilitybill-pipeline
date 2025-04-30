import random
import time
from typing import Dict


def extract_with_gemini(gcs_uri: str) -> Dict:
    """Stub: pretend to call Gemini Vision."""
    time.sleep(0.2)  # latency simulation
    if random.random() < 0.2:
        raise TimeoutError("Gemini timeout")
    return {
        "name": {"value": "Jane Doe", "confidence": random.uniform(0.85, 0.95)},
        "addressline1": {
            "value": "123 Main St",
            "confidence": random.uniform(0.85, 0.95),
        },
    }
