# tests/test_extract.py


from src.extract import extract_entities


def test_vote_merges_by_confidence(monkeypatch):
    """Highest-confidence candidate should win the merge."""

    # Patch the *symbols that extract_entities actually calls*.
    monkeypatch.setattr(
        "src.extract.extract_with_docai",
        lambda gcs: {"name": {"value": "A", "confidence": 0.90}},
    )
    monkeypatch.setattr(
        "src.extract.extract_with_gemini",
        lambda gcs: {"name": {"value": "B", "confidence": 0.95}},
    )
    monkeypatch.setattr(
        "src.extract.local_ocr",
        lambda gcs: {"name": {"value": "C", "confidence": 0.60}},
    )

    merged = extract_entities("gs://dummy/file.pdf")
    assert merged["name"]["value"] == "B"  # the highest-confidence one
    assert merged["name"]["confidence"] == 0.95
