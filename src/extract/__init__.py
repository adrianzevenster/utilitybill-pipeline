from typing import Dict, List

from .docai_client import extract_with_docai
from .gemini_client import extract_with_gemini
from .ocr import local_ocr
from .utils import vote_and_merge


def extract_entities(gcs_uri: str) -> Dict:
    candidates: List[Dict] = []
    candidates.append(extract_with_docai(gcs_uri))
    try:
        candidates.append(extract_with_gemini(gcs_uri))
    except TimeoutError:
        pass
    candidates.append(local_ocr(gcs_uri))
    return vote_and_merge(candidates)
