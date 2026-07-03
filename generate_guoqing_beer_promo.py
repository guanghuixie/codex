from math import cos, pi, sin
from pathlib import Path
import random

from PIL import Image, ImageDraw, ImageFilter, ImageFont


WIDTH = 1080
HEIGHT = 1920
ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "guoqing-beer-festival-promo.png"
FONT_BOLD = "/System/Library/Fonts/Hiragino Sans GB.ttc"
FONT_HEITI = "/System/Library/Fonts/STHeiti Medium.ttc"
HEADLINE = "国庆啤酒节"
OFFER_LINE = "消费满100元"
GIFT_LINE = "送3瓶啤酒"
SUBTITLE = "畅饮黄金周 · 举杯庆国庆"
FOOTNOTE = "活动详情请咨询门店"


def font(size, bold=True):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_HEITI, size=size)


def text_center(draw, xy, text, font_obj, fill, stroke_width=0, stroke_fill=None):
    x, y = xy
    box = draw.textbbox((0, 0), text, font=font_obj, stroke_width=stroke_width)
    tw = box[2] - box[0]
    draw.text(
        (x - tw / 2, y),
        text,
        font=font_obj,
        fill=fill,
        stroke_width=stroke_width,
        stroke_fill=stroke_fill,
    )


def rounded_rectangle(draw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def add_glow(base, shape_fn, color, blur=32):
    glow = Image.new("RGBA", base.size, (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow)
    shape_fn(gdraw)
    glow = glow.filter(ImageFilter.GaussianBlur(blur))
    tint = Image.new("RGBA", base.size, color)
    glow = Image.composite(tint, Image.new("RGBA", base.size, (0, 0, 0, 0)), glow)
    base.alpha_composite(glow)


def gradient_background():
    image = Image.new("RGBA", (WIDTH, HEIGHT), (5, 8, 22, 255))
    pixels = image.load()
    for y in range(HEIGHT):
        t = y / HEIGHT
        for x in range(WIDTH):
            side = abs(x - WIDTH / 2) / (WIDTH / 2)
            r = int(7 + 35 * (1 - side) * (1 - t) + 38 * t)
            g = int(10 + 23 * (1 - side) + 12 * t)
            b = int(29 + 52 * (1 - side) + 10 * t)
            pixels[x, y] = (r, g, b, 255)
    return image


def draw_grid(draw):
    for x in range(0, WIDTH, 90):
        alpha = 34 if x % 180 else 56
        draw.line((x, 0, x, HEIGHT), fill=(23, 219, 255, alpha), width=1)
    for y in range(0, HEIGHT, 90):
        alpha = 30 if y % 180 else 48
        draw.line((0, y, WIDTH, y), fill=(23, 219, 255, alpha), width=1)


def draw_firework(draw, center, radius, color):
    cx, cy = center
    for i in range(18):
        angle = i * 2 * pi / 18
        start = radius * 0.25
        end = radius * (0.75 + 0.2 * (i % 3))
        draw.line(
            (
                cx + cos(angle) * start,
                cy + sin(angle) * start,
                cx + cos(angle) * end,
                cy + sin(angle) * end,
            ),
            fill=color,
            width=4,
        )
    draw.ellipse((cx - 9, cy - 9, cx + 9, cy + 9), fill=color)


def draw_beer_bottle(base, x, y, scale=1.0, tilt=0):
    w = int(105 * scale)
    h = int(440 * scale)
    neck_w = int(43 * scale)
    neck_h = int(150 * scale)
    body = Image.new("RGBA", (w + 80, h + 80), (0, 0, 0, 0))
    bd = ImageDraw.Draw(body)
    bx = 40
    by = 20
    glass = (20, 92, 67, 245)
    edge = (80, 255, 192, 185)
    bd.rounded_rectangle((bx + (w - neck_w) / 2, by, bx + (w + neck_w) / 2, by + neck_h), radius=16, fill=glass)
    bd.rectangle((bx + (w - neck_w) / 2 + 5, by - 10, bx + (w + neck_w) / 2 - 5, by + 18), fill=(235, 194, 76, 255))
    bd.rounded_rectangle((bx, by + neck_h - 8, bx + w, by + h), radius=44, fill=glass, outline=edge, width=3)
    bd.rounded_rectangle((bx + 18, by + neck_h + 90, bx + w - 18, by + neck_h + 200), radius=18, fill=(238, 34, 42, 255), outline=(255, 221, 97, 255), width=5)
    bd.text((bx + 26, by + neck_h + 112), "BEER", font=font(int(27 * scale)), fill=(255, 232, 142, 255))
    bd.line((bx + 28, by + neck_h + 22, bx + 28, by + h - 35), fill=(161, 255, 216, 86), width=7)
    body = body.rotate(tilt, resample=Image.Resampling.BICUBIC, expand=True)
    shadow = body.filter(ImageFilter.GaussianBlur(18))
    shadow_layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    shadow_layer.paste(Image.new("RGBA", shadow.size, (0, 0, 0, 100)), (x + 10, y + 20), shadow.split()[-1])
    base.alpha_composite(shadow_layer)
    base.alpha_composite(body, (x, y))


def draw_beer_mug(base, x, y):
    mug = Image.new("RGBA", (470, 600), (0, 0, 0, 0))
    d = ImageDraw.Draw(mug)

    d.rounded_rectangle((86, 130, 342, 540), radius=42, fill=(255, 185, 36, 216), outline=(255, 245, 166, 255), width=7)
    d.rounded_rectangle((332, 230, 438, 430), radius=52, fill=(0, 0, 0, 0), outline=(255, 230, 139, 230), width=26)
    d.rounded_rectangle((116, 164, 164, 518), radius=22, fill=(255, 239, 122, 85))
    d.rounded_rectangle((205, 164, 246, 518), radius=20, fill=(255, 236, 111, 62))
    d.rounded_rectangle((280, 164, 316, 518), radius=18, fill=(255, 236, 111, 48))

    foam = [(72, 103, 152, 185), (126, 76, 236, 172), (214, 91, 322, 184), (286, 112, 376, 192)]
    for box in foam:
        d.ellipse(box, fill=(255, 247, 214, 255), outline=(255, 255, 255, 220), width=4)
    d.rounded_rectangle((92, 142, 340, 214), radius=32, fill=(255, 248, 220, 255))
    for cx, cy, r in [(150, 290, 8), (292, 350, 7), (196, 410, 6), (268, 462, 5), (226, 248, 5)]:
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(255, 244, 157, 150))

    glow = mug.filter(ImageFilter.GaussianBlur(24))
    glow_layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    glow_layer.paste(Image.new("RGBA", mug.size, (255, 174, 34, 74)), (x, y), glow.split()[-1])
    base.alpha_composite(glow_layer)
    base.alpha_composite(mug, (x, y))


def draw_neon_arc(draw):
    for offset, color, width in [
        (0, (20, 230, 255, 180), 6),
        (18, (255, 35, 92, 150), 5),
        (36, (255, 211, 72, 132), 4),
    ]:
        draw.arc((100 + offset, 484 + offset, 980 - offset, 1336 - offset), 198, 344, fill=color, width=width)


def draw_main_offer(draw):
    rounded_rectangle(draw, (88, 1264, 992, 1628), 42, (110, 16, 32, 218), (255, 214, 91, 230), 4)
    draw.line((146, 1366, 934, 1366), fill=(255, 232, 151, 110), width=2)
    text_center(draw, (540, 1308), OFFER_LINE[:3], font(70), (255, 238, 188, 255), 2, (94, 21, 22, 255))
    text_center(draw, (442, 1384), "100", font(178), (255, 225, 82, 255), 5, (87, 17, 14, 255))
    draw.text((604, 1438), OFFER_LINE[-1], font=font(72), fill=(255, 238, 190, 255), stroke_width=2, stroke_fill=(94, 21, 22, 255))
    text_center(draw, (540, 1532), GIFT_LINE, font(92), (255, 255, 255, 255), 4, (86, 13, 19, 255))


def draw_poster():
    random.seed(1003)
    image = gradient_background()
    draw = ImageDraw.Draw(image, "RGBA")

    draw_grid(draw)
    add_glow(image, lambda d: d.ellipse((120, 130, 960, 980), fill=(255, 172, 35, 112)), (255, 172, 35, 72), 76)
    add_glow(image, lambda d: d.ellipse((-160, 460, 380, 1360), fill=(0, 231, 255, 95)), (0, 231, 255, 64), 86)
    add_glow(image, lambda d: d.ellipse((780, 520, 1300, 1430), fill=(255, 36, 98, 86)), (255, 36, 98, 62), 86)

    draw.rectangle((0, 0, WIDTH, 230), fill=(169, 12, 29, 210))
    draw.polygon([(0, 230), (WIDTH, 130), (WIDTH, 260), (0, 360)], fill=(115, 8, 28, 180))
    for i in range(5):
        cx = 94 + i * 46
        cy = 88 + (i % 2) * 18
        r = 7 if i else 23
        pts = []
        for n in range(10):
            angle = -pi / 2 + n * pi / 5
            rr = r if n % 2 == 0 else r * 0.42
            pts.append((cx + cos(angle) * rr, cy + sin(angle) * rr))
        draw.polygon(pts, fill=(255, 224, 92, 255))

    draw_firework(draw, (870, 290), 88, (255, 213, 91, 192))
    draw_firework(draw, (168, 424), 64, (37, 232, 255, 154))
    draw_firework(draw, (916, 594), 54, (255, 70, 111, 150))

    text_center(draw, (540, 262), HEADLINE, font(118), (255, 243, 191, 255), 5, (92, 10, 18, 255))
    text_center(draw, (540, 398), SUBTITLE, font(44, False), (141, 246, 255, 255), 2, (11, 27, 48, 255))
    rounded_rectangle(draw, (272, 458, 808, 516), 29, (8, 22, 42, 170), (42, 229, 255, 190), 2)
    text_center(draw, (540, 468), "夜场福利限时开启", font(35, False), (255, 227, 135, 255))

    draw_neon_arc(draw)
    draw_beer_bottle(image, 126, 728, 0.98, -12)
    draw_beer_bottle(image, 776, 724, 0.92, 12)
    draw_beer_mug(image, 318, 630)

    for _ in range(42):
        x = random.randint(92, 990)
        y = random.randint(630, 1210)
        r = random.randint(4, 13)
        draw.ellipse((x - r, y - r, x + r, y + r), fill=(255, 240, 173, random.randint(48, 130)))

    draw_main_offer(draw)
    rounded_rectangle(draw, (192, 1664, 888, 1748), 42, (5, 13, 28, 208), (39, 231, 255, 156), 2)
    text_center(draw, (540, 1686), FOOTNOTE, font(42, False), (198, 226, 236, 255))
    text_center(draw, (540, 1816), "HAPPY NATIONAL DAY · BEER FESTIVAL", font(32, False), (255, 221, 128, 185))

    image = image.convert("RGB")
    image.save(OUTPUT, quality=96)


if __name__ == "__main__":
    draw_poster()
    print(OUTPUT)
