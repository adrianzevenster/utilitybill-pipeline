import shutil
import uuid
from pathlib import Path

from fastapi import FastAPI, File, Response, UploadFile
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from src.ingest.loader import create_document
from src.pipeline import process_document

app = FastAPI(title="UtilityBill Pipeline")


@app.post("/ingest")
async def ingest_file(file: UploadFile = File(...)):
    tmp = Path("/tmp") / f"{uuid.uuid4()}_{file.filename}"
    with tmp.open("wb") as f:
        shutil.copyfileobj(file.file, f)
    doc = create_document(tmp)
    process_document(doc)
    return {"status": "accepted", "gcs_uri": doc.uri}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
