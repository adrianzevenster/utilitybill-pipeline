from functools import lru_cache

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    gcp_project: str = Field("demo-project", env="GCP_PROJECT")
    gcs_bucket: str = Field("utilitybill-bucket", env="GCS_BUCKET")
    docai_processor_id: str = Field("000000000000000", env="DOCAI_PROCESSOR_ID")
    gemini_model: str = "models/gemini-pro-vision"
    bq_dataset: str = "kyc_raw"
    confidence_threshold: float = 0.95
    external_api_timeout: int = 3
    max_workers: int = 4

    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache
def get_settings() -> Settings:  # pragma: no cover
    return Settings()
