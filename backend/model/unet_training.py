import os
import numpy as np
import tensorflow as tf
from keras._tf_keras.keras.models import Model
from keras._tf_keras.keras.layers import (
    Input,
    Conv2D,
    MaxPooling2D,
    Conv2DTranspose,
    concatenate,
    Dropout,
)
from keras._tf_keras.keras.callbacks import ModelCheckpoint, EarlyStopping
from keras._tf_keras.keras.optimizers import Adam
from keras._tf_keras.keras.preprocessing.image import load_img, img_to_array

# Directories for images and masks
IMAGE_DIR = "train_images"
MASK_DIR = "train_masks"

IMG_HEIGHT, IMG_WIDTH = 256, 256
IMG_CHANNELS = 3


# Function to load images and masks
def load_data(image_dir, mask_dir):
    images = []
    masks = []

    image_filenames = sorted(os.listdir(image_dir))
    mask_filenames = sorted(os.listdir(mask_dir))

    for img_name, mask_name in zip(image_filenames, mask_filenames):
        img_path = os.path.join(image_dir, img_name)
        mask_path = os.path.join(mask_dir, mask_name)

        image = load_img(img_path, target_size=(IMG_HEIGHT, IMG_WIDTH))
        mask = load_img(
            mask_path, target_size=(IMG_HEIGHT, IMG_WIDTH), color_mode="grayscale"
        )

        image = img_to_array(image) / 255.0  # Normalize to [0,1]
        mask = img_to_array(mask) / 255.0  # Normalize to [0,1]

        images.append(image)
        masks.append(mask)

    return np.array(images), np.array(masks)


# Define U-Net model
def unet_model():
    inputs = Input((IMG_HEIGHT, IMG_WIDTH, IMG_CHANNELS))

    # Contracting Path (Encoder)
    c1 = Conv2D(32, (3, 3), activation="relu", padding="same")(inputs)
    c1 = Conv2D(32, (3, 3), activation="relu", padding="same")(c1)
    p1 = MaxPooling2D((2, 2))(c1)

    c2 = Conv2D(64, (3, 3), activation="relu", padding="same")(p1)
    c2 = Conv2D(64, (3, 3), activation="relu", padding="same")(c2)
    p2 = MaxPooling2D((2, 2))(c2)

    c3 = Conv2D(128, (3, 3), activation="relu", padding="same")(p2)
    c3 = Conv2D(128, (3, 3), activation="relu", padding="same")(c3)
    p3 = MaxPooling2D((2, 2))(c3)

    # Bottleneck
    c4 = Conv2D(256, (3, 3), activation="relu", padding="same")(p3)
    c4 = Conv2D(256, (3, 3), activation="relu", padding="same")(c4)

    # Expansive Path (Decoder)
    u1 = Conv2DTranspose(128, (2, 2), strides=(2, 2), padding="same")(c4)
    u1 = concatenate([u1, c3])
    c5 = Conv2D(128, (3, 3), activation="relu", padding="same")(u1)
    c5 = Conv2D(128, (3, 3), activation="relu", padding="same")(c5)

    u2 = Conv2DTranspose(64, (2, 2), strides=(2, 2), padding="same")(c5)
    u2 = concatenate([u2, c2])
    c6 = Conv2D(64, (3, 3), activation="relu", padding="same")(u2)
    c6 = Conv2D(64, (3, 3), activation="relu", padding="same")(c6)

    u3 = Conv2DTranspose(32, (2, 2), strides=(2, 2), padding="same")(c6)
    u3 = concatenate([u3, c1])
    c7 = Conv2D(32, (3, 3), activation="relu", padding="same")(u3)
    c7 = Conv2D(32, (3, 3), activation="relu", padding="same")(c7)

    outputs = Conv2D(1, (1, 1), activation="sigmoid")(c7)

    model = Model(inputs=[inputs], outputs=[outputs])
    return model


# Load data
X, y = load_data(IMAGE_DIR, MASK_DIR)

# Compile model
model = unet_model()
model.compile(
    optimizer=Adam(learning_rate=1e-4), loss="binary_crossentropy", metrics=["accuracy"]
)

# Callbacks
checkpoint = ModelCheckpoint(
    "wetland_unet.h5", save_best_only=True, monitor="val_loss", mode="min"
)
early_stopping = EarlyStopping(patience=10, restore_best_weights=True)

# Train model
history = model.fit(
    X,
    y,
    validation_split=0.2,
    batch_size=8,
    epochs=50,
    callbacks=[checkpoint, early_stopping],
)

# Final save
model.save("final_wetland_unet.h5")
print("Training complete. Model saved.")
