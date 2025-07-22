import torch
import cv2
from PIL import Image
from diffusers import StableDiffusionImg2ImgPipeline, DDIMScheduler
from transformers import logging
import os
import random

logging.set_verbosity_error()

# Modellpfade
model_path = "./models/stable-diffusion-v1-4"
lora_path = "./models/lora/oilPaintingStyle_lora.safetensors"

# Pipeline laden
pipe = StableDiffusionImg2ImgPipeline.from_pretrained(model_path)
pipe.scheduler = DDIMScheduler.from_pretrained(
    model_path,
    subfolder="scheduler",
    use_karras_sigmas=True
)
pipe.to("cuda" if torch.cuda.is_available() else "cpu")

# LoRA-Adapter laden
try:
    pipe.load_lora_weights(lora_path, adapter_name="oil_painting")
    pipe.set_adapters(["oil_painting"], adapter_weights=[0.6])
    print("LoRA geladen und aktiviert.")
except Exception as e:
    print("LoRA konnte nicht geladen werden:", e)

# Negative Prompt global
negative_prompt = (
    "blurry, distorted, low quality, exaggerated cartoon, plastic, photo, disfigured face, "
    "extra limbs, mutated, cloned, fused, asymmetric eyes, bad anatomy"
)

# Emotion → Prompt Mapping

def get_emotion_prompt(emotion):
    base = (
        "oil painting portrait, realistic face preserved, natural eyes and mouth, "
        "preserve original expression and features, visible brush strokes"
    )
    styles = {
        "happy": (
            "warm light, soft golden tones, gentle background, subtle smile, "
            "peaceful ambiance"
        ),
        "sad": (
            "cool muted tones, melancholic atmosphere, soft shadows, thoughtful mood, "
            "emotional depth"
        ),
        "angry": (
            "bold brush strokes, red and dark hues, dramatic light contrast, tense energy"
        ),
        "surprised": (
            "light surreal tones, bright highlights, expressive energy, open expression"
        ),
        "neutral": (
            "balanced tones, calm lighting, soft edges, centered composition"
        ),
        "fear": (
            "dim lighting, pale tones, fragile tension in atmosphere, shadowy background"
        ),
        "disgust": (
            "earthy palette, expression of discomfort, tension in posture, abstracted style"
        )
    }
    return f"{base}, {styles.get(emotion, 'expressive features, painted in the style of Picasso')}"
# Hauptfunktion
def generate_art_image(frame, emotion):
    try:
        pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        init_image = pil_image.resize((512, 512))

        prompt = get_emotion_prompt(emotion)

        result = pipe(
            prompt=prompt,
            negative_prompt=negative_prompt,
            image=init_image,
            strength=0.07,
            guidance_scale=7.5,
            num_inference_steps=30
        ).images[0]

        # Bild speichern
        output_dir = "static/outputs"
        os.makedirs(output_dir, exist_ok=True)
        filename = f"generated_{emotion}_{random.randint(1000, 9999)}.png"
        output_path = os.path.join(output_dir, filename)
        result.save(output_path)

        print("Kunstwerk gespeichert unter:", output_path)
        return output_path

    except Exception as e:
        print("Fehler bei Kunstbild-Generierung:", str(e))
        return ""