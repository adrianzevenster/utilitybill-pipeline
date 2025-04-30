# src/metrics.py
from prometheus_client import Counter, Histogram

REQUEST_LAT = Histogram(
    "api_request_latency_seconds",
    "Latency of FastAPI HTTP requests",
    buckets=(0.05, 0.1, 0.25, 0.5, 1, 2),
)

DOCS_PROCESSED = Counter("documents_processed_total", "All processed docs")
DOCS_HUMAN_REVIEW = Counter("documents_human_review_total", "Escalated for review")
DOCS_FRAUD = Counter("documents_flagged_fraud_total", "Flagged as fraud")
