import time
import requests
from io import BytesIO
from PIL import Image
from openai import OpenAI
import config

client = OpenAI(api_key=config.OPENAI_API_KEY)
TARGET_SIZE = (1080, 1920)


def generate_images(scenes: list) -> list:
    images = []
    for i, scene in enumerate(scenes):
        print(f"  Image {i+1}/{len(scenes)}: {scene['caption']}")
        response = client.images.generate(
            model="dall-e-3",
            prompt=scene["image_prompt"],
            size="1024x1792",
            quality="standard",
            n=1,
        )
        img_url = response.data[0].url
        img_data = requests.get(img_url).content
        img = Image.open(BytesIO(img_data)).resize(TARGET_SIZE, Image.LANCZOS)
        images.append((img, scene.get("caption", "")))
        if i < len(scenes) - 1:
            time.sleep(1)
    return images
