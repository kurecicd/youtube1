import os
import base64
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from PIL import Image
import fal_client
import config

os.environ["FAL_KEY"] = config.FAL_API_KEY

KLING_MODEL = "fal-ai/kling-video/v1.6/standard/image-to-video"


def _animate_scene(args: tuple) -> tuple:
    idx, img, caption, tmp_dir = args

    img_path = os.path.join(tmp_dir, f"scene_{idx}.jpg")
    img.save(img_path, quality=95)

    with open(img_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    data_url = f"data:image/jpeg;base64,{b64}"

    prompt = (
        f"Gentle smooth cartoon animation. {caption}. "
        "Characters move naturally and softly. Slow peaceful motion. "
        "Pixar kids cartoon style. No camera shake."
    )

    result = fal_client.subscribe(
        KLING_MODEL,
        arguments={
            "image_url": data_url,
            "prompt": prompt,
            "duration": "5",
            "aspect_ratio": "9:16",
        },
    )

    video_url = result["video"]["url"]
    video_path = os.path.join(tmp_dir, f"clip_{idx}.mp4")
    with open(video_path, "wb") as f:
        f.write(requests.get(video_url).content)

    print(f"  Clip {idx + 1} animated: {caption}")
    return idx, video_path, caption


def generate_video_clips(images: list, tmp_dir: str) -> list:
    results = {}
    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = {
            executor.submit(_animate_scene, (i, img, cap, tmp_dir)): i
            for i, (img, cap) in enumerate(images)
        }
        for future in as_completed(futures):
            idx, path, caption = future.result()
            results[idx] = (path, caption)
    return [results[i] for i in range(len(images))]
