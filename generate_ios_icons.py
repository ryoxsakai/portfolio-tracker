"""Generate iOS app icons from the stock icon design."""
import os
import math
from PIL import Image, ImageDraw, ImageFont

# iOS required icon sizes: (size, scale, usage)
IOS_SIZES = [
    1024, 180, 167, 152, 120, 87, 80, 76, 60, 58, 40, 29, 20
]

BG_COLOR = (13, 27, 62)   # dark navy blue
FG_COLOR = (255, 255, 255)


def draw_rounded_rect(draw, xy, radius, fill):
    x0, y0, x1, y1 = xy
    draw.rectangle([x0 + radius, y0, x1 - radius, y1], fill=fill)
    draw.rectangle([x0, y0 + radius, x1, y1 - radius], fill=fill)
    draw.ellipse([x0, y0, x0 + 2 * radius, y0 + 2 * radius], fill=fill)
    draw.ellipse([x1 - 2 * radius, y0, x1, y0 + 2 * radius], fill=fill)
    draw.ellipse([x0, y1 - 2 * radius, x0 + 2 * radius, y1], fill=fill)
    draw.ellipse([x1 - 2 * radius, y1 - 2 * radius, x1, y1], fill=fill)


def create_base_icon(size=1024):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    s = size
    pad = int(s * 0.04)
    radius = int(s * 0.18)

    draw_rounded_rect(draw, [pad, pad, s - pad, s - pad], radius, BG_COLOR + (255,))

    lw = max(2, int(s * 0.025))

    # Chart area bounds
    cx0 = int(s * 0.14)
    cy0 = int(s * 0.12)
    cx1 = int(s * 0.86)
    cy1 = int(s * 0.62)

    # Axes
    draw.line([(cx0, cy0), (cx0, cy1)], fill=FG_COLOR, width=lw)
    draw.line([(cx0, cy1), (cx1, cy1)], fill=FG_COLOR, width=lw)

    # Trend line points (zigzag upward)
    pts = [
        (cx0 + int((cx1 - cx0) * 0.05), cy1 - int((cy1 - cy0) * 0.20)),
        (cx0 + int((cx1 - cx0) * 0.25), cy1 - int((cy1 - cy0) * 0.35)),
        (cx0 + int((cx1 - cx0) * 0.40), cy1 - int((cy1 - cy0) * 0.28)),
        (cx0 + int((cx1 - cx0) * 0.58), cy1 - int((cy1 - cy0) * 0.55)),
        (cx0 + int((cx1 - cx0) * 0.72), cy1 - int((cy1 - cy0) * 0.48)),
        (cx0 + int((cx1 - cx0) * 0.90), cy1 - int((cy1 - cy0) * 0.78)),
    ]
    draw.line(pts, fill=FG_COLOR, width=lw)

    # Arrow at end
    end = pts[-1]
    prev = pts[-2]
    angle = math.atan2(end[1] - prev[1], end[0] - prev[0])
    alen = int(s * 0.07)
    spread = 0.5
    ax1 = (end[0] - int(alen * math.cos(angle - spread)),
           end[1] - int(alen * math.sin(angle - spread)))
    ax2 = (end[0] - int(alen * math.cos(angle + spread)),
           end[1] - int(alen * math.sin(angle + spread)))
    draw.polygon([end, ax1, ax2], fill=FG_COLOR)

    # Candlesticks
    cw = int(s * 0.04)
    candles = [
        (pts[1][0], pts[1][1] - int(s * 0.07), pts[1][1] + int(s * 0.04)),
        (pts[3][0], pts[3][1] - int(s * 0.09), pts[3][1] + int(s * 0.03)),
    ]
    for cx, ctop, cbot in candles:
        draw.line([(cx, ctop - int(s * 0.03)), (cx, cbot + int(s * 0.03))],
                  fill=FG_COLOR, width=max(1, lw // 2))
        draw.rectangle([cx - cw // 2, ctop, cx + cw // 2, cbot],
                       fill=FG_COLOR)

    # "STOCK" text
    text = "STOCK"
    font_size = int(s * 0.13)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
    except Exception:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    tx = (s - tw) // 2
    ty = int(s * 0.71)
    draw.text((tx, ty), text, fill=FG_COLOR, font=font)

    return img


def main():
    out_dir = "ios_icons"
    os.makedirs(out_dir, exist_ok=True)

    print("Generating base 1024x1024 icon...")
    base = create_base_icon(1024)

    for size in IOS_SIZES:
        resized = base.resize((size, size), Image.LANCZOS)
        filename = f"{out_dir}/icon_{size}x{size}.png"
        resized.save(filename, "PNG")
        print(f"  Saved {filename}")

    print(f"\nDone! {len(IOS_SIZES)} icons saved to '{out_dir}/'")
    print("\niOS Icon Size Reference:")
    print("  1024x1024 - App Store")
    print("  180x180   - iPhone @3x (60pt)")
    print("  167x167   - iPad Pro @2x (83.5pt)")
    print("  152x152   - iPad @2x (76pt)")
    print("  120x120   - iPhone @2x (60pt) / @3x (40pt)")
    print("  87x87     - iPhone @3x (29pt)")
    print("  80x80     - iPhone/iPad @2x (40pt)")
    print("  76x76     - iPad @1x (76pt)")
    print("  60x60     - iPhone @3x (20pt)")
    print("  58x58     - iPhone/iPad @2x (29pt)")
    print("  40x40     - iPhone/iPad @1x (40pt) / @2x (20pt)")
    print("  29x29     - iPhone/iPad @1x (29pt)")
    print("  20x20     - iPhone/iPad @1x (20pt)")


if __name__ == "__main__":
    main()
