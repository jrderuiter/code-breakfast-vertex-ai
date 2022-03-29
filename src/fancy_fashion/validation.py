from typing import Dict, List

import pandas as pd
import tensorflow as tf


def validate_predictions(predictions: List[Dict[str, str]]) -> float:
    """
    :param predictions: A list of Dicts with
        {"filename": "<validation_filename", "prediction": <your_integer_label>}
    :return: Validation accuracy
    """
    predictions_df = pd.DataFrame(predictions)
    validation_set = pd.read_parquet("data/validation.parquet")

    both = validation_set.merge(predictions_df, on="filename")

    metric = tf.keras.metrics.Accuracy()
    metric.update_state(both["label"], both["prediction"])

    return metric.result().numpy()
