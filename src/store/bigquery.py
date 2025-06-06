import os
from typing import Dict

from google.cloud import bigquery

from src.config import get_settings

OFFLINE = os.getenv("PIPELINE_OFFLINE") == "1"

settings = get_settings()
client = bigquery.Client(project=settings.gcp_project)
table_id = f"{settings.gcp_project}.{settings.bq_dataset}.utilitybill"


def save_to_bq(doc, entities: Dict, score: float, verdict: bool) -> None:
    """Insert one row into BigQuery (stream)."""

    if OFFLINE:
        print(
            "[offline] would write BQ row:",
            {"filename": doc.filename, "verdict": verdict, "score": score},
        )
        return

    row = {
        "uri": doc.uri,
        "filename": doc.filename,
        "entities": {k: v["value"] for k, v in entities.items()},
        "score": score,
        "verdict": verdict,
    }
    errors = client.insert_rows_json(table_id, [row])
    if errors:
        print("BQ errors:", errors)
