import os
from celery import Celery

celery_app = Celery(
    "utilitybill",
    broker=os.environ.get("CELERY_BROKER_URL", "redis://redis:6379/0"),
    backend="rpc://",
)
celery_app.conf.task_routes = {"src.worker.tasks.*": {"queue": "documents"}}

@celery_app.task(acks_late=True, autoretry_for=(Exception,), retry_backoff=True)
def handle_document(gcs_uri: str) -> None:
    from pathlib import Path
    from src.ingest.models import Document
    from src.pipeline import process_document

    doc = Document(uri=gcs_uri, filename=Path(gcs_uri).name, mime_type="application/pdf")
    process_document(doc)
