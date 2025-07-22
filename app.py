from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
from keras.models import load_model
from keras.preprocessing.image import img_to_array
import json
import base64
import os
import traceback
from art_generator import generate_art_image

app = Flask(__name__)

# Modelle und Label laden
model = load_model("models/emotion_model.h5", compile=False)

with open("models/labels.json", "r") as f:
    label_map = json.load(f)

index_to_emotion = {int(k): v for k, v in label_map.items()}

face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Sicherstellen, dass Speicherordner existiert
os.makedirs("static/temp_images", exist_ok=True)

def detect_emotion(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    if len(faces) == 0:
        return None, None

    for (x, y, w, h) in faces:
        face = gray[y:y+h, x:x+w]
        face = cv2.resize(face, (48, 48))
        face = face.astype("float") / 255.0
        face = img_to_array(face)
        face = np.expand_dims(face, axis=0)

        preds = model.predict(face, verbose=0)[0]

        print("🔎 Wahrscheinlichkeiten für alle Klassen:")
        for i, prob in enumerate(preds):
            print(f"{index_to_emotion[i]}: {round(prob * 100, 2)}%")

        emotion_idx = np.argmax(preds)
        emotion = index_to_emotion[emotion_idx]
        confidence = round(float(preds[emotion_idx]) * 100, 1)

        return emotion, confidence

    return None, None

def generate_poetic_text(emotion):
    poetic_lines = {
        "happy": "Dein Lächeln strahlt heller als der Sonnenschein.",
        "sad": "Ein Tropfen Trauer fließt durch die Farbe der Zeit.",
        "angry": "Feuer in deinen Augen, lautlose Worte.",
        "surprised": "Wie ein Stern am Taghimmel – unerwartet und schön.",
        "fearful": "Ein Schatten flüstert in der Stille der Gedanken.",
        "disgust": "Verzogene Sinne suchen nach Reinheit.",
        "neutral": "Gelassen wie ein See in der Abenddämmerung."
    }
    return poetic_lines.get(emotion, "Du bist ein Mysterium in Farben.")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/webcam_analyze", methods=["POST"])
def webcam_analyze():
    data = request.get_json()
    image_data = data.get("image")

    if not image_data:
        return jsonify({"error": "Kein Bild gesendet."}), 400

    try:
        encoded_data = image_data.split(',')[1]
        nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        emotion, confidence = detect_emotion(frame)
        if not emotion:
            return jsonify({"error": "Keine Emotion erkannt."}), 400

        text = generate_poetic_text(emotion)

        # Bild speichern zur späteren Kunstgenerierung
        filename = f"static/temp_images/input_{emotion}.jpg"
        cv2.imwrite(filename, frame)

        response_data = {
            "emotion": emotion,
            "confidence": confidence,
            "text": text,
            "art_url": None,
            "image_path": filename
        }

        return jsonify(response_data)

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route("/generate_art", methods=["POST"])
def generate_art():
    data = request.get_json()
    emotion = data.get("emotion")
    image_path = data.get("image_path")

    if not emotion or not image_path:
        return jsonify({"error": "Fehlende emotion oder image_path"}), 400

    try:
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Bild konnte nicht geladen werden.")

        art_path = generate_art_image(image, emotion)
        return jsonify({"art_url": "/" + art_path})

    except Exception as e:
        print("Fehler bei Kunstbild-Generierung:", e)
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)