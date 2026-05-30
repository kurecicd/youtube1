import tempfile
import logging
from script_generator import generate_script
from image_generator import generate_images
from voiceover import generate_voiceover
from video_assembler import assemble_video
from youtube_uploader import upload_video

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
log = logging.getLogger(__name__)


def run():
    log.info("=== TinyTunes pipeline starting ===")

    with tempfile.TemporaryDirectory(prefix="tinytunes_") as tmp_dir:
        log.info("Step 1/5: Generating script...")
        script = generate_script()
        log.info(f"  Theme: {script['theme']}")
        log.info(f"  Title: {script['title']}")

        log.info("Step 2/5: Generating images...")
        images = generate_images(script["scenes"])

        log.info("Step 3/5: Generating voiceover...")
        audio_bytes = generate_voiceover(script["voiceover"])

        log.info("Step 4/5: Assembling video...")
        video_path = assemble_video(images, audio_bytes, tmp_dir)

        log.info("Step 5/5: Uploading to YouTube...")
        video_id = upload_video(video_path, script)

        log.info(f"=== Done! https://youtube.com/shorts/{video_id} ===")


if __name__ == "__main__":
    run()
