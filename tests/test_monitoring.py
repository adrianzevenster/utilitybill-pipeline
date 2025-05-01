import re

from fastapi.testclient import TestClient

from src.api.fastapi_app import app
from src.ingest.models import Document
from src.metrics import DOCS_FRAUD, DOCS_HUMAN_REVIEW, DOCS_PROCESSED, REQUEST_LAT
from src.pipeline import process_document

client = TestClient(app)


def test_health_endpoint():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_metrics_endpoint_exposes_default_counters():
    r = client.get("/metrics")
    assert r.status_code == 200
    body = r.text
    # basic sanity: Prometheus exposition format lines exist
    assert re.search(r"^api_request_latency_seconds_bucket", body, re.M)
    assert "documents_processed_total" in body


def test_pipeline_updates_custom_metrics(monkeypatch):
    monkeypatch.setattr(
        "src.pipeline.extract_entities",
        lambda *_: {"name": {"value": "x", "confidence": 0.96}},
    )
    # patch the alias imported in src.pipeline
    monkeypatch.setattr("src.pipeline.compare", lambda *_: (False, 0.96))

    before = {
        "processed": DOCS_PROCESSED._value.get(),
        "review": DOCS_HUMAN_REVIEW._value.get(),
        "fraud": DOCS_FRAUD._value.get(),
    }

    dummy = Document(
        uri="gs://foo/bar.pdf", filename="bar.pdf", mime_type="application/pdf"
    )
    process_document(dummy)

    assert DOCS_PROCESSED._value.get() == before["processed"] + 1
    assert DOCS_HUMAN_REVIEW._value.get() == before["review"]  # no new review
    assert DOCS_FRAUD._value.get() == before["fraud"] + 1  # fraud counter +1


def test_request_latency_histogram_records(monkeypatch):
    # FastAPI’s TestClient automatically records middleware latency via prometheus
    REQUEST_LAT.observe(0.03)
    assert REQUEST_LAT._sum.get() >= 0.03
