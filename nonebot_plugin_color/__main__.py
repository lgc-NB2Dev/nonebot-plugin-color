from contextlib import suppress
from typing import List, Type, Union

from nonebot import logger, on_command, on_message
from nonebot.adapters import Message as BaseMessage
from nonebot.matcher import Matcher
from nonebot.params import Depends, EventMessage
from nonebot.params import _command_arg as get_command_arg
from nonebot.typing import T_State
from nonebot_plugin_alconna.uniseg import Image, Segment, Text, UniMessage
from pydantic.color import Color
from pydantic.errors import ColorError

from .config import config
from .const import COLOR_CHINESE_NAME_MAP
from .data_source import generate_image

KEY_COLOR = "color"


class NotValidColorError(ValueError):
    def __init__(self, color: str) -> None:
        self.color = color


def parse_color(color: str) -> Color:
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


async def rule_color_msg(state: T_State, msg: BaseMessage = EventMessage()) -> bool:
    with suppress(NotValidColorError):
        if color := parse_multi_color(msg.extract_plain_text().strip()):
            state[KEY_COLOR] = color
            return True
    return False


async def dep_color(state: T_State) -> Union[List[Color], NotValidColorError]:
    if KEY_COLOR in state and (color := state[KEY_COLOR]):
        return color

    arg = get_command_arg(state).extract_plain_text().strip()
    try:
        return parse_multi_color(arg)
    except NotValidColorError as e:
        return e


async def handle_color_error(
    matcher: Matcher,
    err: NotValidColorError = Depends(dep_color),
):
    await matcher.finish(f"奇怪的颜色 `{err.color}` 增加了呢！")


async def handle_color(
    matcher: Matcher,
    colors: List[Color] = Depends(dep_color),
):
    if not colors:
        await matcher.finish("色色，我要色色！色色在哪里？")

    try:
        image = generate_image(*colors)
    except Exception as e:
        logger.exception("Error occurred while generating image")
        await matcher.finish(f"不许色色！\n{type(e).__name__}: {e}")

    msg_list: List[Segment] = [Image(raw=image)]
    if config.color_show_desc:
        image_desc = (
            f"HEX: {'; '.join(x.as_hex() for x in colors)}\n"
            f"RGB: {'; '.join(x.as_rgb() for x in colors)}\n"
            f"HSL: {'; '.join(x.as_hsl() for x in colors)}"
        )
        msg_list.append(Text(image_desc))

    await UniMessage(msg_list).send(reply_to=config.color_reply)
    await matcher.finish()


def append_color_handlers(matcher: Type[Matcher]):
    matcher.append_handler(handle_color_error)
    matcher.append_handler(handle_color)


cmd_color = on_command("color", aliases={"色图"})
append_color_handlers(cmd_color)

if config.color_enable_on_message:
    msg_color = on_message(
        rule=rule_color_msg,
        priority=config.color_on_message_priority,
    )
    append_color_handlers(msg_color)
