from nonebot import get_driver
from pydantic import BaseModel


class ConfigModel(BaseModel):
    color_reply: bool = True
    color_show_text: bool = True
    color_show_desc: bool = True
    color_enable_on_message: bool = True
    color_on_message_priority: int = 5


config: ConfigModel = ConfigModel.parse_obj(get_driver().config)
