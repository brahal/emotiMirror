# EmotiMirror – Emotion trifft auf Kunst

**EmotiMirror** ist eine interaktive Webanwendung, die Emotionen aus einem Webcam-Selfie erkennt und diese in ein stilisiertes digitales Kunstwerk im Ölmalerei-Stil überträgt – ergänzt durch einen poetischen Satz, passend zur erkannten Emotion.

## Funktionen

- Aufnahme eines Webcam-Selfies mit automatischer Emotionserkennung (CNN + `emotion_model.h5`)
- Deep Learning mit Keras & OpenCV zur Erkennung von Emotionen wie Trauer, Freude, Überraschung u. a.
- Künstlerische Bildtransformation mit Stable Diffusion (`img2img`) unter Verwendung eines LoRA-Stilmodells (z. B. OilPainting)
-  Gesichtsausdruck & Konturen bleiben im Kunstbild erhalten (Mund, Augen, Gesichtsform)
-  Automatische Generierung eines poetischen Satzes passend zur erkannten Emotion
-  Downloadfunktion für das fertige Kunstporträt
- Offline lauffähig (lokal via Flask) – kein Internet oder Cloud-Zugriff erforderlich

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
git clone  https://github.com/brahal/emotiMirror.git

cd emotiMirror
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
