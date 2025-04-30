"""
Run the full pipeline on one local file.

$ python -m src.cli.run_pipeline --file /path/to/utility_bill.pdf
"""

import argparse
from pathlib import Path

from src.ingest.loader import create_document
from src.pipeline import process_document


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True, help="PDF or image to process")
    args = parser.parse_args()

    path = Path(args.file).expanduser().resolve()
    if not path.exists():
        raise FileNotFoundError(path)

    doc = create_document(path)
    process_document(doc)


if __name__ == "__main__":  # pragma: no cover
    main()
