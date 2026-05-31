import os
import base64
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from PIL import Image
import fal_client
import config

os.environ["FAL_KEY"] = config.FAL_API_KEY

KLING_MODEL = "fal-ai/kling-video/v1.6/standard/text-to-video"


def _animate_scene(args: tuple) -> tuple:
    idx, scene, tmp_dir = args

    prompt = (
        f"{config.CHARACTER_DESC}\n\n"
        f"Animated kids cartoon scene: {scene['image_prompt']}. "
        f"{scene.get('caption', '')}. "
        "Bright Pixar 3D animation style. Gentle smooth character movement. "
        "Slow peaceful motion. Happy cheerful mood. No camera shake. Kids friendly."
    )

    result = fal_client.subscribe(
        KLING_MODEL,
        arguments={
            "prompt": prompt,
            "duration": "5",
            "aspect_ratio": "9:16",
        },
    )

    video_url = result["video"]["url"]
    video_path = os.path.join(tmp_dir, f"clip_{idx}.mp4")
    with open(video_path, "wb") as f:
        f.write(requests.get(video_url).content)

    caption = scene.get("caption", "")
    print(f"  Clip {idx + 1} animated: {caption}")
    return idx, video_path, caption


def generate_video_clips(scenes: list, tmp_dir: str) -> list:
    results = {}
    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = {
            executor.submit(_animate_scene, (i, scene, tmp_dir)): i
            for i, scene in enumerate(scenes)
        }
        for future in as_completed(futures):
            idx, path, caption = future.result()
            results[idx] = (path, caption)
    return [results[i] for i in range(len(scenes))]
