"""
Central orchestration: transform → extract → validate → route.

Env flags
---------
PIPELINE_OFFLINE=1      # skip GCS + BigQuery, useful for local dev
PIPELINE_VERBOSE=1      # pretty-print extracted entities
PIPELINE_SAVE_JSON=1    # dump entities to ./extracted_results/<file>.json
"""

from __future__ import annotations

import datetime
import json
import os
from pathlib import Path
from pprint import pprint

from src.config import get_settings
from src.enrich.external_api import enrich_selected
from src.extract import extract_entities
from src.ingest.models import Document
from src.metrics import DOCS_FRAUD, DOCS_HUMAN_REVIEW, DOCS_PROCESSED
from src.store.bigquery import save_to_bq
from src.store.dvs_client import enqueue_verification
from src.transform.clean import clean
from src.validate.match import compare
from src.worker.human_review import enqueue_for_human_review, flag_fraud

settings = get_settings()

OFFLINE = os.getenv("PIPELINE_OFFLINE") == "1"
VERBOSE = OFFLINE or os.getenv("PIPELINE_VERBOSE") == "1"
SAVE_JSON = os.getenv("PIPELINE_SAVE_JSON") == "1"


def _maybe_print(entities: dict) -> None:
    if VERBOSE:
        print("🔍  Extracted entities")
        pprint(entities, sort_dicts=False)


def _maybe_save_json(doc: Document, entities: dict) -> None:
    if SAVE_JSON:
        out_dir = Path("extracted_results")
        out_dir.mkdir(exist_ok=True)
        ts = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        out_file = out_dir / f"{doc.filename}.{ts}.json"
        out_file.write_text(json.dumps(entities, indent=2))
        print(f"💾  Saved {out_file.relative_to(Path.cwd())}")


def process_document(doc: Document) -> None:
    """Run the full pipeline for a single document."""
    cleaned_uri = clean(doc)  # deskew / mask / convert
    entities = extract_entities(cleaned_uri)  # DocAI + Gemini + OCR merge
    _maybe_print(entities)
    _maybe_save_json(doc, entities)

    verdict, score = compare(entities)  # business rules
    DOCS_PROCESSED.inc()

    # ------- Branches -------------------------------------------------------
    if score < settings.confidence_threshold:
        DOCS_HUMAN_REVIEW.inc()
        enqueue_for_human_review(doc, entities, score)
        return

    if not verdict:
        DOCS_FRAUD.inc()
        flag_fraud(doc, entities)
    else:
        enriched = enrich_selected(entities)
        enqueue_verification(enriched)

    # -------- Persist -------------------------------------------------------
    save_to_bq(doc, entities, score, verdict)
