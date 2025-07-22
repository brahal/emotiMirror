from diffusers import StableDiffusionPipeline
import torch

pipe = StableDiffusionPipeline.from_pretrained(
    "CompVis/stable-diffusion-v1-4",
    use_auth_token="HF_TOKEN",
    torch_dtype=torch.float32
)

pipe.save_pretrained("./models/stable-diffusion-v1-4")