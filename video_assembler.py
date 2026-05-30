import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy import VideoFileClip, AudioFileClip, ImageClip, CompositeVideoClip, concatenate_videoclips

FONT_PATHS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/Library/Fonts/Arial Bold.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
]
FONT_SIZE = 64
TEXT_COLOR = (255, 255, 255, 255)
SHADOW_COLOR = (0, 0, 0, 255)
TEXT_Y_RATIO = 0.83


def _get_font():
    for path in FONT_PATHS:
        try:
            return ImageFont.truetype(path, FONT_SIZE)
        except Exception:
            continue
    return ImageFont.load_default()


def _caption_overlay(clip, caption: str):
    if not caption:
        return clip
    w, h = clip.size
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    font = _get_font()
    bbox = draw.textbbox((0, 0), caption, font=font)
    text_w = bbox[2] - bbox[0]
    x = (w - text_w) // 2
    y = int(h * TEXT_Y_RATIO)
    for dx, dy in [(-2, -2), (2, -2), (-2, 2), (2, 2)]:
        draw.text((x + dx, y + dy), caption, font=font, fill=SHADOW_COLOR)
    draw.text((x, y), caption, font=font, fill=TEXT_COLOR)
    arr = np.array(overlay)
    overlay_clip = ImageClip(arr, duration=clip.duration)
    return CompositeVideoClip([clip, overlay_clip])


def assemble_video(video_clips: list, audio_bytes: bytes, tmp_dir: str) -> str:
    audio_path = os.path.join(tmp_dir, "voiceover.mp3")
    with open(audio_path, "wb") as f:
        f.write(audio_bytes)
    audio_clip = AudioFileClip(audio_path)

    clips = []
    for path, caption in video_clips:
        clip = VideoFileClip(path).resized((1080, 1920))
        clip = _caption_overlay(clip, caption)
        clips.append(clip)

    video = concatenate_videoclips(clips, method="compose").with_audio(audio_clip)
    output_path = os.path.join(tmp_dir, "output.mp4")
    video.write_videofile(
        output_path,
        fps=24,
        codec="libx264",
        audio_codec="aac",
        logger=None,
    )
    return output_path
