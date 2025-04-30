from typing import Any, Dict, List


def vote_and_merge(
    candidates: List[Dict[str, Dict[str, Any]]]
) -> Dict[str, Dict[str, Any]]:
    """Majority vote on key-value pairs by confidence."""
    result: Dict[str, Dict[str, Any]] = {}

    for cand in candidates:
        for k, v in cand.items():
            if k not in result or v.get("confidence", 0) > result[k].get(
                "confidence", 0
            ):
                result[k] = v
    return result
