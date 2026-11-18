"""Gera assets/hello.webp — um terminal que digita, apaga e acende uma ideia.

Uso: python assets/make-hello.py   (precisa de Pillow e da fonte JetBrains Mono)
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

LINES = [
    "oi, sou o matheus.",
    "pego uma ideia meio torta e transformo em algo clicável.",
    "rust, c#, python, dart, java — o que a ideia pedir.",
    "mod de minecraft? sem canos, por favor.",
    "ia local, no meu wi-fi, sem nuvem.",
    "às vezes abro um jogo por dentro só pra ver como ele pensa.",
    "se eu uso todo dia, vira ferramenta.",
]

W, H = 1200, 220
BG, BORDER = (13, 17, 23), (48, 54, 61)
TEXT, MUTED, ACCENT = (230, 237, 243), (110, 118, 129), (126, 231, 135)
BULB_OFF, BULB_ON = (60, 66, 75), (255, 214, 102)

FONT_PATH = "/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-Regular.ttf"
font = ImageFont.truetype(FONT_PATH, 26)
small = ImageFont.truetype(FONT_PATH, 20)

TYPE_MS, DELETE_MS, HOLD_MS, BLINK_MS = 55, 18, 1700, 450


def bulb(draw, on, cx=1124, cy=H // 2 + 6):
    color = BULB_ON if on else BULB_OFF
    draw.ellipse((cx - 22, cy - 44, cx + 22, cy + 2), fill=color)
    draw.rectangle((cx - 11, cy, cx + 11, cy + 14), fill=color)
    base = (150, 156, 165) if on else (75, 81, 90)
    for i in range(3):
        y = cy + 17 + i * 7
        draw.rounded_rectangle((cx - 12, y, cx + 12, y + 4), 2, fill=base)
    if on:  # raios
        for x1, y1, x2, y2 in [(-40, -22, -54, -22), (40, -22, 54, -22),
                               (-30, -50, -40, -60), (30, -50, 40, -60), (0, -56, 0, -70)]:
            draw.line((cx + x1, cy + y1, cx + x2, cy + y2), fill=BULB_ON, width=4)


def frame(text, cursor=True, lit=False):
    img = Image.new("RGB", (W, H), BG)
    if lit:  # brilho suave atrás da lâmpada
        glow = Image.new("RGB", (W, H), BG)
        ImageDraw.Draw(glow).ellipse((1054, 20, 1194, 160), fill=(70, 58, 25))
        img = glow.filter(ImageFilter.GaussianBlur(28))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((1, 1, W - 2, H - 2), 18, outline=BORDER, width=2)
    d.text((48, 42), "~/oficina", font=small, fill=MUTED)
    y = 98
    d.text((48, y), "›", font=font, fill=ACCENT)
    x = 84
    d.text((x, y), text, font=font, fill=TEXT)
    if cursor:
        cx = x + d.textlength(text, font=font) + 4
        d.rectangle((cx, y + 4, cx + 15, y + 38), fill=ACCENT)
    bulb(d, lit)
    return img


frames, durations = [], []


def add(img, ms):
    frames.append(img)
    durations.append(ms)


for line in LINES:
    for i in range(len(line) + 1):
        add(frame(line[:i]), TYPE_MS)
    # ideia pronta: acende e pisca o cursor
    for k in range(4):
        add(frame(line, cursor=k % 2 == 0, lit=True), HOLD_MS // 4)
    for i in range(len(line), -1, -1):
        add(frame(line[:i]), DELETE_MS)
    add(frame("", cursor=False), 300)

out = Path(__file__).with_name("hello.webp")
frames[0].save(out, save_all=True, append_images=frames[1:], duration=durations,
               loop=0, lossless=False, quality=80, method=6, minimize_size=True)
print(out, f"{out.stat().st_size / 1024:.0f} KiB", len(frames), "frames")
