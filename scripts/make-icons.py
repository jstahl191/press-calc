#!/usr/bin/env python3
"""Generate home-screen PNGs: dark #111 background, red #c8102e MWM wordmark."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

BG = (0x11, 0x11, 0x11)
RED = (0xC8, 0x10, 0x2E)
FONT_PATH = "/usr/share/fonts/truetype/macos/Inter-Bold.ttf"
ROOT = Path(__file__).resolve().parents[1]


def render(size: int) -> Image.Image:
    img = Image.new("RGB", (size, size), BG)
    draw = ImageDraw.Draw(img)
    target_w = int(size * 0.72)
    target_h = int(size * 0.38)
    lo, hi, best = 8, size, 8
    while lo <= hi:
        mid = (lo + hi) // 2
        font = ImageFont.truetype(FONT_PATH, mid)
        bbox = draw.textbbox((0, 0), "MWM", font=font)
        width = bbox[2] - bbox[0]
        height = bbox[3] - bbox[1]
        if width <= target_w and height <= target_h:
            best = mid
            lo = mid + 1
        else:
            hi = mid - 1
    font = ImageFont.truetype(FONT_PATH, best)
    bbox = draw.textbbox((0, 0), "MWM", font=font)
    width = bbox[2] - bbox[0]
    height = bbox[3] - bbox[1]
    x = (size - width) / 2 - bbox[0]
    y = (size - height) / 2 - bbox[1] - size * 0.03
    draw.text((x, y), "MWM", font=font, fill=RED)
    bar_w = int(width * 0.62)
    bar_h = max(3, size // 42)
    bar_x = (size - bar_w) // 2
    bar_y = int(y + bbox[3] + size * 0.045)
    radius = bar_h // 2
    draw.rounded_rectangle(
        (bar_x, bar_y, bar_x + bar_w, bar_y + bar_h),
        radius=radius,
        fill=RED,
    )
    return img


def main() -> None:
    for name, size in (
        ("apple-touch-icon.png", 180),
        ("icon-192.png", 192),
        ("icon-512.png", 512),
    ):
        path = ROOT / name
        render(size).save(path, "PNG", optimize=True)
        print(f"{path.name} {size}x{size}")


if __name__ == "__main__":
    main()
