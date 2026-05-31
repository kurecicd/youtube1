import tempfile
import logging
from script_generator import generate_script
from image_generator import generate_images
from video_generator import generate_video_clips
from music_generator import generate_music
from video_assembler import assemble_video_clips
from youtube_uploader import upload_video

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
log = logging.getLogger(__name__)


def run():
    log.info("=== TinyTunes pipeline starting ===")

    with tempfile.TemporaryDirectory(prefix="tinytunes_") as tmp_dir:
        log.info("Step 1/5: Generating story script...")
        script = generate_script()
        log.info(f"  Story: {script['theme']}")
        log.info(f"  Title: {script['title']}")

        log.info("Step 2/5: Generating scene images...")
        images = generate_images(script["scenes"])

        log.info("Step 3/5: Animating images with Kling...")
        video_clips = generate_video_clips(images, tmp_dir)

        log.info("Step 4/5: Generating nursery rhyme music...")
        total_duration = len(video_clips) * 10
        music_bytes = generate_music(script["music_prompt"], total_duration)

        log.info("Step 5/5: Assembling + uploading to YouTube...")
        video_path = assemble_video_clips(video_clips, music_bytes, tmp_dir)
        video_id = upload_video(video_path, script)

        log.info(f"=== Done! https://youtube.com/shorts/{video_id} ===")


if __name__ == "__main__":
    run()
