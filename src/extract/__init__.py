# src/extract/__init__.py
"""
Expose exactly one public function: `extract_entities(uri_or_path)`,
which returns ONLY the entities produced by our custom extractor.

Google Document AI, Gemini, and Tesseract stubs are no longer used.
"""

from __future__ import annotations

from pathlib import Path, PurePosixPath
from typing import Dict

from .custom import extract_custom


def _download_gcs_to_tmp(gcs_uri: str) -> str:
    """Download a gs:// object to /tmp and return the local path."""
    from google.cloud import storage

    bucket_name, blob_name = gcs_uri[5:].split("/", 1)
    tmp_path = Path("/tmp") / Path(PurePosixPath(blob_name).name)
    storage.Client().bucket(bucket_name).blob(blob_name).download_to_filename(tmp_path)
    return str(tmp_path)


def extract_entities(uri_or_path: str) -> Dict:
    """
    Parameters
    ----------
    uri_or_path : str
        • 'file://<abs-path>'   — produced by offline loader
        • '<local-path>'        — direct path on disk
        • 'gs://bucket/obj'     — downloaded on the fly

    Returns
    -------
    Dict[str, Dict]  like {'name': {'value': 'Alice', 'confidence': 0.91}, ...}
    """
    if uri_or_path.startswith("file://"):
        local_path = uri_or_path[len("file://") :]
    elif uri_or_path.startswith("gs://"):
        local_path = _download_gcs_to_tmp(uri_or_path)
    else:  # assume already a filesystem path
        local_path = uri_or_path

    return extract_custom(local_path)
