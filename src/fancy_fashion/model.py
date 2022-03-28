import tensorflow as tf
from tensorflow.keras import Model, layers, preprocessing
from tensorflow.keras.applications import MobileNet


def train_model(train_data_dir):
    """Trains the model on the given training data."""

    # Not sure why, but we need it
    tf.config.run_functions_eagerly(True)

    model = build_model()
    model.compile(
        optimizer="Adam", loss="categorical_crossentropy", metrics=["accuracy"]
    )

    train_data = preprocessing.image_dataset_from_directory(
        train_data_dir, label_mode="categorical", image_size=(128, 128)
    )
    model.fit(train_data, verbose=1, epochs=2, steps_per_epoch=10)

    return model


def build_model():
    """Builds the model structure."""

    # Start with basic MobileNet model.
    base_model = MobileNet(include_top=False, input_shape=(128, 128, 3))
    for layer in base_model.layers:
        layer.trainable = False

    # Add extra leyers.
    x = base_model.output
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dense(units=512, activation="relu")(x)

    # Add output layers (3 classes: bags, shoes, sneakers)
    predictions = layers.Dense(units=3, activation="softmax")(x)
    model = Model(inputs=base_model.input, outputs=predictions)

    return model


def evaluate_model(model, test_data_dir):
    """Evaluates a given model on a test dataset."""

    test_datagenerator = preprocessing.image_dataset_from_directory(
        test_data_dir, label_mode="categorical", image_size=(128, 128)
    )
    loss, accuracy = model.evaluate(test_datagenerator)

    return loss, accuracy


def generate_predictions(model, predict_data_dir):
    """Generates predictions for a dataset with the given model."""

    predict_data = preprocessing.image_dataset_from_directory(
        predict_data_dir, label_mode=None, image_size=(128, 128)
    )
    predictions = model.predict(predict_data)

    return predictions.argmax(axis=1)
