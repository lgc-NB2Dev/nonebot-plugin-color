from typing import List

from nonebot import get_plugin_config
from pydantic import BaseModel, Field


class ConfigModel(BaseModel):
    color_font_families: List[str] = Field(
        default_factory=lambda: [
            "HarmonyOS Sans SC",
            "HarmonyOS Sans",
            "Source Han Sans SC",
            "Source Han Sans",
            "Noto Sans SC",
            "Noto Sans CJK SC",
            "Segoe UI",
            "Microsoft YaHei",
        ],
    )
    color_reply: bool = True
    color_show_text: bool = True
    color_show_desc: bool = True
    color_enable_on_message: bool = True
    color_on_message_priority: int = 5
    color_hex_with_sign: bool = True
    color_text_black_n_white: bool = False


config = get_plugin_config(ConfigModel)
