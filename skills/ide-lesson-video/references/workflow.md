# 从开发到交付的完整流程

## 1. 找到真正的生成入口

修改已有项目时，从用户最后认可的 MP4 和实际生成它的脚本入手，不重新运行全部历史脚本。本项目的有效链条是 render_typing.py → lesson_style.py → run_click_effect.py。本包将其整理为 scripts/render_lesson.py 和两个样式模块。

用户要求复用 IDE 容器时先做只读检查：

~~~bash
docker ps -a --format "table {{.Names}}\t{{.Status}}\t{{.Image}}"
docker inspect --format '{{json .Mounts}}' <已确认的IDE容器名>
docker exec <已确认的IDE容器名> python3 --version
~~~

不要打印完整容器环境变量，里面可能有凭据。确认源码的宿主机/容器路径对应关系。不要为了视频新建 worker。已有编码容器只在已授权范围内复用。Docker 不可用时记录具体问题，不删除 socket 或擅自重建；画面渲染本身不依赖 Docker。执行环境变更应明确说明。

## 2. 分镜与真实运行

每段准备一句讲解、截至该段的完整可执行 Python 文件和本段编辑操作。先审阅再执行，尤其是附件或外部源码。例子应无交互输入，输出确定；本包示例仅操作列表。

第一段从空编辑器输入；之后保留旧代码。move/type/backspace 生成逐字符状态，最终状态必须与阶段源码一致。不是把完成后的三块代码直接切换。

每段 stdout 必须来自实际运行，不手编看似合理的结果。不要把整个教程的输出在第一段提前展示。

## 3. 配音与凭据

本案例采用阿里百炼 Ethan 中文男声；示例 WAV 与 lesson.json 中 narration 一一对应。新文本不可复用不匹配的旧音频。

新配音可来自用户、已有缓存或用户授权的服务。调用百炼前核实当时官方文档中的模型、地区端点、Ethan 支持及参数；本包没有未经验证的实时 TTS API 封装。不要猜模型或沿用未经确认的旧接口。

凭据仅从环境变量或用户指定的本机凭据文件读取，不写入配置、脚本、日志或技能，不复述用户曾粘贴的密钥。相同文本、模型、声音和参数优先复用缓存。

用 WAV 样本数/采样率测量实际时长，不按字数猜。合成时转成 48 kHz 单声道 PCM，保留原音频不变。

## 4. 动态时间轴

默认：30 fps，每字符 0.1 秒；段首旁白与逐字编辑同步开始，二者之间无间隔；最后字符后停 1 秒，结果保留 2 秒。

- speech_start = stage_start / fps
- speech_end = speech_start + 实测音频长度
- typing_start = stage_start（帧），首个编辑事件与旁白同帧开始
- key_interval = round(character_seconds × fps)，须准确落在帧上
- typing_end = 最后编辑事件帧
- result_frame = typing_end + round(after_typing × fps)
- stage_end = result_frame + round(result_hold × fps)

下一段从 stage_end 开始；旁白必须在本段结束前播完，否则缩短旁白、拆段或增加 result_hold，不能截断或覆盖下一段旁白。当前同步版示例为 810 帧、27 秒，这只是示例结果，不是新课程的硬指标。move 或换行也属于编辑事件，段首恰为此类操作时保留其准确光标位置。

## 5. 视觉与准确光标

lesson_style.py 实现用户 HTML 的设计：Oklch 转 sRGB、深色圆角面板、文件标签、运行按钮、行号栏、语法高亮和独立终端。原 HTML 在 assets/style-reference.html。面板尺寸固定，代码增多时不跳布局。

代码、颜色片段、光标都使用同一字体；x 坐标按整行前缀测量。固定字体基线，防止输入不同字形时上下抖动。未闭合字符串也要正确高亮；高亮只改变颜色，不改变字体/字号。

Windows 默认 Consolas + 微软雅黑；跨机器可设置 IDE_VIDEO_CODE_FONT 和 IDE_VIDEO_UI_FONT。`lesson_style.py` 里这两个默认值写的是 Windows 字体路径，在 WSL 或本项目 Docker 内不存在，**必须显式设置这两个环境变量**，否则渲染取不到字体就失败，脚本不会自动回退到系统字体。不要替换成不能显示中文的字体。不要出现等待提示或大块实现说明；保留行列位置提示。

## 6. 点击运行与淡出

输出前 0.6 秒出现鼠标，缓动移向运行按钮；点击帧严格等于 result_frame。按钮短暂变暗，出现青色圆环；指针停 0.2 秒后用 1.2 秒淡出，每段重复。

