# UtilityBill Pipeline

End-to-end service that ingests utility-bill PDFs or images, cleans them, extracts entities with your **custom spaCy + regex extractor** (or optional Document AI / Gemini), validates results, and routes them to BigQuery and the DVS Landing API.  
Kubernetes-ready • Prometheus metrics • CI-friendly offline mode.

---

## 1  Features

| Capability | Notes |
|------------|-------|
| Multi-source ingest | REST (FastAPI), CLI, Pub/Sub / Celery queue |
| Pluggable extractors | **Default:** `src/extract/custom.py` (spaCy + regex)<br>Optional: Document AI, Gemini, Tesseract |
| Confidence routing | `< 95 %` ⇒ human review; bad match ⇒ fraud |
| Dual-mode runs | `PIPELINE_OFFLINE=1` skips all Google calls |
| Observability | Prometheus counters + histogram at `/metrics` |
| Deployment | Dockerfile → GKE Deployment / HPA |
| Tests | `pytest` unit + monitoring suite, pre-commit hooks |

---

## 2  Quick start

```bash
git clone <repo> && cd utilitybill-pipeline
python -m venv .venv && source .venv/bin/activate
pip install -e .            # editable install
pip install spacy pdfplumber pytesseract
python -m spacy download en_core_web_sm
pre-commit install
```
# Offline run (no GCP)

```bash
export PIPELINE_OFFLINE=1 PIPELINE_VERBOSE=1
python -m src.cli.run_pipeline --file <path/to/bill.pdf>
```

# Testing Suite

```bash
python -m pytest 
```

