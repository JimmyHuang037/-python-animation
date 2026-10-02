# 课程 JSON 与标注格式

所有路径相对 `lesson.json` 所在目录解析。新课程先复制 `assets/list-demo/`，再替换源码、旁白、连续键盘录音和注释。

| 字段 | 说明 |
|---|---|
| `schema_version` | 当前为 `1` |
| `display_file` | 画面显示的短文件名，如 `vehicle.py` |
| `lesson_label` / `voice_label` | 页脚课程与配音标签 |
| `timing.character_seconds` | 默认 `0.1`，必须是 1/30 秒的整数倍 |
| `timing.after_typing` / `result_hold` | 默认与示例均为 `3.8` / `3` 秒；有标注时等待至少 `3.8` 秒，无标注时至少 `0.6` 秒；结果停留必须超过 `1.4` 秒以完成鼠标淡出 |
| `typing_sound.enabled` / `volume` | 连续键盘录音开关和音量 |
| `typing_sound.source` | 48 kHz、单声道、16-bit PCM WAV，路径相对 lesson.json |
| `typing_sound.source_start_seconds` | 从连续录音的哪个位置开始取样 |
| `execution.mode` | `local` 或 `docker`，不会隐式切换 |
| `execution.container` / `python` | Docker 模式的已运行容器及解释器；解释器默认 `python3` |
| `execution.timeout_seconds` | 默认 15 秒 |
| `stages[].source` / `audio` | 本段完整 Python 文件 / 对应 WAV |
| `stages[].narration` | 讲解文本，供准备音频和人工校对 |
| `stages[].edits` | 逐步编辑指令 |
| `stages[].annotations` | 气泡注释及可选红色重点圈选 |

旁白与首个编辑事件固定在每段起点同步开始，启动偏移为 0。旧字段 `timing.voice_lead` / `timing.after_voice` 已停用，应删除；迁移时只接受值 0，非零值会报错。旁白必须在本段结束前播完。

## 标注

气泡注释始终指向一行代码，放在编辑器右侧近距离栏。连接线的首节点落在整行代码末尾，与红圈范围无关。`row`、`start_col`、`end_col` 从 0 开始。

需要红圈时，显式提供非空 `highlight`：

~~~json
{
  "text": "加号生成一个新列表",
  "highlight": {"row": 2, "start_col": 0, "end_col": 30}
}
~~~

只需要气泡时省略 `highlight`，并在标注根部提供 `row`：

~~~json
{
  "text": "这里把新列表写回变量",
  "row": 2
}
~~~

没有明确重点时不要自动补 `highlight`。目标行尚未输入时，标注会等该行出现后再显示。

## 编辑指令

`row` / `col` 都从 0 开始，画面 Ln/Col 自动加 1。坐标针对当前文档状态。

~~~json
[
  {"op":"move", "row":1, "col":"end"},
  {"op":"type", "text":"\nvehicle = vehicle1 + vehicle2"},
  {"op":"move", "row":"last", "col":"end"},
  {"op":"type", "text":"\nprint(vehicle)"}
]
~~~

- `move`：移动插入点；`row` 可为 `last`，`col` 可为 `end`。
- `type`：按字符输入 `text`，包括换行。
- `backspace`：从插入点删除 `count` 个字符，可跨行；默认 1。
- 首段省略 `edits` 时输入源文件全文。
- 后续省略 `edits` 时，仅在新源码以旧源码为前缀时自动追加，否则报错。
- 最终状态必须匹配源码，只忽略文件末尾换行。

源码使用空格缩进；默认最多 8 行代码、3 行输出，单行不能越界。宽字符或复杂字形需要额外视觉验收。出错时不要伪造输出，应拆段或调整布局。

修改映射：内容、音频、速度和等待时间改 JSON；布局、颜色、气泡进出和连接线改 `scripts/lesson_style.py`；鼠标改 `scripts/run_click_effect.py`；时间轴、真实执行和连续键盘音频截取改 `scripts/render_lesson.py`；验收改 `scripts/verify_lesson.py`。

`--preflight` 会执行已审阅源码、测量音频、检查编辑和布局并生成预览，但不编码；它不是纯静态检查。
