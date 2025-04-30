from dataclasses import dataclass


@dataclass
class Document:
    uri: str
    filename: str
    mime_type: str
