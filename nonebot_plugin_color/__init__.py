from nonebot.plugin import PluginMetadata, inherit_supported_adapters, require

require("nonebot_plugin_alconna")

from . import __main__ as __main__  # noqa: E402
from .config import ConfigModel  # noqa: E402

__version__ = "0.2.0.post1"
__plugin_meta__ = PluginMetadata(
    name="色图生成",
    description="用于生成指定色彩图片的 NoneBot2 插件",
    usage=(
        "插件基于 `pydantic` 的 `Color` 类解析颜色，"
        "当发送符合其格式的消息时，Bot 将会回复你一张颜色图片\n"
        " \n"
        "也可以作为指令 `color` / `色图` 的参数来使用\n"
        " \n"
        "例子：\n"
        "- 颜色别名：`yellow` / `黄` / `黄色`（插件对中文颜色别名做了特殊处理）\n"
        "- 十六进制（HEX）：`#ff0` / `#ff0f` / `#ffff00` / `#ffff00ff` / `0xff0` / `ff0`\n"
        "- CSS RGB / RGBA：`rgb(255, 255, 0)` / `rgba(255, 255, 255, 1)`\n"
        "- CSS HSL：`hsl(60, 100%, 50%)` / `hsl(60, 100%, 50%, 1)`"
    ),
    type="application",
    homepage="https://github.com/monsterxcn/nonebot-plugin-color",
    config=ConfigModel,
    supported_adapters=inherit_supported_adapters("nonebot_plugin_alconna"),
    extra={"License": "MIT", "Author": "student_2333"},
)
