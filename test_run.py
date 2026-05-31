"""Test run — full pipeline, saves locally instead of uploading to YouTube."""

import os
import shutil
import tempfile
import logging
from script_generator import generate_script
from image_generator import generate_images
from video_generator import generate_video_clips
from music_generator import generate_music
from video_assembler import assemble_video_clips

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
log = logging.getLogger(__name__)

OUTPUT_PATH = os.path.expanduser("~/Desktop/tinytunes_test.mp4")


def run():
    log.info("=== TinyTunes TEST (no upload) ===")

    with tempfile.TemporaryDirectory(prefix="tinytunes_") as tmp_dir:
        log.info("Step 1/4: Generating story script...")
        script = generate_script()
        log.info(f"  Story: {script['theme']}")
        log.info(f"  Title: {script['title']}")
        for i, scene in enumerate(script["scenes"], 1):
            log.info(f"  Scene {i} [{scene['story_beat']}]: {scene['caption']}")

        log.info("Step 2/4: Generating scene images with gpt-image-1...")
        images = generate_images(script["scenes"])

        log.info("Step 3/4: Animating images with Kling (~15 min)...")
        video_clips = generate_video_clips(images, tmp_dir)

        log.info("Step 4/4: Generating music + assembling video...")
        total_duration = len(video_clips) * 5
        music_bytes = generate_music(script["music_prompt"], total_duration)
        video_path = assemble_video_clips(video_clips, music_bytes, tmp_dir)
        shutil.copy(video_path, OUTPUT_PATH)

    log.info(f"=== Done! Saved to {OUTPUT_PATH} ===")
    os.system(f'open "{OUTPUT_PATH}"')


if __name__ == "__main__":
    run()
