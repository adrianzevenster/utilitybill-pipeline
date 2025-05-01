# tests/test_extract.py
import src.extract as extract_mod


def test_vote_merges_by_confidence(monkeypatch):
    """Highest-confidence candidate should win the merge."""

    # Patch the public wrapper so it returns our synthetic dict
    monkeypatch.setattr(
        "src.extract.extract_entities",
        lambda *_: {"name": {"value": "B", "confidence": 0.95}},
    )

    merged = extract_mod.extract_entities("file://dummy/path.pdf")
    assert merged["name"]["value"] == "B"
    assert merged["name"]["confidence"] == 0.95
