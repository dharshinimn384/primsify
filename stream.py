import streamlit as st
import torch
import cv2
import numpy as np
from PIL import Image

from diffusers.pipelines import StableDiffusionXLAdapterPipeline
from diffusers.schedulers import LCMScheduler
from diffusers.models import T2IAdapter
from diffusers.utils import make_image_grid

# Function to perform inference and generate images
def generate_images(image_path, prompt, negative_prompt):
    # Load the image using PIL directly from the file path
    image = Image.open(image_path).resize((384, 384))
    image = np.array(image)

    low_threshold = 100
    high_threshold = 200

    image = cv2.Canny(image, low_threshold, high_threshold)
    image = image[:, :, None]
    image = np.concatenate([image, image, image], axis=2)
    canny_image = Image.fromarray(image).resize((1024, 1024))

    # Load adapter
    adapter = T2IAdapter.from_pretrained("TencentARC/t2i-adapter-canny-sdxl-1.0", torch_dtype=torch.float16, variant="fp16")

    # Load pipeline
    pipe = StableDiffusionXLAdapterPipeline.from_pretrained(
        "stabilityai/stable-diffusion-xl-base-1.0", 
        adapter=adapter,
        torch_dtype=torch.float16,
        variant="fp16", 
    ).to("cuda")

    # Set scheduler
    pipe.scheduler = LCMScheduler.from_config(pipe.scheduler.config)

    # Load LCM-LoRA
    pipe.load_lora_weights("latent-consistency/lcm-lora-sdxl")

    generator = torch.manual_seed(0)
    image_result = pipe(
        prompt=prompt,
        negative_prompt=negative_prompt,
        image=canny_image,
        num_inference_steps=4,
        guidance_scale=1.5, 
        adapter_conditioning_scale=0.8, 
        adapter_conditioning_factor=1,
        generator=generator,
    ).images[0]

    return canny_image, image_result

# Streamlit app
def main():
    st.title("Primsify")

    # Upload image
    uploaded_image = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

    # Input prompts
    prompt = st.text_input("Enter prompt:")
    negative_prompt = st.text_input("Enter negative prompt:")

    # Generate images on button click
    if st.button("Generate Images"):
        if uploaded_image is not None:
            canny_image, generated_image = generate_images(uploaded_image, prompt, negative_prompt)
            st.image([canny_image, generated_image], caption=['Canny Image', 'Generated Image'], width=500, use_column_width=False)

if __name__ == "__main__":
    main()
