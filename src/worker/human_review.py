from typing import Dict

def enqueue_for_human_review(doc, entities: Dict, score: float) -> None:
    print(f"Queued {doc.filename} for human review (score={score:.2f})")

def flag_fraud(doc, entities: Dict) -> None:
    print(f"Flagged {doc.filename} as potential fraud")
