from pathlib import Path

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATASET_DIR = PROJECT_ROOT / "PlantVillage" / "raw" / "color"
MODEL_DIR = PROJECT_ROOT / "models"

IMAGE_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 10
VALIDATION_SPLIT = 0.2
SEED = 42


# ---------------------------------------------------------
# Validate dataset path
# ---------------------------------------------------------

if not DATASET_DIR.exists():
    raise FileNotFoundError(
        f"Dataset folder was not found:\n{DATASET_DIR}"
    )

MODEL_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------
# Load dataset
# ---------------------------------------------------------

print("Loading PlantVillage dataset...")
print(f"Dataset path: {DATASET_DIR}")

train_dataset = tf.keras.utils.image_dataset_from_directory(
    DATASET_DIR,
    validation_split=VALIDATION_SPLIT,
    subset="training",
    seed=SEED,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
)

validation_dataset = tf.keras.utils.image_dataset_from_directory(
    DATASET_DIR,
    validation_split=VALIDATION_SPLIT,
    subset="validation",
    seed=SEED,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
)

class_names = train_dataset.class_names

print(f"\nNumber of classes: {len(class_names)}")
print("Classes:")

for index, class_name in enumerate(class_names):
    print(f"{index}: {class_name}")


# ---------------------------------------------------------
# Improve dataset performance
# ---------------------------------------------------------

AUTOTUNE = tf.data.AUTOTUNE

train_dataset = train_dataset.prefetch(AUTOTUNE)
validation_dataset = validation_dataset.prefetch(AUTOTUNE)


# ---------------------------------------------------------
# Data augmentation
# ---------------------------------------------------------

data_augmentation = keras.Sequential(
    [
        layers.RandomFlip("horizontal"),
        layers.RandomRotation(0.08),
        layers.RandomZoom(0.1),
    ],
    name="data_augmentation",
)


# ---------------------------------------------------------
# Transfer-learning model
# ---------------------------------------------------------

base_model = tf.keras.applications.MobileNetV2(
    input_shape=IMAGE_SIZE + (3,),
    include_top=False,
    weights="imagenet",
)

base_model.trainable = False


inputs = keras.Input(shape=IMAGE_SIZE + (3,))

x = data_augmentation(inputs)

x = tf.keras.applications.mobilenet_v2.preprocess_input(x)

x = base_model(x, training=False)

x = layers.GlobalAveragePooling2D()(x)

x = layers.Dropout(0.25)(x)

outputs = layers.Dense(
    len(class_names),
    activation="softmax",
)(x)

model = keras.Model(inputs, outputs)


# ---------------------------------------------------------
# Compile
# ---------------------------------------------------------

model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=0.001),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"],
)


# ---------------------------------------------------------
# Train
# ---------------------------------------------------------

print("\nStarting model training...\n")

history = model.fit(
    train_dataset,
    validation_data=validation_dataset,
    epochs=EPOCHS,
)


# ---------------------------------------------------------
# Save model
# ---------------------------------------------------------

model_path = MODEL_DIR / "plant_disease_model.keras"

model.save(model_path)


# ---------------------------------------------------------
# Save class names
# ---------------------------------------------------------

class_names_path = MODEL_DIR / "class_names.txt"

class_names_path.write_text(
    "\n".join(class_names),
    encoding="utf-8",
)


# ---------------------------------------------------------
# Final information
# ---------------------------------------------------------

final_training_accuracy = history.history["accuracy"][-1]
final_validation_accuracy = history.history["val_accuracy"][-1]

print("\n" + "=" * 60)
print("TRAINING COMPLETE")
print("=" * 60)

print(f"Training accuracy:   {final_training_accuracy:.4f}")
print(f"Validation accuracy: {final_validation_accuracy:.4f}")

print(f"\nModel saved to:")
print(model_path)

print("\nClass names saved to:")
print(class_names_path)