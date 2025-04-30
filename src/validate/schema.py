import re

from pydantic import BaseModel, field_validator

_METER_RE = re.compile(r"^\d{6}$")


class UtilityBillEntities(BaseModel):
    name: str
    addressline1: str | None = None
    addressline2: str | None = None
    meternumber: str | None = None
    identification_number: str | None = None
    vin: str | None = None

    @field_validator("meternumber")
    @classmethod
    def _meter_six_digits(cls, v: str | None) -> str | None:
        if v and not _METER_RE.fullmatch(v):
            raise ValueError("Meter number must be exactly six digits")
        return v

    @field_validator("vin")
    @classmethod
    def _vin_upper(cls, v: str | None) -> str | None:
        return v.upper() if v else v
