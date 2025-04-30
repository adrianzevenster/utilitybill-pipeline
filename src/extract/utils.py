from typing import Dict, List

def vote_and_merge(candidates: List[Dict]) -> dict:
    """Majority vote on key-value pairs by confidence."""
    result = {}
    for cand in candidates:
        for k, v in cand.items():
            if k not in result or v["confidence"] > result[k]["confidence"]:
                result[k] = v
    return result
