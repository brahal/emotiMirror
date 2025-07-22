import tensorflow as tf
from matplotlib import pyplot as plt
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
import json
import os

# Pfade
train_dir = "data_emotion/train"
test_dir = "data_emotion/test"
model_save_path = "models/emotion_model.h5"
label_map_path = "models/labels.json"

# Bildgröße und Trainingsparameter
img_size = (48, 48)
batch_size = 32
epochs = 30

# Trainingsdaten vorbereiten
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=10,
    zoom_range=0.1,
    width_shift_range=0.1,
    height_shift_range=0.1,
    horizontal_flip=True
)
test_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=img_size,
    color_mode="grayscale",
    batch_size=batch_size,
    class_mode="categorical"
)

test_generator = test_datagen.flow_from_directory(
    test_dir,
    target_size=img_size,
    color_mode="grayscale",
    batch_size=batch_size,
    class_mode="categorical"
)

# Modell definieren
model = Sequential([
    Conv2D(32, (3,3), activation='relu', input_shape=(48, 48, 1)),
    MaxPooling2D(2,2),
    Conv2D(64, (3,3), activation='relu'),
    MaxPooling2D(2,2),
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(train_generator.num_classes, activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Modell trainieren
model.fit(
    train_generator,
    epochs=epochs,
    validation_data=test_generator
)

# Modell speichern
os.makedirs(os.path.dirname(model_save_path), exist_ok=True)
model.save(model_save_path)
print(f"Modell gespeichert unter: {model_save_path}")

# Label-Mapping speichern
index_to_label = {v: k for k, v in train_generator.class_indices.items()}
with open(label_map_path, "w") as f:
    json.dump(index_to_label, f)
print(f"Labels gespeichert unter: {label_map_path}")


# Trainingsergebnisse visualisieren und speichern
history_dict = model.history.history

plt.figure(figsize=(12, 5))

# Verlust (Loss)
plt.subplot(1, 2, 1)
plt.plot(history_dict['loss'], label='Trainingsverlust')
plt.plot(history_dict['val_loss'], label='Validierungsverlust')
plt.title('Modellverlust')
plt.xlabel('Epoche')
plt.ylabel('Verlust')
plt.legend()

# Genauigkeit (Accuracy)
plt.subplot(1, 2, 2)
plt.plot(history_dict['accuracy'], label='Trainingsgenauigkeit')
plt.plot(history_dict['val_accuracy'], label='Validierungsgenauigkeit')
plt.title('Modellgenauigkeit')
plt.xlabel('Epoche')
plt.ylabel('Genauigkeit')
plt.legend()

plt.tight_layout()
plt.savefig("training_plot-bild.png")
print("Trainingsverlauf gespeichert als: training_plot-bild.png")