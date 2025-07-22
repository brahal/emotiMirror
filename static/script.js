const video = document.getElementById('video');
const captureBtn = document.getElementById('capture');
const emotionText = document.getElementById('emotion');
const poemText = document.getElementById('poem');
const artwork = document.getElementById('artwork');
const loadingMsg = document.getElementById('loading-msg');

let currentEmotion = null;
let currentImagePath = null;

// Anfangszustand
emotionText.style.display = 'none';
poemText.style.display = 'none';
artwork.style.display = 'none';
loadingMsg.style.display = 'none';

function translateEmotion(emotion) {
    const translations = {
        happy: "glücklich",
        sad: "traurig",
        angry: "wütend",
        surprised: "überrascht",
        fearful: "ängstlich",
        disgust: "angeekelt",
        neutral: "neutral"
    };
    return translations[emotion] || emotion;
}

function restart() {
    document.getElementById('emotion').innerText = '';
    document.getElementById('poem').innerText = '';
    document.getElementById('artwork').src = '';
    document.getElementById('artwork').style.display = 'none';
    document.getElementById('restartBtn').style.display = 'none';
    document.getElementById('downloadBtn').style.display = 'none';
}

// Webcam starten
navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        video.srcObject = stream;
    })
    .catch(err => {
        console.error("Fehler beim Zugriff auf die Kamera:", err);
    });

captureBtn.addEventListener('click', async () => {
    // Ladeanzeige aktivieren
    loadingMsg.style.display = 'block';
    loadingMsg.textContent = 'Emotion wird analysiert…';

    // Screenshot vom Video machen
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const context = canvas.getContext('2d');
    context.drawImage(video, 0, 0);
    const imageData = canvas.toDataURL('image/jpeg');

    try {
        // Schritt 1: Emotion & Text sofort analysieren
        const response = await fetch('/webcam_analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ image: imageData })
        });

        const data = await response.json();
        console.log("Analyseergebnis:", data);

        currentEmotion = data.emotion;
        currentImagePath = data.image_path;

        if (data.error) {
            loadingMsg.textContent = 'Fehler: ' + data.error;
            return;
        }

        // Emotion anzeigen
        const translated = translateEmotion(data.emotion);
        emotionText.innerHTML = `<strong>Emotion:</strong> ${translated}`;
        emotionText.style.display = 'block';

        // Poem anzeigen
        poemText.innerHTML = ` ${data.text}`;
        poemText.style.display = 'block';

        // Ladeanzeige aktualisieren
        loadingMsg.textContent = 'Kunstwerk wird erstellt…';

        // Schritt 2: Kunstbild nachladen
        const artResponse = await fetch('/generate_art', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                emotion: data.emotion,
                image_path: data.image_path
            })
        });

        const artData = await artResponse.json();

        if (artData.art_url) {
            artwork.src = artData.art_url + '?t=' + new Date().getTime(); // Cache verhindern
            artwork.style.display = 'block';
            document.getElementById('artwork').style.display = 'block';
            document.getElementById('restartBtn').style.display = 'inline-block';
            document.getElementById('downloadBtn').style.display = 'inline-block';
            document.getElementById('downloadBtn').href = artData.art_url;
            document.getElementById('downloadBtn').download = "kunstwerk.png";

        } else {
            artwork.style.display = 'none';
        }

        loadingMsg.textContent = 'Fertig!';

    } catch (error) {
        console.error("Fehler:", error);
        loadingMsg.textContent = 'Fehler – bitte erneut versuchen.';
        emotionText.style.display = 'none';
        poemText.style.display = 'none';
        artwork.style.display = 'none';
    }

    // Ladeanzeige automatisch ausblenden
    setTimeout(() => {
        loadingMsg.style.display = 'none';
    }, 4000);
});
