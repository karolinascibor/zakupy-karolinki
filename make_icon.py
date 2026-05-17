#!/usr/bin/env python3
"""Generate cute PWA icons for Zakupy Karolinki."""
from PIL import Image, ImageDraw, ImageFilter
import os

OUT = os.path.dirname(os.path.abspath(__file__))


def make_icon(size: int, maskable: bool = False) -> Image.Image:
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    # Background: soft coral/pink gradient (top -> bottom)
    top = (255, 175, 189)      # #FFAFBD
    bot = (255, 195, 160)      # #FFC3A0
    for y in range(size):
        t = y / size
        r = int(top[0] * (1 - t) + bot[0] * t)
        g = int(top[1] * (1 - t) + bot[1] * t)
        b = int(top[2] * (1 - t) + bot[2] * t)
        d.line([(0, y), (size, y)], fill=(r, g, b, 255))

    # Apply rounded mask. For maskable icons, the safe-zone is the inner 80%.
    # Non-maskable uses generous rounded corners (iOS adds its own mask too).
    radius = int(size * 0.22)
    mask = Image.new("L", (size, size), 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle((0, 0, size, size), radius=radius, fill=255)
    bg = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    bg.paste(img, (0, 0), mask)
    img = bg
    d = ImageDraw.Draw(img)

    # Bag scale: maskable should fit inside inner 80%
    scale = 0.62 if maskable else 0.72
    bw = int(size * scale)
    bh = int(bw * 0.95)
    bx = (size - bw) // 2
    by = (size - bh) // 2 + int(size * 0.06)

    white = (255, 255, 255, 255)
    shadow = (0, 0, 0, 35)

    # Soft drop shadow under bag
    shadow_img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow_img)
    sd.rounded_rectangle(
        (bx + size * 0.02, by + size * 0.05, bx + bw + size * 0.02, by + bh + size * 0.05),
        radius=int(bw * 0.18),
        fill=shadow,
    )
    shadow_img = shadow_img.filter(ImageFilter.GaussianBlur(radius=size * 0.02))
    img = Image.alpha_composite(img, shadow_img)
    d = ImageDraw.Draw(img)

    # Bag body (rounded rect)
    d.rounded_rectangle(
        (bx, by, bx + bw, by + bh), radius=int(bw * 0.18), fill=white
    )

    # Bag handles (two arcs above the bag)
    handle_w = int(bw * 0.22)
    handle_h = int(bh * 0.45)
    handle_thick = max(3, int(size * 0.035))
    handle_y_top = by - int(handle_h * 0.7)
    # Left handle
    lhx = bx + int(bw * 0.22)
    d.arc(
        (lhx, handle_y_top, lhx + handle_w, handle_y_top + handle_h),
        start=180,
        end=360,
        fill=white,
        width=handle_thick,
    )
    # Right handle
    rhx = bx + bw - int(bw * 0.22) - handle_w
    d.arc(
        (rhx, handle_y_top, rhx + handle_w, handle_y_top + handle_h),
        start=180,
        end=360,
        fill=white,
        width=handle_thick,
    )

    # Heart on the bag
    cx = bx + bw // 2
    cy = by + int(bh * 0.55)
    hs = int(bw * 0.32)  # heart half-width
    heart_color = (255, 99, 132, 255)  # bright pink/red

    # Two circles + triangle (classic heart)
    r = hs // 2
    d.ellipse((cx - hs, cy - r, cx, cy + r), fill=heart_color)
    d.ellipse((cx, cy - r, cx + hs, cy + r), fill=heart_color)
    d.polygon(
        [(cx - hs, cy + r // 3), (cx + hs, cy + r // 3), (cx, cy + int(hs * 1.05))],
        fill=heart_color,
    )

    # Tiny highlight on the heart for kawaii sheen
    hl = int(hs * 0.25)
    d.ellipse(
        (cx - int(hs * 0.55), cy - int(r * 0.55), cx - int(hs * 0.55) + hl, cy - int(r * 0.55) + hl),
        fill=(255, 255, 255, 220),
    )

    # Sparkles around the bag (small white dots)
    sparkles = [
        (bx - int(bw * 0.08), by + int(bh * 0.15), int(size * 0.025)),
        (bx + bw + int(bw * 0.04), by + int(bh * 0.30), int(size * 0.020)),
        (bx + bw + int(bw * 0.02), by + bh - int(bh * 0.10), int(size * 0.028)),
        (bx - int(bw * 0.04), by + bh - int(bh * 0.20), int(size * 0.018)),
    ]
    for sx, sy, sr in sparkles:
        d.ellipse((sx - sr, sy - sr, sx + sr, sy + sr), fill=(255, 255, 255, 230))

    return img


def save(img: Image.Image, name: str) -> None:
    path = os.path.join(OUT, name)
    img.save(path, "PNG", optimize=True)
    print(f"wrote {path}  ({img.size[0]}x{img.size[1]})")


if __name__ == "__main__":
    # Standard sizes
    save(make_icon(180), "apple-touch-icon.png")            # iOS home screen
    save(make_icon(192), "icon-192.png")                    # PWA manifest
    save(make_icon(512), "icon-512.png")                    # PWA manifest
    save(make_icon(512, maskable=True), "icon-512-maskable.png")  # Android maskable
    save(make_icon(32), "favicon-32.png")
