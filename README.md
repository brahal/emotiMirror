# EmotiMirror – Emotion trifft auf Kunst

**EmotiMirror** ist eine interaktive Webanwendung, die Emotionen aus einem Webcam-Selfie erkennt und in ein stilisiertes digitales Kunstwerk im Ölmalerei-Stil überträgt – ergänzt durch einen poetischen Satz, passend zur erkannten Emotion.

## Funktionen

- 📷 Webcam-Snapshot mit Emotionserkennung (CNN + `emotion_model.h5`)
- 🧠 Deep Learning mit Keras + OpenCV zur Emotionserkennung (traurig, glücklich, überrascht, usw.)
- 🎨 Bildgenerierung mit Stable Diffusion `img2img` (lokal, LoRA-Stilmodell z. B. OilPainting)
- 🖼️ Gesichtsausdruck & Form bleiben erhalten (Mund, Augen, Gesichtskonturen)
- 📝 Poetischer Text wird zur erkannten Emotion erzeugt
- 📥 Downloadfunktion für das fertige Kunstporträt
- 🖥️ Offline lauffähig (lokal in Flask), kein Cloud-Zugriff nötig

---

## 🛠️ Verwendete Technologien

| Technologie        | Beschreibung                              |
|--------------------|-------------------------------------------|
| Python + Flask     | Backend Webserver                         |
| HTML/CSS/JS        | Benutzeroberfläche mit Webcam-Anbindung  |
| TensorFlow / Keras | Emotionserkennung (CNN-Modell `.h5`)     |
| Stable Diffusion   | Bildgenerierung via `img2img` mit LoRA   |
| LoRA Adapter       | Künstlerischer Stil: z. B. Ölmalerei-Stil |
| OpenCV             | Webcam-Zugriff und Bildspeicherung       |

---

## Installation (lokal)

1. Clone das Repository:

```bash
git clone  https://github.com/brahal/emoti_mirror.git

cd emoti-mirror
```

## Autorin

**Basma Rahal**  
Master Medieninformatik (M.Sc.)  
Modul: *Smart Graphics*  
Technische Hochschule Lübeck  
Sommersemester 2025

##  Lizenz

Dieses Projekt wurde im Rahmen einer Studienleistung an der Technischen Hochschule Lübeck im Modul *Smart Graphics* (SoSe 2025) entwickelt.

Alle Inhalte (Code, Texte, Bilder) unterliegen dem Urheberrecht der Autorin. Eine Weiterverwendung, Veröffentlichung oder kommerzielle Nutzung ist ohne ausdrückliche schriftliche Genehmigung der Autorin nicht gestattet.

Die Bereitstellung auf GitHub dient ausschließlich der Dokumentation und Bewertung im Hochschulkontext.
