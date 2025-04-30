from typing import Dict
import json, time, random

def enqueue_verification(payload: Dict) -> None:
    """Simulate publishing to DVS verification request queue."""
    time.sleep(0.05)
    print("Published to DVS:", json.dumps(payload)[:120], "...")
