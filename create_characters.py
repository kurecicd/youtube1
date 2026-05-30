"""Run once to generate cartoon character reference images saved to assets/."""

import os
import base64
from io import BytesIO
from PIL import Image
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
os.makedirs("assets", exist_ok=True)


def generate(prompt: str, filename: str):
    print(f"Generating {filename}...")
    response = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1024x1024",
        quality="high",
        n=1,
    )
    img_data = base64.b64decode(response.data[0].b64_json)
    Image.open(BytesIO(img_data)).save(f"assets/{filename}")
    print(f"Saved assets/{filename}")


generate(
    """Pixar/Disney animated movie character sheet, white background. Two brothers side by side, full body, labeled with names:

LEFT — TOBIAS: toddler boy ~2 years old. Platinum white-blonde hair. Enormous bright blue eyes. Very chubby round cheeks. Tiny button nose. Sweet giggling smile. Blue hoodie, grey pants. Very small and round.

RIGHT — SAMUEL: boy ~7 years old. Golden blonde hair. Bright eyes. Confident happy smile. Athletic. Red t-shirt, dark shorts. Much taller than Tobias.

Same Pixar cartoon style for both. Vibrant colors, clean outlines, white background.""",
    "characters.png",
)

generate(
    """Pixar/Disney animated movie character sheet, white background. Two parents, full body, labeled:

LEFT — DAD: tall man, dark brown hair, friendly short beard, warm smile, broad shoulders, casual clothes.

RIGHT — MUM: woman, dark hair, round glasses, kind loving smile, warm expression, casual clothes.

Same Pixar cartoon style. Vibrant colors, clean outlines, white background.""",
    "parents.png",
)

print("\nDone! Check assets/characters.png and assets/parents.png")
