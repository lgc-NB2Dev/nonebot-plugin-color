import re
from contextlib import suppress
from functools import partial
from io import BytesIO
from pathlib import Path
from typing import List, Optional, Tuple, Union, cast

from nonebot import logger
from nonebot.compat import PYDANTIC_V2
from PIL import Image
from pil_utils import BuildImage, Text2Image
from pil_utils.gradient import ColorStop, LinearGradient
from pil_utils.types import ColorType

from .config import config
from .const import COLOR_CHINESE_NAME_MAP

PyDanticColorTuple = Union[Tuple[int, int, int], Tuple[int, int, int, float]]

if PYDANTIC_V2:
    from pydantic_core import PydanticCustomError as ColorError

    try:
        from pydantic_extra_types.color import Color
    except ImportError:
        logger.warning(
            "Missing suggested dependency, "
            "please use `pip install nonebot-plugin-color[pyd2]` to install",
        )
        logger.warning("Fallback to pydantic deprecated Color class")
        from pydantic.color import Color

else:
    from pydantic.color import Color
    from pydantic.errors import ColorError


RGBColorTuple = Tuple[int, int, int]
RGBAColorTuple = Tuple[int, int, int, int]

RES_PATH = Path(__file__).parent / "res"
FONT_PATH = RES_PATH / "HarmonyOS_Sans_Bold.ttf"
FONT_NAME = str(FONT_PATH)

PADDING = 24
IMG_SIZE = 256
TITLE_FONT_SIZE = 48
SUB_FONT_SIZE = 24
SMALL_SIZE_MULTIPLIER = 0.75


HEX_REGEX = re.compile(r"([0-9a-fA-F]{3,4}){1,2}")


class NotValidColorError(ValueError):
    def __init__(self, color: str) -> None:
        self.color = color


def parse_color(color: str) -> Color:
    if config.color_hex_with_sign and HEX_REGEX.fullmatch(color):
        raise NotValidColorError(color)
    with suppress(ColorError):
        return Color(color)

    # chinese name compatibility
    if color.endswith("色"):
        color = color[:-1]
    if color in COLOR_CHINESE_NAME_MAP:
        return Color(COLOR_CHINESE_NAME_MAP[color])

    # old `r g b` format compatibility
    with suppress(ColorError, ValueError):
        splitted = color.split()
        if 3 <= len(splitted) <= 4:
            r, g, b = map(int, splitted[:3])
            a = (
                (a if (a := float(splitted[3])) < 1 else a / 255)
                if len(splitted) == 4
                else None
            )
            return Color((r, g, b) if a is None else (r, g, b, a))

    raise NotValidColorError(color)


def split_multi(text: str, *seps: str) -> List[str]:
    pri, *rest = seps
    for sep in rest:
        text = text.replace(sep, pri)
    return text.split(pri)


def parse_multi_color(color: str) -> List[Color]:
    if not color:
        return []
    color_strs = [x.strip() for x in split_multi(color, ";", "；")]
    return [parse_color(color_str) for color_str in color_strs]


def trans_pydantic_rgba(color: PyDanticColorTuple) -> RGBAColorTuple:
    if len(color) == 4:
        return (*color[:3], int(color[3] * 255))
    return (*color, 255)


def reverse_color(rgb: RGBColorTuple) -> RGBColorTuple:
    if all(abs(x - 128) < 16 for x in rgb):
        return (0, 0, 0)
    return cast(RGBColorTuple, tuple(255 - i for i in rgb))


def reverse_to_black_or_white(rgb: RGBColorTuple) -> RGBColorTuple:
    light = Color(rgb).as_hsl_tuple()[2]
    return (255, 255, 255) if light < 0.4375 else (0, 0, 0)


def calc_text_color(rgb: RGBColorTuple) -> RGBColorTuple:
    return (
        reverse_to_black_or_white(rgb)
        if config.color_text_black_n_white
        else reverse_color(rgb)
    )


