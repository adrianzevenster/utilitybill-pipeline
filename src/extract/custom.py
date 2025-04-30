# src/extract/custom.py
"""
Custom entity extractor
-----------------------

* Regex for meter number (six digits)
* Regex for VIN 17-char code
* spaCy transformer model for PERSON (full name)

Add more rules or model logic as needed.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Dict

import spacy

# ---------- static patterns ----------
METER_RE = re.compile(r"\b(\d{6})\b")
VIN_RE = re.compile(r"\b[A-HJ-NPR-Z\d]{17}\b")

# ---------- spaCy model (loaded once) ----------
# choose a light model for dev; swap to "en_core_web_trf" for highest accuracy
_NLP = spacy.load("en_core_web_sm")  # 13 MB, no GPU needed

# optional: add confidence-like score for v3.7+ models
try:
    from spacy.scorer import Scorer

    SCORER = Scorer()
except Exception:  # pragma: no cover
    SCORER = None


def _extract_name(text: str) -> tuple[str, float] | None:
    """Return (name, conf) or None."""
    doc = _NLP(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            # crude heuristic: require at least two tokens (first + last name)
            if len(ent.text.split()) >= 2:
                conf = getattr(ent, "kb_id_", None)
                # spaCy small models don't give per-ent confidence, so fallback
                return ent.text.title(), float(conf or 0.85)
    return None


def _load_text(file_path: str) -> str:
    """PDF → text, else OCR image → text."""
    if file_path.lower().endswith(".pdf"):
        import pdfplumber

        with pdfplumber.open(file_path) as pdf:
            return "\n".join(p.extract_text() or "" for p in pdf.pages)
    else:
        import pytesseract

        return pytesseract.image_to_string(Path(file_path))


def extract_custom(file_path: str) -> Dict[str, Dict]:
    """
    Parameters
    ----------
    file_path : str   absolute path on disk

    Returns
    -------
    dict[label] = {"value": str, "confidence": float}
    """
    text = _load_text(file_path)
    entities: Dict[str, Dict] = {}

    # ---------- regex patterns ----------
    if m := METER_RE.search(text):
        entities["meternumber"] = {"value": m.group(1), "confidence": 0.80}
    if m := VIN_RE.search(text):
        entities["vin"] = {"value": m.group(0), "confidence": 0.80}

    # ---------- spaCy PERSON ----------
    if res := _extract_name(text):
        name, conf = res
        entities["name"] = {"value": name, "confidence": conf}

    return entities
