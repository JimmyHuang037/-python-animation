---
name: ide-lesson-video
description: 制作或修改 IDE 风格的 Python 分步教学视频：中文旁白与逐字输入同步开始，准确显示光标，点击运行并展示真实输出。用于复用本技能的教学动画流程，不用于普通 IDE 维护或仅生成配音。
---

# IDE 分步教学视频

默认继承本次确认的流程与样式；用户的新要求优先。

## 默认效果

每段按「旁白与逐字编辑同步开始 → 打完后停顿 1 秒 → 鼠标点击运行并显示结果 → 鼠标缓慢淡出」执行。旁白与输入之间不留间隔。

- 每字符 0.1 秒，30 fps 时为 3 帧；总时长随内容变化，不再强行压到 30 秒。
- 保留上一段代码，仅模拟本段必要编辑；段首即开始旁白和首个编辑事件，不一次性显示整段新代码。
- 默认阿里百炼 Ethan 中文男声。自带配音只对应示例文本，换内容须准备新配音。
- 深色圆角编辑器、青色强调、字符串绿色、运算符和函数蓝色、独立终端。
- 打完后 1 秒点击，结果在点击帧出现；指针淡出 1.2 秒，每段重复。
- 光标与高亮片段共用同一字体和完整前缀宽度计算，不能估算字符宽度。
- 保留上一段终端输出，运行新段时更新；不加「等待讲解完成」提示。

## 使用流程

1. 首次制作或接手项目，读 [完整开发流程](references/workflow.md)。
2. 创建新课时，读 [配置说明](references/lesson-format.md)，复制 assets/list-demo/ 后换源码、讲解文字和 WAV。
3. 运行 scripts/render_lesson.py --lesson <课程JSON> --output <绝对MP4路径>。
4. 运行 scripts/verify_lesson.py --manifest <生成的manifest.json>，检查实际成片，并查看截图与点击动画拼图。
5. 交付到当前项目的 outputs/，使用完整本机路径的普通 Markdown 链接。此用户偏好「查看更新后的视频」链接，不自动嵌入播放器。

## 环境与真实性

- 用户要求既有 IDE 容器时，先识别容器和挂载并复用，不自行新建 worker/work 容器。
- 当前实现是 Pillow 绘图与 FFmpeg 编码，源码单独真实执行；不能称为实时 IDE 录屏。
- 源码验证支持本机 Python 或指定的已运行 Docker 容器；容器失败时不偷偷切换。
- 不保存对话、API 密钥或凭据文件。已有配音缓存不再次请求 API。
- 默认固定 1920×1080，最多 8 行代码、3 行输出；超限先拆段或调整布局，不裁切文字。
- `scripts/lesson_style.py` 的默认字体是 Windows 路径（`C:/Windows/Fonts/consola.ttf`、`msyh.ttc`）。在 WSL 或本项目 Docker 内运行必须用 `IDE_VIDEO_CODE_FONT`、`IDE_VIDEO_UI_FONT` 指向实际存在的字体；两个镜像装的是 `fonts-noto-cjk` 与 `fonts-dejavu-core`。未设置时渲染会因取不到字体失败，不会自动回退。

## 快速复现

自带三段列表源码和对应 WAV，可离线复现，无须 API 密钥。依赖 Pillow、imageio-ffmpeg、NumPy；优先复用现有 Python 环境。

下面在技能目录内执行，`<输出目录>` 换成本次任务自己的输出位置，不要写个人绝对路径。

~~~bash
python3 scripts/render_lesson.py --lesson assets/list-demo/lesson.json --output <输出目录>/list-demo.mp4
python3 scripts/verify_lesson.py --manifest <输出目录>/list-demo.manifest.json
~~~

Windows 上把 `python3` 换成实际解释器；命令语义相同。

支持 --runtime-dir 指向现有依赖目录；--preflight 检查输入并生成预览。更多命令见 workflow。

