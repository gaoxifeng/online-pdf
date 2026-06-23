#!/usr/bin/env python
"""Generate the online-pdf PWA icon set.

Brand: blue #2f6fed -> #1b54c8 rounded-square, white document glyph with a
folded corner, and a red "PDF" tag (the universally-recognised PDF cue).
Rendered 4x-supersampled then downscaled with LANCZOS for clean anti-aliasing.

Run:  python make_icons.py
Outputs into the same folder as this script.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
SS = 4  # supersample factor

C1 = (47, 111, 237)   # --pri
C2 = (27, 84, 200)    # --pri2
PAPER = (255, 255, 255)
FOLD = (210, 221, 244)
LINE = (171, 190, 230)
RED = (192, 57, 43)   # --bad, classic PDF tag


def _font(px):
    for name in ("segoeuib.ttf", "arialbd.ttf", "seguisb.ttf", "calibrib.ttf"):
        try:
            return ImageFont.truetype(name, px)
        except OSError:
            continue
    return ImageFont.load_default()


def _vgradient(w, h, top, bottom):
    grad = Image.new("RGB", (w, h))
    px = grad.load()
    for y in range(h):
        t = y / max(1, h - 1)
        px_row = tuple(round(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
        for x in range(w):
            px[x, y] = px_row
    return grad


def draw_icon(size, maskable=False):
    W = size * SS
    img = Image.new("RGBA", (W, W), (0, 0, 0, 0))

    # ---- background (rounded square; full-bleed for maskable) ----
    radius = 0 if maskable else int(W * 0.22)
    mask = Image.new("L", (W, W), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, W - 1, W - 1], radius=radius, fill=255)
    img.paste(_vgradient(W, W, C1, C2), (0, 0), mask)

    d = ImageDraw.Draw(img)

    # ---- document glyph (smaller inside maskable safe zone) ----
    span = 0.60 if maskable else 0.70          # fraction of canvas the page spans
    dw = W * span * 0.80
    dh = dw * 1.28
    cx, cy = W / 2, W / 2
    L, T, R, B = cx - dw / 2, cy - dh / 2, cx + dw / 2, cy + dh / 2
    fold = dw * 0.30                            # folded-corner size
    rr = dw * 0.07                              # page corner radius

    # subtle drop shadow
    sh = Image.new("RGBA", (W, W), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle(
        [L, T + dh * 0.03, R, B + dh * 0.03], radius=rr, fill=(0, 0, 0, 70))
    img.alpha_composite(sh.filter(__import__("PIL.ImageFilter", fromlist=["GaussianBlur"]).GaussianBlur(W * 0.012)))
    d = ImageDraw.Draw(img)

    # page body with a clipped top-right corner
    body = [(L + rr, T), (R - fold, T), (R, T + fold), (R, B - rr),
            (R - rr, B), (L + rr, B), (L, B - rr), (L, T + rr)]
    d.polygon(body, fill=PAPER)
    # round the square-ish corners back a touch
    d.rounded_rectangle([L, T, R, B], radius=rr, fill=None)
    # the folded corner
    d.polygon([(R - fold, T), (R, T + fold), (R - fold, T + fold)], fill=FOLD)

    # ---- text lines on the page ----
    lh = dh * 0.052
    lx0, lx1 = L + dw * 0.16, R - dw * 0.16
    for i, frac in enumerate((0.30, 0.40, 0.50)):
        y = T + dh * frac
        x1 = lx1 if i < 2 else lx0 + (lx1 - lx0) * 0.62
        d.rounded_rectangle([lx0, y, x1, y + lh], radius=lh / 2, fill=LINE)

    # ---- red PDF tag ----
    tw, th = dw * 0.86, dh * 0.26
    tx0, ty0 = cx - tw / 2, B - dh * 0.30
    d.rounded_rectangle([tx0, ty0, tx0 + tw, ty0 + th], radius=th * 0.22, fill=RED)
    f = _font(int(th * 0.62))
    label = "PDF"
    bb = d.textbbox((0, 0), label, font=f)
    d.text((cx - (bb[2] - bb[0]) / 2 - bb[0], ty0 + th / 2 - (bb[3] - bb[1]) / 2 - bb[1]),
           label, font=f, fill=PAPER)

    return img.resize((size, size), Image.LANCZOS)


def main():
    jobs = [
        ("icon-192.png", 192, False),
        ("icon-256.png", 256, False),
        ("icon-512.png", 512, False),
        ("maskable-512.png", 512, True),
        ("apple-touch-icon.png", 180, False),
        ("favicon-32.png", 32, False),
    ]
    for name, size, mask in jobs:
        draw_icon(size, mask).save(os.path.join(HERE, name))
        print("wrote", name, size)

    # multi-resolution .ico for the browser tab / Windows
    ico = draw_icon(64, False)
    ico.save(os.path.join(HERE, "favicon.ico"),
             sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64)])
    print("wrote favicon.ico")


if __name__ == "__main__":
    main()
