from pathlib import Path

import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras import Model, layers, preprocessing
from tensorflow.keras.applications import MobileNet

TARGET_DIR = Path("data")

# Not sure why, but we need it
tf.config.run_functions_eagerly(True)


base_model = MobileNet(include_top=False, input_shape=(128, 128, 3))
for layer in base_model.layers:
    layer.trainable = False


def make_custom_model(base_model):
    # get base model output
    x = base_model.output
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dense(units=512, activation="relu")(x)
    # 3 classses: bags, shoes, sneakers
    predictions = layers.Dense(units=3, activation="softmax")(x)
    model = Model(inputs=base_model.input, outputs=predictions)
    return model


model = make_custom_model(base_model)
model.compile(optimizer="Adam", loss="categorical_crossentropy", metrics=["accuracy"])

train_datagenerator = preprocessing.image_dataset_from_directory(
    TARGET_DIR / "train", label_mode="categorical", image_size=(128, 128)
)
model.fit(train_datagenerator, verbose=1, epochs=2, steps_per_epoch=10)


def show(sample):
    # fig, ax = plt.subplots()
    plt.imshow(sample.astype(int))
    plt.show()
    # return ax


train_batch, _ = next(train_datagenerator.as_numpy_iterator())
# plt.imshow(train_batch[1].reshape(28,28))
# show(train_batch[0])
#
#
# predictions = model.predict(train_datagenerator)
# predictions
#
# print(predictions.argmax(axis=1))

test_datagenerator = preprocessing.image_dataset_from_directory(
    TARGET_DIR / "test", label_mode="categorical", image_size=(128, 128)
)

loss, accuracy = model.evaluate(test_datagenerator)
print(f"Loss: {loss}")
print(f"Accuracy: {accuracy}")


actual_datagenerator = preprocessing.image_dataset_from_directory(
    TARGET_DIR / "actual", label_mode=None, image_size=(128, 128)
)

predictions = model.predict(actual_datagenerator)
print(predictions.argmax(axis=1))
