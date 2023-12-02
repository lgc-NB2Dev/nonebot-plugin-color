<!-- markdownlint-disable MD031 MD033 MD036 MD041 -->

<div align="center">

<a href="https://v2.nonebot.dev/store">
  <img src="https://raw.githubusercontent.com/A-kirami/nonebot-plugin-template/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo">
</a>

<p>
  <img src="https://raw.githubusercontent.com/A-kirami/nonebot-plugin-template/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText">
</p>

# NoneBot-Plugin-Color

_✨ 用于生成指定色彩图片的 NoneBot2 插件 ✨_

<img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="python">
<a href="https://pdm.fming.dev">
  <img src="https://img.shields.io/badge/pdm-managed-blueviolet" alt="pdm-managed">
</a>

<br />

<a href="./LICENSE">
  <img src="https://img.shields.io/github/license/monsterxcn/nonebot-plugin-color.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-color">
  <img src="https://img.shields.io/pypi/v/nonebot-plugin-color.svg" alt="pypi">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-color">
  <img src="https://img.shields.io/pypi/dm/nonebot-plugin-color" alt="pypi download">
</a>

</div>

## 💿 安装

以下提到的方法 任选**其一** 即可

<details open>
<summary>[推荐] 使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

```bash
nb plugin install nonebot-plugin-color
```

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>pip</summary>

```bash
pip install nonebot-plugin-color
```

</details>
<details>
<summary>pdm</summary>

```bash
pdm add nonebot-plugin-color
```

</details>
<details>
<summary>poetry</summary>

```bash
poetry add nonebot-plugin-color
```

</details>
<details>
<summary>conda</summary>

```bash
conda install nonebot-plugin-color
```

</details>

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分的 `plugins` 项里追加写入

```toml
[tool.nonebot]
plugins = [
    # ...
    "nonebot_plugin_color"
]
```

</details>

## ⚙️ 配置

在 NoneBot2 项目的 `.env` 文件中添加下表中的必填配置

|           配置项            | 必填 | 默认值 |                      说明                      |
| :-------------------------: | :--: | :----: | :--------------------------------------------: |
|        `COLOR_REPLY`        |  否  | `True` |                是否回复用户消息                |
|      `COLOR_SHOW_DESC`      |  否  | `True` | 是否在图片下方追加文字形式的颜色值便于复制使用 |
|  `COLOR_ENABLE_ON_MESSAGE`  |  否  | `True` |          是否响应符合格式的非指令消息          |
| `COLOR_ON_MESSAGE_PRIORITY` |  否  |  `5`   |              非指令消息响应优先级              |

## 🎉 使用

插件基于 `pydantic` 的 `Color` 类解析颜色，将下方支持的颜色值格式作为指令 `color` / `色图` 的参数发送即可

- 颜色别名：`yellow` / `黄` / `黄色`（插件对部分中文颜色别名做了处理，支持的名称列表见 [const.py](./nonebot_plugin_color/const.py)）
- 十六进制（HEX）：`#ff0` / `#ff0f` / `#ffff00` / `#ffff00ff` / `0xff0` / `ff0`
- CSS RGB / RGBA：`rgb(255, 255, 0)` / `rgba(255, 255, 255, 0.5)`
- CSS HSL：`hsl(60, 100%, 50%)` / `hsl(60, 100%, 50%, 0.5)`
- RGB / RGBA（空格分隔）：`255 255 0` / `255 255 0 128` / `255 255 0 0.5`（A 小于 1 时代表百分比）

插件还支持渐变色，将上面支持的颜色格式使用 `;` 或 `；` 分隔即可生成渐变色图片，同样支持透明度，例：`color f00;0f0;00f`  
~~不！够！色！我要五彩斑斓的黑和五颜六色的白！~~

<details>
<summary><i>哎哟这个色啊！好色！</i></summary>

![色图来咯](https://raw.githubusercontent.com/lgc-NB2Dev/readme/main/color/screenshot.png)  
![色图又来咯](https://raw.githubusercontent.com/lgc-NB2Dev/readme/main/color/screenshot2.png)

</details>

## 📞 联系

QQ：3076823485  
Telegram：[@lgc2333](https://t.me/lgc2333)  
吹水群：[1105946125](https://jq.qq.com/?_wv=1027&k=Z3n1MpEp)  
邮箱：<lgc2333@126.com>

## 💡 鸣谢

- [@nonebot/nonebot2](https://github.com/nonebot/nonebot2/)
- [@nonebot/plugin-alconna](https://github.com/nonebot/plugin-alconna)
- [@Mrs4s/go-cqhttp](https://github.com/Mrs4s/go-cqhttp)

## 💰 赞助

感谢大家的赞助！你们的赞助将是我继续创作的动力！

- [爱发电](https://afdian.net/@lgc2333)
- <details>
    <summary>赞助二维码（点击展开）</summary>

  ![讨饭](https://raw.githubusercontent.com/lgc2333/ShigureBotMenu/master/src/imgs/sponsor.png)

  </details>

## 📝 更新日志

### 0.3.0

- 支持了渐变色（[#1](https://github.com/lgc-NB2Dev/nonebot-plugin-color/issues/1)）
- 添加了一些配置项：
  - `COLOR_REPLY`
  - `COLOR_SHOW_DESC`
  - `COLOR_ENABLE_ON_MESSAGE`
  - `COLOR_ON_MESSAGE_PRIORITY`

### 0.2.0

- 重构项目
