from typing import Dict, Tuple


def compare(entities: Dict) -> Tuple[bool, float]:
    """Return verdict and confidence score (dummy for now)."""
    score = min(v["confidence"] for v in entities.values())
    verdict = score >= 0.9
    return verdict, score
