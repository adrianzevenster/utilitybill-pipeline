# src/extract/__init__.py
from __future__ import annotations

from pathlib import Path, PurePosixPath
from typing import Dict

from src.extract.custom import extract_custom
from src.ingest.models import Document  # NEW
from src.extract.ocr import local_ocr   # keep or swap for Vision API

def _download_gcs_to_tmp(gcs_uri: str) -> str:
    from google.cloud import storage
    bucket, blob = gcs_uri[5:].split("/", 1)
    tmp = Path("/tmp") / Path(PurePosixPath(blob).name)
    storage.Client().bucket(bucket).blob(blob).download_to_filename(tmp)
    return str(tmp)

def _ensure_local(uri: str) -> str:
    if uri.startswith("file://"):
        return uri[7:]
    if uri.startswith("gs://"):
        return _download_gcs_to_tmp(uri)
    return uri  # already a local path

# ---------- public entry point ---------- #
def extract_entities(doc: Document, cleaned_uri: str) -> Dict:
    """
    Route to the correct extractor based on MIME type.

    Parameters
    ----------
    doc          : Document  (has mime_type)
    cleaned_uri  : file://… or gs://…  returned by transform.clean()

    Returns
    -------
    Dict[str, Dict]  e.g. {'name': {'value': 'Alice', 'confidence': 0.9}}
    """
    local_path = _ensure_local(cleaned_uri)

    if doc.mime_type.startswith("image/"):
        # PRIMARY path for images
        return local_ocr(local_path)

    # default: PDF or other → custom spaCy+regex
    return extract_custom(local_path)
