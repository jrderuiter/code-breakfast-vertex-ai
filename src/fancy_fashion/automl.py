import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from google.cloud.storage import Client

ML_USE_MAP = {"train": "TRAINING", "test": "TEST"}


@dataclass
class DatasetItem:
    """Class representing an AutoML dataset item."""

    ml_use: str  # How item should be used in the model (should be TRAINING or TEST).
    url: str  # GCS url to the image (e.g. gs://<bucket>/path/to/image.jpg).
    label: str  # Label of the image (e.g. bag, sneaker).


def generate_items_from_bucket(bucket_name: str) -> Iterable[DatasetItem]:
    """Generates a list of train/test dataset items from the given bucket."""

    client = Client()

    for blob in client.list_blobs(bucket_name):
        if (
            blob.name.startswith("train") or blob.name.startswith("test")
        ) and blob.name.endswith(".jpg"):
            ml_use, label, _ = blob.name.split("/")
            url = f"gs://{bucket_name}/{blob.name}"
            yield DatasetItem(ml_use=ML_USE_MAP[ml_use], url=url, label=label)


def write_items_to_csv(dataset_items: Iterable[DatasetItem], output_path: Path):
    """Writes dataset items to a CSV file."""

    with open(output_path, "w", encoding="utf-8") as file_:
        writer = csv.writer(file_, quoting=csv.QUOTE_MINIMAL)

        for item in dataset_items:
            writer.writerow([item.ml_use, item.url, item.label])
