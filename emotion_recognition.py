import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
import json

# Modell und Labels laden
model = load_model("models/archiv/emotion_model-old.h5", compile=False)
with open("models/labels.json", "r") as f:
    label_map = json.load(f)

# Umgekehrte Zuordnung von Index zu Emotionslabel
index_to_emotion = {int(k): v for k, v in label_map.items()}

# Haar-Cascade Gesichtsdetektor laden
face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

def detect_emotion(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    if len(faces) == 0:
        return None, Nonexd

    # Nur das erste Gesicht verwenden
    (x, y, w, h) = faces[0]
    face = gray[y:y+h, x:x+w]
    face = cv2.resize(face, (48, 48))
    face = face.astype("float") / 255.0
    face = img_to_array(face)
    face = np.expand_dims(face, axis=0)

    preds = model.predict(face, verbose=0)[0]
    emotion_idx = np.argmax(preds)
    emotion_label = index_to_emotion[emotion_idx]
    confidence = round(preds[emotion_idx] * 100, 1)

    return emotion_label, confidence