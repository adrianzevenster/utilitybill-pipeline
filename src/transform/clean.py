import re

from src.ingest.models import Document


def mask_pii(text: str) -> str:
    # Example: mask SA ID numbers (13 digits) except last 4
    def repl(m):
        return "*" * 9 + m.group(0)[-4:]

    return re.sub(r"\b\d{13}\b", repl, text)


def clean(doc: Document) -> str:
    """Placeholder: copy the GCS URI into a processed folder (noop).
    Returns new GCS URI string."""
    # TODO: deskew images, denoise, convert PDF→PNG, then upload.
    return doc.uri.replace("/raw/", "/processed/")
