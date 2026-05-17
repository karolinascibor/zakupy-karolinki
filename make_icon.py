#!/usr/bin/env python3
"""Generate PWA icons from the puppy image for Zakupy Karolinki."""
from PIL import Image
import os

OUT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(OUT, "puppy-source.png")

# Cream/warm-white background sampled from the icon scene (safe-zone fill)
BG = (250, 240, 228, 255)


def main() -> None:
    if not os.path.exists(SRC):
        raise SystemExit(f"missing source: {SRC}")
    src = Image.open(SRC).convert("RGBA")
    w, h = src.size
    if w != h:
        s = min(w, h)
        src = src.crop(((w - s) // 2, (h - s) // 2, (w + s) // 2, (h + s) // 2))

    sizes = {
        "apple-touch-icon.png": 180,
        "icon-192.png": 192,
        "icon-512.png": 512,
        "favicon-32.png": 32,
    }
    for name, size in sizes.items():
        img = src.resize((size, size), Image.LANCZOS)
        path = os.path.join(OUT, name)
        img.save(path, "PNG", optimize=True)
        print(f"wrote {path}  ({size}x{size})")

    # Maskable: keep critical content in inner ~78% safe-zone
    mask_size = 512
    inner = int(mask_size * 0.78)
    maskable = Image.new("RGBA", (mask_size, mask_size), BG)
    resized = src.resize((inner, inner), Image.LANCZOS)
    off = (mask_size - inner) // 2
    maskable.paste(resized, (off, off), resized)
    p = os.path.join(OUT, "icon-512-maskable.png")
    maskable.save(p, "PNG", optimize=True)
    print(f"wrote {p}  ({mask_size}x{mask_size} maskable)")


if __name__ == "__main__":
    main()
