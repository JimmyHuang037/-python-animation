# Python promo30

30 秒全 Motion Canvas 宣传动画。没有 Python 编辑器录屏或逐字代码。主要依据为 Motion Canvas 官方文档与官方 examples，不依赖低星社区 skill 插件。

- `src/promo.tsx`：完整画面与时间轴，逻辑尺寸 1280×720。
- `src/render.ts`、`render.mjs`：调用 Motion Canvas Renderer，1.5 倍输出 1920×1080、30 fps、900 帧。
- `soundtrack.py`：原创合成音乐，无配音。
- 分镜：`../../course/lessons/promo30/storyboard.md`。
- 成片：`../../build/promo30/python-course-promo-30s.mp4`。

AI 配音方案见 [GitHub 研究](../../docs/research/promo30-tts-2026-09-28.md)。按用户最新要求，当前使用[云希中文男声版](../../build/promo30/python-course-promo-30s-tts-male.mp4)。[晓晓女声版](../../build/promo30/python-course-promo-30s-tts.mp4)及原音乐版保留。

配音复现（本目录，需联网调用 Edge TTS）：

```bash
uv venv .venv-tts
uv pip install --python .venv-tts/bin/python -r requirements-tts.txt
.venv-tts/bin/python voiceover.py
```

`voiceover.py` 默认生成云希男声，保存七句配音及时间表；逐句测量，语速在原速至 +30% 内调整，超出时间窗则报错，不截断。5–6 秒保留音乐。人声归一化后触发音乐侧链压缩，复用原片视频流输出配音版。男声音频、独立 SRT 字幕及检查记录位于 `../../build/promo30/tts-male/`，女声记录位于 `../../build/promo30/tts/`；字幕未烧录到画面。在线服务再次生成的声音与时长可能变化。

两版均验证：30 秒、900 帧、完整解码通过、所有口播落入时间窗；具体响度见各自 verification.json。女声版另校验视频流哈希未变；两版均尚未完成真人听审。

复现（在本目录）：

```bash
npm ci
npm run serve
# 另一个终端
npx tsc --noEmit
node render.mjs
python3 soundtrack.py
ffmpeg -y -framerate 30 -i ../../build/promo30/frames/%05d.png -i ../../build/promo30/music-original.wav -frames:v 900 -t 30 -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart ../../build/promo30/python-course-promo-30s.mp4
```

需要 Node.js、FFmpeg、Python + NumPy，以及 Playwright Chromium。render.mjs 默认复用此机器已安装的 Chromium 路径；迁移时可用 CHROMIUM_PATH 覆盖。字体使用本机 Noto Sans CJK SC。渲染服务只绑定 127.0.0.1:9030。


依赖版本锁在 package-lock.json。安装审计报告有 3 个 moderate、2 个 high 上游问题；此工具仅供本地离线制作，未部署为公网服务。未为修复审计问题擅自替换动画引擎或跨版本升级。
