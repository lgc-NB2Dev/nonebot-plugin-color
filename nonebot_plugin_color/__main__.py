from contextlib import suppress
from typing import List, Type, Union, cast

from nonebot import logger, on_command, on_message
from nonebot.adapters import Message as BaseMessage
from nonebot.matcher import Matcher
from nonebot.params import Depends, EventMessage, _command_arg as get_command_arg
from nonebot.typing import T_State
from nonebot_plugin_alconna.uniseg import Image, Segment, Text, UniMessage

from .config import config
from .data_source import Color, NotValidColorError, generate_image, parse_multi_color

KEY_COLOR = "color"


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
        return cast(List[Color], parse_multi_color(arg))
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
