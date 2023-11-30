from contextlib import suppress
from typing import Optional

from nonebot import logger, on_command, on_message
from nonebot.adapters import Message as BaseMessage
from nonebot.matcher import Matcher
from nonebot.params import Depends, EventMessage
from nonebot.params import _command_arg as get_command_arg
from nonebot.typing import T_State
from nonebot_plugin_alconna.uniseg import Image, UniMessage
from pydantic.color import Color
from pydantic.errors import ColorError

from .const import COLOR_CHINESE_NAME_MAP
from .data_source import generate_image

KEY_COLOR = "color"
IMG_SIZE = 200


def parse_color(color: str) -> Optional[Color]:
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

    return None


async def rule_color_msg(state: T_State, msg: BaseMessage = EventMessage()) -> bool:
    if color := parse_color(msg.extract_plain_text().strip()):
        state[KEY_COLOR] = color
        return True
    return False


async def dep_color(state: T_State) -> Optional[Color]:
    if KEY_COLOR in state and (color := state[KEY_COLOR]):
        return color

    with suppress(KeyError):
        arg = get_command_arg(state).extract_plain_text().strip()
        if color := parse_color(arg):
            return color

    return None


cmd_color = on_command("color", aliases={"色图"})
msg_color = on_message(rule=rule_color_msg, priority=5)


@cmd_color.handle()
@msg_color.handle()
async def handle_color(
    matcher: Matcher,
    color: Optional[Color] = Depends(dep_color, use_cache=False),
):
    if not color:
        await matcher.finish("奇怪的颜色增加了呢！")

    try:
        image = await generate_image(color)
    except Exception as e:
        logger.exception("Error occurred while generating image")
        await matcher.finish(f"不许色色！\n{type(e).__name__}: {e}")

    await matcher.finish(
        await UniMessage(Image(raw=image)).export(),
    )
