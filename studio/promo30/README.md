# Python promo30

本工程保存 2026-09-28 的30秒宣传样片及声音变体，不是全课程的固定视觉或音色规范。四位成员在各自 WSL2 仓库根目录使用[Docker 工作台](../../docker/README.md)的 `./docker/course animation` 制作原音乐样片；该入口尚不覆盖下面的 Qwen/Edge TTS 全流程。下面保留可选本机原生复现命令，按任务范围准备依赖、音轨与凭据，不要求文档任务执行制作。

## Qwen3-TTS API 试听版

已产出 [Qwen 晨煦男声版](../../build/promo30/python-course-promo-30s-qwen-ethan.mp4)。使用 `qwen3-tts-instruct-flash-2026-01-26`／`Ethan`，八段口播包含“一站式解决！”。该画面改为第 5–7 秒，声音从第 5.4 秒开始；学分目标画面改为第 7–10 秒，其余主要时点保留，总长 30 秒。Motion Canvas 已重新渲染，音乐提示音同步调整。

可选原生复现（本目录；先完成本文件列出的 Node/Python/FFmpeg/字体/Chromium 依赖准备；API Key 从环境变量读取，或用 `--key-file` 指向项目外的密钥文件，不在代码中填写密钥）：

```bash
python3 qwen_voiceover.py --voice Ethan
python3 qwen_assemble.py --prepare
TIMING_PATH=../../build/promo30/qwen-ethan/timing.json MUSIC_PATH=../../build/promo30/qwen-ethan/music.wav python3 soundtrack.py
npm run serve -- --port 9031 --strictPort
# 另一个终端，同目录
TIMING_PATH=../../build/promo30/qwen-ethan/timing.json FRAMES_DIR=../../build/promo30/qwen-ethan/frames RENDER_URL=http://127.0.0.1:9031/render.html node render.mjs
python3 qwen_assemble.py
```

合成脚本缓存相同请求的音频，重复运行可复用，不保存凭据或临时下载 URL。官方接口与音色依据：[API](https://help.aliyun.com/zh/model-studio/qwen-tts-api)、[音色](https://help.aliyun.com/zh/model-studio/qwen-tts-voice-list)。2026-09-28 八次 API 返回共 196 计费字符；不能直接用 Python 字符串长度 110 代替计费字符。当时按 0.8 元／万字符估算约 0.01568 元，未核查账号账单或免费额度；该估算不是后续任务的现价承诺。

音频、字幕、时间表、API 用量和验证记录在仓库根目录的 `build/promo30/qwen-ethan/`。当前 `.gitignore` 不整体忽略 `build/promo30/`；是否已纳入 Git、是否可供其他成员取得须核对实际文件。团队交接提供可访问地址和哈希；复用本次声音需取得原音频，重新调用的时长可能变化。`qwen_assemble.py --prepare` 会检查新声音是否仍能放入时间窗，超出即报错，不能跳过后直接合成。字幕为独立 SRT，未烧录到画面。未完成真人听审。

## 原音乐与 Edge TTS 版本

本节保留早期原音乐和七句 Edge TTS 版本的复现记录，包含5–6秒音乐留白。后续用户已明确“一站式解决”必须朗读；上方 Qwen 版本按新要求重新对齐。复现旧版本不代表它满足后续声音要求，新交付按当前任务选择口播与时间轴。

30 秒全 Motion Canvas 宣传动画。没有 Python 编辑器录屏或逐字代码。主要依据为 Motion Canvas 官方文档与官方 examples，不依赖低星社区 skill 插件。

- `src/promo.tsx`：完整画面与时间轴，逻辑尺寸 1280×720。
- `src/render.ts`、`render.mjs`：调用 Motion Canvas Renderer，1.5 倍输出 1920×1080、30 fps、900 帧。
- `soundtrack.py`：原创合成音乐，无配音。
- 分镜：`../../course/lessons/promo30/storyboard.md`。
- 成片：`../../build/promo30/python-course-promo-30s.mp4`。

AI 配音方案见 [GitHub 研究](../../docs/research/promo30-tts-2026-09-28.md)。该次宣传片按用户中文男声要求制作[云希版](../../build/promo30/python-course-promo-30s-tts-male.mp4)，另有上面的 Qwen 同稿试听版本；全课程音色尚未定稿。[晓晓女声版](../../build/promo30/python-course-promo-30s-tts.mp4)及原音乐版保留。

可选原生配音复现（本目录，需要 uv、FFmpeg 和原音乐版视频；运行下面命令需联网调用 Edge TTS）：

```bash
uv venv .venv-tts
uv pip install --python .venv-tts/bin/python -r requirements-tts.txt
.venv-tts/bin/python voiceover.py
```

`voiceover.py` 默认生成云希男声，保存七句配音及时间表；逐句测量，语速在原速至 +30% 内调整，超出时间窗则报错，不截断。5–6 秒保留音乐。人声归一化后触发音乐侧链压缩，复用原片视频流输出配音版。男声音频、独立 SRT 字幕及检查记录位于 `../../build/promo30/tts-male/`，女声记录位于 `../../build/promo30/tts/`；字幕未烧录到画面。在线服务再次生成的声音与时长可能变化。

这两份历史样片均记录：30 秒、900 帧、完整解码通过、所有口播落入时间窗；具体响度见各自 verification.json。女声版另校验视频流哈希未变；两版均尚未完成真人听审，不代表其他成员电脑已经复现通过。

可选原生原音乐版复现（在本目录，先准备下一段所列依赖）：

```bash
npm ci
npm run serve
# 另一个终端
npx tsc --noEmit
node render.mjs
python3 soundtrack.py
ffmpeg -y -framerate 30 -i ../../build/promo30/frames/%05d.png -i ../../build/promo30/music-original.wav -frames:v 900 -t 30 -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart ../../build/promo30/python-course-promo-30s.mp4
```

需要 Node.js、FFmpeg、Python + NumPy，以及 Playwright Chromium。render.mjs 默认使用 Playwright 匹配的 Chromium，首次本地安装可执行 `npx playwright install chromium`；也可用 CHROMIUM_PATH 覆盖。字体使用 Noto Sans CJK SC。本地渲染服务默认绑定 127.0.0.1:9030；Docker 配置内部监听 0.0.0.0，宿主端口仍只绑定回环地址。

Linux Docker 启动、按需渲染与远程浏览器访问见 [Docker 入口](../../docker/README.md)。


依赖版本锁在 package-lock.json。2026-09-28 安装审计报告有 3 个 moderate、2 个 high 上游问题；此工具用于本地制作，TTS 可按需联网，未部署为公网服务。该历史报告不代表当前依赖重新审计结果；本次文档修订未替换动画引擎或升级依赖。
