from matplotlib import pyplot as plt


def local_gcs_path(url_or_path: str):
    """Converts a GCS url or path to a local GCS path if needed."""

    if url_or_path.startswith("gs://"):
        gcs_path = url_or_path.replace("gs://", "/gcs/")
    elif url_or_path.startswith("/gcs"):
        gcs_path = url_or_path
    else:
        raise ValueError(
            f"Unexpected value '{url_or_path}', does not start with gs:// or /gcs"
        )

    return gcs_path


def show_sample(sample):
    """
    Plot an individual image from the dataset.

    Example
    -------
    train_batch, _ = next(train_datagenerator.as_numpy_iterator())
    show_sample(train_batch[0])
    """

    fig, axes = plt.subplots()
    plt.imshow(sample.astype(int))
    plt.show()

    return fig, axes
