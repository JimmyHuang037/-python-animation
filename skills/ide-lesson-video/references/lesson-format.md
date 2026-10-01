# 课程 JSON 与修改位置

路径相对 lesson.json 所在目录解析。新课程先复制 assets/list-demo/，不要修改技能的基准示例。

| 字段 | 说明 |
|---|---|
| schema_version | 当前 1 |
| display_file | 画面显示的短文件名，如 vehicle.py |
| lesson_label / voice_label | 页脚课程与配音标签 |
| timing.character_seconds | 默认 0.1，须是 1/30 秒的整数倍 |
| timing.after_typing / result_hold | 默认 1 / 2 秒，需容纳点击进入与淡出 |
| execution.mode | local 或 docker，不隐式切换 |
| execution.container / python | Docker 模式的已运行容器及解释器，解释器默认 python3 |
| execution.timeout_seconds | 默认 15 秒 |
| stages[].source / audio | 本段完整 Python 文件 / 对应 WAV |
| stages[].narration | 讲解文本，供准备音频与人工校对 |
| stages[].edits | 逐步编辑指令 |

旁白与首个编辑事件固定在每段起点同步开始，启动间隔为 0。旧字段 timing.voice_lead / timing.after_voice 已停用，应删除；为方便迁移也接受值 0，非零值会明确报错，避免静默沿用旧时序。旁白须在本段结束前播完，否则缩短旁白、拆段或增加 result_hold。

## 编辑指令

row/col 都从 0 开始，画面 Ln/Col 自动加 1。坐标针对当前文档状态。

~~~json
[
  {"op":"move", "row":1, "col":"end"},
  {"op":"type", "text":"\nvehicle = vehicle1 + vehicle2"},
  {"op":"move", "row":"last", "col":"end"},
  {"op":"type", "text":"\nprint(vehicle)"}
]
~~~

- move：移动插入点；row 可为 last，col 可为 end。
- type：按字符输入 text，包括换行。
- backspace：从插入点删除 count 个字符，可跨行；默认 1。
- 首段省略 edits 时输入源文件全文。
- 后续省略 edits 时，仅在新源码以旧源码为前缀时自动追加，否则报错，要求显式 edits，不能突然替换整块代码。
- 最终状态必须匹配源码；只忽略文件末尾换行。

源码用空格缩进；当前字体逻辑面向本例 ASCII Python 代码，宽字符或复杂字形需额外视觉验收。默认最多 8 行代码、3 行输出，单行不能越界。出错不应伪造输出，应拆段或调整布局。

修改映射：内容、音频、速度、等待时间改 JSON；布局/颜色/字体改 lesson_style.py；鼠标外观、路径和淡出改 run_click_effect.py；时间轴与执行合成改 render_lesson.py；验收改 verify_lesson.py。

--preflight 会执行已审阅源码、测量音频、检查编辑和布局并生成预览，但不编码；它不是纯静态检查。

