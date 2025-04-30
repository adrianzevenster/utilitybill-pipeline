# tests/conftest.py
import pytest


@pytest.fixture(autouse=True)
def offline_cloud_stubs(monkeypatch):
    """
    Disable outbound calls during tests:
      * BigQuery insert
      * DVS queue publish
    """
    # Stub the original implementations …
    monkeypatch.setattr("src.store.bigquery.save_to_bq", lambda *a, **k: None)
    monkeypatch.setattr("src.store.dvs_client.enqueue_verification", lambda *_: None)

    # …and stub the *aliases* that src.pipeline imported at module load.
    monkeypatch.setattr("src.pipeline.save_to_bq", lambda *a, **k: None)
    monkeypatch.setattr("src.pipeline.enqueue_verification", lambda *_: None)
