import random
import time
from typing import Dict


def enrich_selected(entities: Dict) -> Dict:
    """Call external APIs for subset of entities (stub)."""
    time.sleep(0.1)
    entities["api_status"] = random.choice(["MATCH", "NO_MATCH"])
    return entities
