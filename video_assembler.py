import os
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy import VideoClip, VideoFileClip, AudioFileClip, ImageClip, CompositeVideoClip, concatenate_videoclips

FONT_PATHS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/Library/Fonts/Arial Bold.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
]
FONT_SIZE = 64
TARGET_W, TARGET_H = 1080, 1920
ZOOM = 1.10  # 10% extra canvas for Ken Burns movement


def _get_font():
    for path in FONT_PATHS:
        try:
            return ImageFont.truetype(path, FONT_SIZE)
        except Exception:
            continue
    return ImageFont.load_default()


def _burn_caption(img: Image.Image, caption: str) -> Image.Image:
    if not caption:
        return img
    result = img.copy()
    draw = ImageDraw.Draw(result)
    font = _get_font()
    bbox = draw.textbbox((0, 0), caption, font=font)
    text_w = bbox[2] - bbox[0]
    x = (TARGET_W - text_w) // 2
    y = int(TARGET_H * 0.83)
    for dx, dy in [(-2, -2), (2, -2), (-2, 2), (2, 2)]:
        draw.text((x + dx, y + dy), caption, font=font, fill=(0, 0, 0))
    draw.text((x, y), caption, font=font, fill=(255, 255, 255))
    return result


def _ken_burns_clip(img: Image.Image, caption: str, duration: float, fps: int = 24) -> VideoClip:
    large_w = int(TARGET_W * ZOOM)
    large_h = int(TARGET_H * ZOOM)
    max_x = large_w - TARGET_W
    max_y = large_h - TARGET_H

    img_captioned = _burn_caption(img, caption)
    large = np.array(img_captioned.resize((large_w, large_h), Image.LANCZOS))

    # Random Ken Burns: zoom in, zoom out, or pan across
    move = random.choice(["zoom_in", "zoom_out", "pan"])
    if move == "zoom_in":
        sx, sy = random.randint(0, max_x), random.randint(0, max_y)
        ex, ey = max_x // 2, max_y // 2
    elif move == "zoom_out":
        sx, sy = max_x // 2, max_y // 2
        ex, ey = random.randint(0, max_x), random.randint(0, max_y)
    else:  # pan
        sx, sy = 0, random.randint(0, max_y)
        ex, ey = max_x, random.randint(0, max_y)

    def make_frame(t):
        p = t / duration
        p = p * p * (3 - 2 * p)  # smooth ease in/out
        x = int(sx + (ex - sx) * p)
        y = int(sy + (ey - sy) * p)
        return large[y: y + TARGET_H, x: x + TARGET_W]

    clip = VideoClip(make_frame, duration=duration)
    clip.fps = fps
    return clip


def assemble_video_clips(video_clips: list, audio_bytes: bytes, tmp_dir: str) -> str:
    audio_path = os.path.join(tmp_dir, "audio.mp3")
    with open(audio_path, "wb") as f:
        f.write(audio_bytes)

    clips = []
    for path, caption in video_clips:
        clip = VideoFileClip(path).resized((TARGET_W, TARGET_H))
        if caption:
            overlay = Image.new("RGBA", (TARGET_W, TARGET_H), (0, 0, 0, 0))
            draw = ImageDraw.Draw(overlay)
            font = _get_font()
            bbox = draw.textbbox((0, 0), caption, font=font)
            x = (TARGET_W - (bbox[2] - bbox[0])) // 2
            y = int(TARGET_H * 0.83)
            for dx, dy in [(-2, -2), (2, -2), (-2, 2), (2, 2)]:
                draw.text((x + dx, y + dy), caption, font=font, fill=(0, 0, 0, 255))
            draw.text((x, y), caption, font=font, fill=(255, 255, 255, 255))
            ov = ImageClip(np.array(overlay), duration=clip.duration)
            clip = CompositeVideoClip([clip, ov])
        clips.append(clip)

    video = concatenate_videoclips(clips, method="compose")

    audio_clip = AudioFileClip(audio_path)
    # Loop short audio to cover the full video duration
    if audio_clip.duration < video.duration:
        from moviepy import concatenate_audioclips
        import math
        n = math.ceil(video.duration / audio_clip.duration)
        audio_clip = concatenate_audioclips([audio_clip] * n)
    audio_clip = audio_clip.subclipped(0, video.duration)

    video = video.with_audio(audio_clip)
    output_path = os.path.join(tmp_dir, "output.mp4")
    video.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac", logger=None)
    return output_path


def assemble_video(images: list, audio_bytes: bytes, tmp_dir: str) -> str:
    audio_path = os.path.join(tmp_dir, "voiceover.mp3")
    with open(audio_path, "wb") as f:
        f.write(audio_bytes)

    audio_clip = AudioFileClip(audio_path)
    duration_per_scene = audio_clip.duration / len(images)

    clips = []
    for img, caption in images:
        clips.append(_ken_burns_clip(img, caption, duration_per_scene))

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
