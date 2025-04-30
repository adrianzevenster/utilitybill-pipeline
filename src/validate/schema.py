from pydantic import BaseModel, Field, constr, validator

class UtilityBillEntities(BaseModel):
    name: str
    addressline1: str | None = None
    addressline2: str | None = None
    meternumber: constr(regex=r"^\d{6}$") | None = None
    identification_number: str | None = None
    vin: str | None = None

    @validator("vin")
    def vin_upper(cls, v):
        return v.upper() if v else v
