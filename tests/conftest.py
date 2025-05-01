# tests/conftest.py
import os

import pytest

# Force every test run to stay offline
os.environ["PIPELINE_OFFLINE"] = "1"


@pytest.fixture(autouse=True)
def offline_cloud_stubs(monkeypatch):
    """Disable all outbound calls inside tests."""
    # BigQuery & DVS originals
    monkeypatch.setattr("src.store.bigquery.save_to_bq", lambda *a, **k: None)
    monkeypatch.setattr("src.store.dvs_client.enqueue_verification", lambda *_: None)
    # Aliases imported into pipeline.py at module-load time
    monkeypatch.setattr("src.pipeline.save_to_bq", lambda *a, **k: None)
    monkeypatch.setattr("src.pipeline.enqueue_verification", lambda *_: None)
    # Default extractor alias (so tests that don’t patch it never hit GCS)
    monkeypatch.setattr(
        "src.pipeline.extract_entities",
        lambda *_: {"dummy": {"value": "x", "confidence": 0.99}},
    )
