from functools import partial
from io import BytesIO
from pathlib import Path
from typing import Tuple, cast

from pil_utils import BuildImage, Text2Image
from pydantic.color import Color
from pydantic.color import ColorTuple as PyDanticColorTuple

RGBColorTuple = Tuple[int, int, int]
RGBAColorTuple = Tuple[int, int, int, int]

RES_PATH = Path(__file__).parent / "res"
FONT_PATH = RES_PATH / "HarmonyOS_Sans_Bold.ttf"

PADDING = 24
IMG_SIZE = 256
TITLE_FONT_SIZE = 48
SUB_FONT_SIZE = 24
HAS_ALPHA_SIZE_MULTIPLIER = 0.75


def reverse_color(rgb: RGBColorTuple) -> RGBColorTuple:
    return cast(RGBColorTuple, tuple(255 - i for i in rgb))


def trans_pydantic_rgb(color: PyDanticColorTuple) -> RGBAColorTuple:
    if len(color) == 4:
        return (*color[:3], int(color[3] * 255))
    return (*color, 255)


async def generate_image(color: Color) -> BytesIO:
    pydantic_color = color.as_rgb_tuple()
    bg_color = trans_pydantic_rgb(pydantic_color)
    rgb, alpha = bg_color[:3], bg_color[3]

    font_name = str(FONT_PATH)
    text_color = (*reverse_color(rgb), alpha)

    has_alpha = len(pydantic_color) == 4
    sub_size = SUB_FONT_SIZE
    if has_alpha:
        sub_size = round(sub_size * HAS_ALPHA_SIZE_MULTIPLIER)

    build = partial(Text2Image.from_text, fill=text_color, fontname=font_name)
    hex_text = build(color.as_hex(), TITLE_FONT_SIZE)
    rgb_text = build(color.as_rgb(), sub_size)
    hsl_text = build(color.as_hsl(), sub_size)

    gap_size = round(
        (
            IMG_SIZE
            - (PADDING * 2)
            - sum(x.height for x in (hex_text, rgb_text, hsl_text))
        )
        / 4,
    )

    img = BuildImage.new("RGBA", (IMG_SIZE, IMG_SIZE), bg_color)
    y_offset = PADDING + gap_size
    for text in (hex_text, rgb_text, hsl_text):
        text.draw_on_image(
            img.image,
            (round((IMG_SIZE - text.width) / 2), y_offset),
        )
        y_offset += text.height + gap_size

    return img.save_png()
