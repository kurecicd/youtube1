import os
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips

FONT_PATHS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",  # Linux / Railway
    "/Library/Fonts/Arial Bold.ttf",                          # Mac
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",      # Mac alt
    "C:/Windows/Fonts/arialbd.ttf",                           # Windows
]
FONT_SIZE = 72
TEXT_COLOR = (255, 255, 255)
SHADOW_COLOR = (0, 0, 0)
TEXT_Y_RATIO = 0.83


def _get_font():
    for path in FONT_PATHS:
        try:
            return ImageFont.truetype(path, FONT_SIZE)
        except Exception:
            continue
    return ImageFont.load_default()


def _add_caption(img: Image.Image, caption: str) -> Image.Image:
    if not caption:
        return img
    result = img.copy()
    draw = ImageDraw.Draw(result)
    font = _get_font()
    w, h = result.size
    bbox = draw.textbbox((0, 0), caption, font=font)
    text_w = bbox[2] - bbox[0]
    x = (w - text_w) // 2
    y = int(h * TEXT_Y_RATIO)
    for dx, dy in [(-2, -2), (2, -2), (-2, 2), (2, 2)]:
        draw.text((x + dx, y + dy), caption, font=font, fill=SHADOW_COLOR)
    draw.text((x, y), caption, font=font, fill=TEXT_COLOR)
    return result


def assemble_video(images: list, audio_bytes: bytes, tmp_dir: str) -> str:
    audio_path = os.path.join(tmp_dir, "voiceover.mp3")
    with open(audio_path, "wb") as f:
        f.write(audio_bytes)

    audio_clip = AudioFileClip(audio_path)
    duration_per_scene = audio_clip.duration / len(images)

    clips = []
    for i, (img, caption) in enumerate(images):
        img_captioned = _add_caption(img, caption)
        img_path = os.path.join(tmp_dir, f"scene_{i}.jpg")
        img_captioned.save(img_path, quality=95)
        clips.append(ImageClip(img_path, duration=duration_per_scene))

    video = concatenate_videoclips(clips, method="compose").set_audio(audio_clip)
    output_path = os.path.join(tmp_dir, "output.mp4")
    video.write_videofile(
        output_path,
        fps=24,
        codec="libx264",
        audio_codec="aac",
        verbose=False,
        logger=None,
    )
    return output_path