点击热点要落在按钮内部，淡出后无残留。渲染缓存键必须包含动画相位，否则指针/淡出会卡住。打字插入点和鼠标指针是不同对象，不可混用坐标。

## 7. 编码与验收

RGB 帧通过 stdin 送入 FFmpeg，H.264 / yuv420p / CRF 18 / AAC / faststart。先生成 pending MP4，完整解码成功后复制到 outputs，不覆盖用户已确认的成品。

检查实际编码视频，不能只读脚本中的常量：

- 实测帧数、时长、分辨率和全片可解码。
- 旁白与首个编辑事件在段首同帧开始，启动偏移为 0；字符间隔、1 秒等待和点击时点正确。
- 每个编辑事件及所有打字帧的光标位置。
- 输出与点击同帧、点击在按钮内、每次指针都完全淡出。
- 阶段源码与最终编辑状态一致，stdout 来自真实执行。
- 抽看同步开始帧、打字中、点击、结果、淡出；没有裁切或遗留提示。
- WAV 在各段起点完整插入，不要求打字期间静音；旁白不能被截断或跨入下一段。
- 仅修改视觉时音频轨与时间轴应不变。

RGB→YUV420 编码会造成约 1–3 色阶差异，尤其在暗背景。不能仅因这种差异判为残影，也不能盲目放宽阈值掩盖问题。验收脚本同时检查原始图层完全消失、编码画面接近基准，并输出拼图。

## 8. 本机复现与交付

优先使用已安装的环境。下面在技能目录内执行，`<输出目录>` 换成本次任务自己的输出位置；不要写入任何个人绝对路径。

~~~bash
cd <仓库>/skills/ide-lesson-video
python3 scripts/render_lesson.py \
  --lesson assets/list-demo/lesson.json \
  --output <输出目录>/list-demo.mp4
python3 scripts/verify_lesson.py \
  --manifest <输出目录>/list-demo.manifest.json
~~~

`--lesson`、`--output`、`--manifest` 为必填；`--runtime-dir` 可选，指向已装好依赖的目录，省略时用当前解释器的环境。`--preflight` 只检查输入并生成预览。

原始验证是在 Windows 上用一个 Codex 私有 Python 运行时和该次会话自己的 runtime 目录完成的，那些路径只对当时那台机器有效，**不作为团队前提**。本仓库内改用各成员自己的 WSL 环境，或 `./docker/course` 的镜像。

现成镜像都不能直接跑本技能，需按 `scripts/requirements.txt` 补装依赖：

- `docker/Dockerfile.studio`（基于 `mcr.microsoft.com/playwright:v1.58.2-noble`）已有 `python3`、`python3-numpy`、`ffmpeg`、`fonts-noto-cjk`、`fonts-dejavu-core`，以及装了 `edge-tts==7.2.8` 的 venv；缺 Pillow 与 imageio-ffmpeg。
- `docker/Dockerfile.ide`（基于 `python:3.12-slim-bookworm`）只有 `curl`、`ca-certificates`、`git` 和上述两个字体包；**没有 ffmpeg，也没有 numpy**。

必要时在任务自己的环境安装 scripts/requirements.txt；不要复制整套环境或凭据。成品放在本次任务约定的输出位置，并给团队成员实际可取得的地址与哈希，个人本机路径不作为共享交付地址。简短回复并给普通 Markdown 视频链接，不自动嵌入视频。


## 同步版验证记录（2026-09-30，当前默认）

- 技能格式校验、UI 元数据及 Python 编译检查通过。
- 使用包内源码与缓存 WAV 完整复现：810 帧、27 秒、每字符 0.1 秒。
- 三段旁白与编辑起点均为 0 偏移，分别从 0、13、20.6 秒开始；音频完整且不跨段。
- 实际编码视频核对 543 个打字帧、183 个编辑落点、3 次按钮点击、同步输出及完整淡出。
- 音频轨与用户认可的 list-concat-ali-styled-sync.mp4 完全一致。
- 本次验证文件位于项目 work/skill-sync-smoke/，用户认可成品未覆盖。

## 历史打包验证记录（2026-09-30，旧版先讲解后输入）

- 官方 quick_validate 校验通过；技能 UI 元数据已校验。
- 使用包内源码与缓存 WAV 完整复现：1256 帧、41.867 秒、每字符 0.1 秒。
- 实际编码视频核对 543 个打字帧、183 个编辑落点、3 次按钮点击及完整淡出。
- 复现视频的音频轨与当时确认的旧版成品一致。
- 两段课程、不同文件名、每字符 0.2 秒的独立配置通过 preflight。
- 技能脚本不依赖旧项目目录；包内无 API 密钥。
