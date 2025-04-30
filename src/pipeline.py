from src.config import get_settings
from src.enrich.external_api import enrich_selected
from src.extract import extract_entities
from src.ingest.models import Document
from src.store.bigquery import save_to_bq
from src.store.dvs_client import enqueue_verification
from src.transform.clean import clean
from src.validate.match import compare
from src.worker.human_review import enqueue_for_human_review, flag_fraud

settings = get_settings()


def process_document(doc: Document) -> None:
    cleaned_uri = clean(doc)
    entities = extract_entities(cleaned_uri)
    verdict, score = compare(entities)

    if score < settings.confidence_threshold:
        enqueue_for_human_review(doc, entities, score)
        return

    if verdict:
        enriched = enrich_selected(entities)
        enqueue_verification(enriched)
    else:
        flag_fraud(doc, entities)

    save_to_bq(doc, entities, score, verdict)
