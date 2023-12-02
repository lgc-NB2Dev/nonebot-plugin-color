from nonebot.plugin import PluginMetadata, inherit_supported_adapters, require

require("nonebot_plugin_alconna")

from . import __main__ as __main__  # noqa: E402
from .config import ConfigModel  # noqa: E402

__version__ = "0.3.1"
__plugin_meta__ = PluginMetadata(
    name="色图生成",
    description="用于生成指定色彩图片的 NoneBot2 插件",
    usage=(
        "插件基于 `pydantic` 的 `Color` 类解析颜色，"
        "将下方支持的颜色值格式作为指令 `color` / `色图` 的参数发送即可\n"
        " \n"
        "- 颜色别名：`yellow` / `黄` / `黄色`（插件对部分中文颜色别名做了处理）\n"
        "- 十六进制（HEX）：`#ff0` / `#ff0f` / `#ffff00` / `#ffff00ff` / `0xff0` / `ff0`\n"
        "- CSS RGB / RGBA：`rgb(255, 255, 0)` / `rgba(255, 255, 255, 0.5)`\n"
        "- CSS HSL：`hsl(60, 100%, 50%)` / `hsl(60, 100%, 50%, 0.5)`\n"
        "- RGB / RGBA（空格分隔）：`255 255 0` / `255 255 0 128` / `255 255 0 0.5`（A 小于 1 时代表百分比）\n"
        " \n"
        "插件还支持渐变色，将上面支持的颜色格式使用 `;` 或 `；` 分隔即可生成渐变色图片，"
        "同样支持透明度，例：`color f00;0f0;00f`\n"
        "不！够！色！我要五彩斑斓的黑和五颜六色的白！（划掉）"
    ),
    type="application",
    homepage="https://github.com/monsterxcn/nonebot-plugin-color",
    config=ConfigModel,
    supported_adapters=inherit_supported_adapters("nonebot_plugin_alconna"),
    extra={"License": "MIT", "Author": "monsterxcn & student_2333"},
)
