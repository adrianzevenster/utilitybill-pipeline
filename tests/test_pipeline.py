from src.ingest.models import Document
from src.pipeline import process_document


def test_process_document(tmp_path):
    dummy = Document(
        uri=f"file://{tmp_path}/bill.pdf",
        filename="bill.pdf",
        mime_type="application/pdf",
    )
    # Should run without raising
    process_document(dummy)
