"""Draw the app icons (navy tile with a small value-bridge chart)."""
import sys
from PIL import Image, ImageDraw
NAVY, SKY, WHITE, AMBER = (21, 70, 129), (95, 180, 234), (255, 255, 255), (242, 179, 61)
def tile(size, pad_ratio, radius_ratio):
    S = size * 4
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if radius_ratio is None: d.rectangle([0, 0, S, S], fill=NAVY)
    else: d.rounded_rectangle([0, 0, S - 1, S - 1], radius=int(S * radius_ratio), fill=NAVY)
    pad = S * pad_ratio; w = S - 2 * pad; base = pad + w * 0.86
    bw = w * 0.17; gap = (w - 4 * bw) / 3
    levels = [(0.0, 0.50, SKY), (0.50, 0.66, AMBER), (0.66, 0.80, WHITE), (0.0, 0.80, WHITE)]
    for i, (a, b, col) in enumerate(levels):
        x = pad + i * (bw + gap)
        y_top = base - w * 0.80 * b / 0.80 * 0.95; y_bot = base - w * 0.80 * a / 0.80 * 0.95
        d.rounded_rectangle([x, y_top, x + bw, y_bot], radius=int(bw * 0.12), fill=col)
    d.rectangle([pad - w * 0.02, base, pad + w * 1.02, base + w * 0.035], fill=(255, 255, 255, 170))
    return im.resize((size, size), Image.LANCZOS)
out = sys.argv[1]
tile(512, 0.20, 0.22).save(out + "/icon-512.png")
tile(192, 0.20, 0.22).save(out + "/icon-192.png")
tile(512, 0.26, None).save(out + "/maskable-512.png")
tile(180, 0.18, None).convert("RGB").save(out + "/apple-touch-icon.png")
tile(32, 0.12, 0.18).save(out + "/favicon-32.png")
