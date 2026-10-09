"""
Synthetic Nepali Number Plate Generator.
Generates synthetic plates with various backgrounds (Private Red, Commercial Black, Govt White)
for training OCR models before collecting extensive real-world datasets.
"""

import random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from src.rules.nepali_plates import (
    PROVINCES_DEVANAGARI,
    ZONES_DEVANAGARI,
    NEPALI_VEHICLE_SYMBOLS,
    arabic_to_devanagari_digits,
)

# Plate Color Configurations (Background, Text Color)
PLATE_THEMES = {
    "private": {"bg": (180, 20, 20), "text": (255, 255, 255)},      # Red with White
    "commercial": {"bg": (20, 20, 20), "text": (255, 255, 255)},    # Black with White
    "government": {"bg": (240, 240, 240), "text": (180, 20, 20)},   # White with Red
}


def generate_random_plate_text() -> tuple[str, str]:
    """Generates a random valid Nepali plate string (Line 1, Line 2)."""
    province = random.choice(PROVINCES_DEVANAGARI)
    lot = arabic_to_devanagari_digits(str(random.randint(1, 99)).zfill(2))
    category = random.choice(list(NEPALI_VEHICLE_SYMBOLS.keys()))
    number = arabic_to_devanagari_digits(str(random.randint(1, 9999)).zfill(4))
    
    line1 = f"{province} {lot}"
    line2 = f"{category} {number}"
    return line1, line2


def generate_synthetic_plate(
    width: int = 400,
    height: int = 150,
    theme_name: str = "private",
    output_path: Path | None = None
) -> Image.Image:
    """Creates a synthetic plate image."""
    theme = PLATE_THEMES.get(theme_name, PLATE_THEMES["private"])
    img = Image.new("RGB", (width, height), color=theme["bg"])
    draw = ImageDraw.Draw(img)
    
    # Border
    draw.rectangle([4, 4, width - 5, height - 5], outline=theme["text"], width=3)
    
    line1, line2 = generate_random_plate_text()
    
    # In standard setup, load a Devanagari TTF font (e.g. Kalimati/NotoSansDevanagari)
    # If font file is not present, use default font
    try:
        font = ImageFont.truetype("/usr/share/fonts/google-noto/NotoSansDevanagari-Bold.ttf", 36)
        small_font = ImageFont.truetype("/usr/share/fonts/google-noto/NotoSansDevanagari-Bold.ttf", 28)
    except IOError:
        font = ImageFont.load_default()
        small_font = font

    draw.text((width // 4, height // 5), line1, fill=theme["text"], font=small_font)
    draw.text((width // 4, height // 2), line2, fill=theme["text"], font=font)
    
    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        img.save(output_path)
        
    return img


if __name__ == "__main__":
    out_dir = Path("data/synthetic")
    print(f"Generating 5 sample synthetic plates in {out_dir}...")
    for i in range(5):
        theme = random.choice(list(PLATE_THEMES.keys()))
        dest = out_dir / f"sample_{i+1}_{theme}.png"
        generate_synthetic_plate(theme_name=theme, output_path=dest)
    print("Done! Check data/synthetic/ for samples.")
