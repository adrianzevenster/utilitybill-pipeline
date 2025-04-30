import re

METER_REGEX = re.compile(r"\b\d{6}\b")
VIN_REGEX = re.compile(r"\b[A-HJ-NPR-Z\d]{17}\b")

def basic_checks(text: str) -> dict:
    return {
        "meternumber": METER_REGEX.search(text),
        "vin": VIN_REGEX.search(text),
    }
