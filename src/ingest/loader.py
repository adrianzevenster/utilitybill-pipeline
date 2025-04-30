from pathlib import Path
import mimetypes
from google.cloud import storage
from .models import Document
from src.config import get_settings

settings = get_settings()
gcs = storage.Client(project=settings.gcp_project)
bucket = gcs.bucket(settings.gcs_bucket)

def guess_mime(path: Path) -> str:
    mime, _ = mimetypes.guess_type(path.name)
    return mime or "application/octet-stream"

def upload_to_gcs(local_path: Path, dest_blob: str) -> str:
    blob = bucket.blob(dest_blob)
    blob.upload_from_filename(local_path.as_posix())
    return f"gs://{settings.gcs_bucket}/{dest_blob}"

def create_document(path: Path) -> Document:
    uri = upload_to_gcs(path, f"raw/{path.name}")
    return Document(uri=uri, filename=path.name, mime_type=guess_mime(path))
