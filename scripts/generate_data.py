import random
from pathlib import Path

import pandas as pd
from PIL import Image
from tensorflow.keras.datasets import fashion_mnist

N_TRAIN = 500
N_TEST = 100
N_ACTUAL = 50
TARGET_DIR = Path("data")
TARGET_DIR.mkdir(exist_ok=True)


from fancy_fashion.dataset import REVERSE_MAPPING


def save_images(save_dir: Path, images: list, prefix: str = ""):
    save_dir.mkdir(exist_ok=True, parents=True)
    for ii in range(len(images)):
        image = Image.fromarray(images[ii, :, :].squeeze())
        image.save(save_dir / f"{prefix}{ii}.jpg")


def save_train_test_images(
    target_dir: Path, x, y, label: str, n_train: int, train_or_test: str
):
    is_label = y == REVERSE_MAPPING[label]
    images = x[is_label]
    label_dir = target_dir / train_or_test / label
    save_images(label_dir, images[-n_train:], prefix=label)


def save_actual_images(target_dir: Path, x, y, label: str, n_train: int, prefix: str):
    is_label = y == REVERSE_MAPPING[label]
    images = x[is_label]
    label_dir = target_dir / "actual"
    save_images(label_dir, images[-n_train:], prefix=prefix)


def save_validation_images(target_dir: Path, x, y, labels, n_per_label: int):
    target_dir.mkdir(exist_ok=True, parents=True)

    results = []
    labels_and_images = []

    for label in labels:
        is_label = y == REVERSE_MAPPING[label]
        images = x[is_label]
        images = images[-n_per_label:]
        for image in images:
            image = Image.fromarray(image[:, :].squeeze())
            labels_and_images.append((label, image))
    random.shuffle(labels_and_images)

    for i, (label, image) in enumerate(labels_and_images):
        filename = f"{i}.jpg"
        image.save(target_dir / filename)
        results.append(
            {
                "filename": filename,
                "label": REVERSE_MAPPING[label],
            }
        )

    df = pd.DataFrame(results)
    df.to_parquet(TARGET_DIR / "validation.parquet")


if __name__ == "__main__":
    (x_train, y_train), (x_test, y_test) = fashion_mnist.load_data()

    # Confuse others by using test as train images.
    train_labels = ["shirt", "sneaker", "bag"]
    test_labels = ["shirt", "sneaker", "bag"]
    validation_labels = ["shirt", "sneaker", "bag", "dress"]

    print("Generating train data...")
    for train_label in train_labels:
        save_train_test_images(
            TARGET_DIR, x_train, y_train, train_label, N_TRAIN, train_or_test="train"
        )

    print("Generating test data...")
    for test_label in test_labels:
        save_train_test_images(
            TARGET_DIR, x_test, y_test, test_label, N_TEST, train_or_test="test"
        )

    print("Generating validation data...")
    n_per_actual_label = len(validation_labels) // N_ACTUAL
    save_validation_images(
        TARGET_DIR / "validation",
        x_test,
        y_test,
        labels=validation_labels,
        n_per_label=10,
    )

    print("Done!")
