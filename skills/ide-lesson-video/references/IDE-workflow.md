# 从开发到交付的完整流程

## 1. 找到真正的生成入口

修改已有项目时，从用户最后认可的 MP4 和实际生成它的脚本入手，不重新运行全部历史脚本。本包的有效链条是 `scripts/render_lesson.py`、`scripts/lesson_style.py`、`scripts/run_click_effect.py` 和 `scripts/verify_lesson.py`。

用户要求复用 IDE 容器时先做只读检查：

~~~bash
docker ps -a --format "table {{.Names}}\t{{.Status}}\t{{.Image}}"
docker inspect --format '{{json .Mounts}}' <已确认的IDE容器名>
docker exec <已确认的IDE容器名> python3 --version
~~~

不要打印完整容器环境变量，里面可能有凭据。确认源码的宿主机/容器路径对应关系。不要为了视频新建 worker/work 容器。已有编码容器只在已授权范围内复用；Docker 不可用时记录具体问题，不删除 socket 或擅自重建。

## 2. 分镜与真实运行

每段准备一句讲解、截至该段的完整可执行 Python 文件和本段编辑操作。先审阅再执行，尤其是附件或外部源码。例子应无交互输入，输出确定。

第一段从空编辑器输入；之后保留旧代码。`move`、`type`、`backspace` 生成逐字符状态，最终状态必须与阶段源码一致。不是把完成后的整块代码直接切换。

每段 stdout 必须来自实际运行，不手编看似合理的结果。不要把整个教程的输出在第一段提前展示。

## 3. 配音与凭据

示例采用阿里百炼 Ethan 中文男声；示例 WAV 与 lesson JSON 中 `narration` 一一对应。新文本不可复用不匹配的旧音频。

新配音可来自用户、已有缓存或用户授权的服务。调用百炼前核实当时官方文档中的模型、地区端点、Ethan 支持及参数；本包没有未经验证的实时 TTS API 封装。不要猜模型或沿用未经确认的旧接口。

凭据仅从环境变量或用户指定的本机凭据文件读取，不写入配置、脚本、日志或技能，不复述用户曾粘贴的密钥。相同文本、模型、声音和参数优先复用缓存。

用 WAV 样本数和采样率测量实际时长，不按字数猜。合成时转成 48 kHz 单声道 PCM，保留原音频不变。

## 4. 动态时间轴

默认 30 fps，每字符 0.1 秒；段首旁白与逐字编辑同步开始，二者之间无间隔。示例的每段节奏为：最后字符后等待 1 秒，显示红圈（仅对显式 `highlight`），再等待 1 秒开始气泡进入；气泡进入约 1.4 秒，完整出现后等待约 0.4 秒点击运行；结果停留 3 秒，气泡通常在段末前约 1.2 秒退出。

- `speech_start = stage_start / fps`
- `speech_end = speech_start + 实测音频长度`
- `typing_start = stage_start`，首个编辑事件与旁白同帧开始
- `key_interval = round(character_seconds × fps)`，须准确落在帧上
- `typing_end = 最后编辑事件帧`
- `result_frame = typing_end + round(after_typing × fps)`
- `stage_end = result_frame + round(result_hold × fps)`

下一段从 `stage_end` 开始；旁白必须在本段结束前播完，不能截断或跨入下一段旁白。`move` 或换行也属于编辑事件，段首恰为此类操作时保留准确光标位置。

## 5. 视觉、标注与准确光标

`lesson_style.py` 实现用户 HTML 参考的设计：Oklch 转 sRGB、深色圆角面板、文件标签、运行按钮、行号栏、语法高亮和独立终端。面板尺寸固定，代码增多时不跳布局。

气泡注释使用课程 JSON 的 `annotations`，固定在编辑器右侧近距离栏。连接线首节点按整行实际字体宽度测量，落在目标代码行末尾，不从红圈边缘起线。气泡可以没有红圈；只有用户明确要求圈出的重点才在 annotation 中加入非空 `highlight`。

气泡进入和退出都采用渐变颜色、透明度、位移、缩放和轻微模糊；连接线单独延迟收回。红圈快速出现，不做逐笔绘制。代码、颜色片段、光标和连接线都使用同一字体；x 坐标按完整前缀测量。未闭合字符串也要正确高亮；高亮只改变颜色，不改变字体和字号。

必须设置 `IDE_VIDEO_CODE_FONT` 和 `IDE_VIDEO_UI_FONT` 为当前系统中存在的字体文件。Linux 侧未设置或路径无效时脚本会直接失败，不会自动回退。不要出现等待提示或大块实现说明；保留行列位置提示。

## 6. 连续键盘音效

使用真实的连续机械键盘录音，不为每个字符单独合成声音。`typing_sound.source` 必须是 48 kHz、单声道、16-bit PCM WAV；渲染器从 `source_start_seconds` 开始，按每段打字的实际时长连续截取并混入旁白。每段打字结束即停止该段录音，下一段从后续位置继续。检查混音峰值，避免削波。

示例素材 `assets/list-demo/keyboard-continuous.wav` 来自 Freesound 的 “Mechanical Keyboard Typing (Treble Version)”，页面标注为 CC0；替换素材时保留来源和许可证记录。

## 7. 点击运行与淡出

输出前约 0.6 秒出现鼠标，缓动移向运行按钮；点击帧严格等于 `result_frame`。按钮短暂变暗并出现青色圆环；指针停留后用约 1.2 秒淡出，每段重复。

点击热点要落在按钮内部，淡出后无残留。渲染缓存键必须包含点击相位和标注相位，否则鼠标或气泡动画会卡住。打字插入点和鼠标指针是不同对象，不可混用坐标。

## 8. 编码与验收

RGB 帧通过 stdin 送入 FFmpeg，H.264 / yuv420p / CRF 18 / AAC / faststart。先生成 pending MP4，完整解码成功后复制到 `<输出目录>`，不覆盖用户已确认的成品。

检查实际编码视频，不能只读脚本中的常量：

- 实测帧数、时长、分辨率和全片可解码。
- 旁白与首个编辑事件同帧开始，启动偏移为 0；字符间隔、等待和点击时点正确。
- 每个编辑事件及所有打字帧的光标位置。
- 仅在显式 `highlight` 时检查红圈；气泡连接线首节点在目标行末尾。
- 输出与点击同帧、点击在按钮内、每次指针都完全淡出。
- 阶段源码与最终编辑状态一致，stdout 来自真实执行。
- 抽看同步开始帧、打字中、红圈/气泡、点击、结果和淡出；没有裁切或遗留提示。
- 连续键盘音效只覆盖打字阶段，`typing-clicks.wav` 非空，旁白不能被截断或跨段。

RGB→YUV420 编码会造成约 1–3 色阶差异，尤其在暗背景。不能仅因这种差异判为残影，也不能盲目放宽阈值掩盖问题。验收脚本同时检查原始图层完全消失、编码画面接近基准，并输出拼图。

## 9. 复现与交付

在目标环境安装锁定依赖，并替换占位符路径：

~~~bash
python3 -m pip install -r scripts/requirements.txt
export IDE_VIDEO_CODE_FONT='<代码字体文件>'
export IDE_VIDEO_UI_FONT='<界面字体文件>'
python3 scripts/render_lesson.py \
  --lesson assets/list-demo/lesson.json \
  --output '<输出目录>/list-demo.mp4'
python3 scripts/verify_lesson.py \
  --manifest '<输出目录>/list-demo.manifest.json'
~~~

不要复制整套环境或凭据。视频、音频和大图片逐个检查，单文件不得超过 100 MB；未执行的验证必须如实标记。
