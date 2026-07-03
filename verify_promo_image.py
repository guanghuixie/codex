from pathlib import Path

from PIL import Image, ImageStat


ROOT = Path(__file__).resolve().parent
IMAGE_PATH = ROOT / "guoqing-beer-festival-promo.png"
GENERATOR_PATH = ROOT / "generate_guoqing_beer_promo.py"
EXPECTED_TEXT = [
    "国庆啤酒节",
    "消费满100元",
    "送3瓶啤酒",
    "畅饮黄金周 · 举杯庆国庆",
    "活动详情请咨询门店",
]


def assert_true(condition, message):
    if not condition:
        raise AssertionError(message)


def main():
    assert_true(IMAGE_PATH.exists(), f"missing image: {IMAGE_PATH}")
    assert_true(GENERATOR_PATH.exists(), f"missing generator: {GENERATOR_PATH}")

    with Image.open(IMAGE_PATH) as image:
        assert_true(image.size == (1080, 1920), f"unexpected image size: {image.size}")
        assert_true(image.mode in {"RGB", "RGBA"}, f"unexpected image mode: {image.mode}")

        stat = ImageStat.Stat(image.convert("RGB"))
        channel_ranges = [hi - lo for lo, hi in stat.extrema]
        assert_true(min(channel_ranges) > 120, f"image lacks color contrast: {channel_ranges}")

        center = image.convert("RGB").crop((120, 780, 960, 1320))
        center_stat = ImageStat.Stat(center)
        center_brightness = sum(center_stat.mean) / 3
        assert_true(center_brightness > 35, "central beer visual area is too dark")

    generator_source = GENERATOR_PATH.read_text(encoding="utf-8")
    for text in EXPECTED_TEXT:
        assert_true(text in generator_source, f"missing expected text in generator: {text}")

    print("Promo image verification passed")


if __name__ == "__main__":
    main()
