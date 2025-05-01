# tests/test_pipeline.py
from src.ingest.models import Document
from src.pipeline import process_document

TINY_PDF = (
    b"%PDF-1.4\n"
    b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n"
    b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n"
    b"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 10 10] >>\nendobj\n"
    b"xref\n0 4\n0000000000 65535 f \n0000000010 00000 n \n"
    b"0000000072 00000 n \n0000000125 00000 n \n"
    b"trailer\n<< /Size 4 /Root 1 0 R >>\nstartxref\n190\n%%EOF"
)


def test_process_document(tmp_path):
    pdf = tmp_path / "bill.pdf"
    pdf.write_bytes(TINY_PDF)

    doc = Document(
        uri=f"file://{pdf}", filename="bill.pdf", mime_type="application/pdf"
    )
    # Should run without raising
    process_document(doc)
