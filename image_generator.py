import base64
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor, as_completed
from PIL import Image
from openai import OpenAI
import config

client = OpenAI(api_key=config.OPENAI_API_KEY)
TARGET_SIZE = (1080, 1920)
MAX_WORKERS = 2


def _generate_single(args: tuple) -> tuple:
    idx, scene = args
    full_prompt = f"{config.CHARACTER_DESC}\n\nScene: {scene['image_prompt']}"
    fallback_prompt = f"{config.CHARACTER_DESC}\n\nScene: Two happy cartoon brothers playing together outdoors on a sunny day, bright colors, cheerful mood."
    for prompt in [full_prompt, fallback_prompt]:
        try:
            response = client.images.generate(
                model="gpt-image-1",
                prompt=prompt,
                size="1024x1536",
                quality="medium",
                n=1,
            )
            img_data = base64.b64decode(response.data[0].b64_json)
            img = Image.open(BytesIO(img_data)).resize(TARGET_SIZE, Image.LANCZOS)
            return idx, img, scene.get("caption", "")
        except Exception as e:
            if "moderation_blocked" in str(e) and prompt == full_prompt:
                continue
            raise
    # last resort: solid sky-blue placeholder
    img = Image.new("RGB", TARGET_SIZE, color=(135, 206, 235))
    return idx, img, scene.get("caption", "")


def generate_images(scenes: list) -> list:
    results = {}
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(_generate_single, (i, s)): i for i, s in enumerate(scenes)}
        for future in as_completed(futures):
            idx, img, caption = future.result()
            results[idx] = (img, caption)
            print(f"  Image {idx + 1}/{len(scenes)} done: {caption}")
    return [results[i] for i in range(len(scenes))]
