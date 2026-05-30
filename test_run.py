"""Test run — full pipeline but saves locally instead of uploading."""

import os
import shutil
import tempfile
import logging
from script_generator import generate_script
from image_generator import generate_images
from video_generator import generate_video_clips
from voiceover import generate_voiceover
from video_assembler import assemble_video

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
log = logging.getLogger(__name__)

OUTPUT_PATH = os.path.expanduser("~/Desktop/tinytunes_test.mp4")


def run():
    log.info("=== TinyTunes TEST (no upload) ===")

    with tempfile.TemporaryDirectory(prefix="tinytunes_") as tmp_dir:
        log.info("Step 1/4: Generating script...")
        script = generate_script()
        log.info(f"  Theme: {script['theme']}")
        log.info(f"  Title: {script['title']}")

        log.info("Step 2/4: Generating scene images...")
        images = generate_images(script["scenes"])

        log.info("Step 3/4: Animating scenes with Kling (~5 min)...")
        video_clips = generate_video_clips(images, tmp_dir)

        log.info("Step 4/4: Voiceover + assembly...")
        audio_bytes = generate_voiceover(script["voiceover"])
        video_path = assemble_video(video_clips, audio_bytes, tmp_dir)

        shutil.copy(video_path, OUTPUT_PATH)

    log.info(f"=== Done! Saved to {OUTPUT_PATH} ===")
    os.system(f'open "{OUTPUT_PATH}"')


if __name__ == "__main__":
    run()