class ColorText:
    def __init__(
        self,
        target_color: Color,
        text_color: Optional[RGBColorTuple] = None,
    ) -> None:
        self.target_color = target_color
        target_rgb_tuple = target_color.as_rgb_tuple()
        has_alpha = len(target_rgb_tuple) == 4
        sub_size = SUB_FONT_SIZE
        if has_alpha:
            sub_size = round(sub_size * SMALL_SIZE_MULTIPLIER)

        build = partial(
            Text2Image.from_text,
            fill=text_color or calc_text_color(target_rgb_tuple[:3]),
            fontname=FONT_NAME,
        )
        self.hex_text = build(target_color.as_hex(), TITLE_FONT_SIZE)
        self.rgb_text = build(target_color.as_rgb(), sub_size)
        self.hsl_text = build(target_color.as_hsl(), sub_size)
        if self.hex_text.width > (IMG_SIZE - PADDING):  # 两侧留 PADDING / 2
            self.hex_text = build(
                target_color.as_hex(),
                round(TITLE_FONT_SIZE * SMALL_SIZE_MULTIPLIER),
            )

    def draw_on_image(
        self,
        img: Image.Image,
        offset_pos: Optional[Tuple[int, int]] = None,
    ) -> None:
        gx, gy = offset_pos or (0, 0)
        gap_size = (
            IMG_SIZE
            - (PADDING * 2)
            - sum(x.height for x in (self.hex_text, self.rgb_text, self.hsl_text))
        ) // 4
        y_offset = PADDING + gap_size
        for text in (self.hex_text, self.rgb_text, self.hsl_text):
            text.draw_on_image(
                img,
                (((IMG_SIZE - text.width) // 2) + gx, y_offset + gy),
            )
            y_offset += text.height + gap_size

    def to_image(self, bg_color: Optional[ColorType] = None) -> Image.Image:
        img = Image.new(
            "RGBA",
            (IMG_SIZE, IMG_SIZE),
            bg_color or trans_pydantic_rgba(self.target_color.as_rgb_tuple()),
        )
        self.draw_on_image(img)
        return img


def make_color_stop(*colors: RGBAColorTuple) -> List[ColorStop]:
    step_len = 1 / (len(colors) * 2)
    center_steps = [
        ColorStop(step_len * ((2 * i) + 1), c) for i, c in enumerate(colors)
    ]
    return [
        ColorStop(0, colors[0]),
        *center_steps,
        ColorStop(1, colors[-1]),
    ]


def generate_solid_image(color: Color) -> BytesIO:
    if config.color_show_text:
        return BuildImage(ColorText(color).to_image()).save_png()
    return BuildImage.new(
        "RGBA",
        (IMG_SIZE, IMG_SIZE),
        trans_pydantic_rgba(color.as_rgb_tuple()),
    ).save_png()


def generate_gradient_image(*colors: Color) -> BytesIO:
    colors_rgba = tuple(trans_pydantic_rgba(x.as_rgb_tuple()) for x in colors)
    colors_len = len(colors_rgba)

    center_y = IMG_SIZE // 2
    bg_w = IMG_SIZE * colors_len
    image_size = (bg_w, IMG_SIZE)
    gradient_xy = (0, center_y, bg_w, center_y)
    bg_gradient = LinearGradient(
        gradient_xy,
        make_color_stop(*colors_rgba),
    )
    bg_gradient_img = bg_gradient.create_image(image_size).convert("RGBA")

    if config.color_show_text:
        if config.color_text_black_n_white:
            for i, x in enumerate(colors):
                ColorText(x).draw_on_image(bg_gradient_img, (i * IMG_SIZE, 0))
        else:
            text_gradient = LinearGradient(
                gradient_xy,
                make_color_stop(*((*reverse_color(x[:3]), x[3]) for x in colors_rgba)),
            )
            text_gradient_img = text_gradient.create_image(image_size).convert("RGBA")
            text_mask = Image.new("RGBA", image_size)
            for i, x in enumerate(colors):
                ColorText(x).draw_on_image(text_mask, (i * IMG_SIZE, 0))
            bg_gradient_img.paste(text_gradient_img, mask=text_mask)

    return BuildImage(bg_gradient_img).save_png()


def generate_image(*colors: Color) -> BytesIO:
    if len(colors) == 1:
        return generate_solid_image(*colors)
    return generate_gradient_image(*colors)
