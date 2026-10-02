# ide-lesson-video 来源与版本记录

## 来源

- **自制技能，不是从外部仓库下载**，因此没有上游仓库地址、tag 或 commit 可引用。
- 由王旭晖在本机用 Codex 生成并迭代，首次成形于 2026-09-30，2026-10-02 完成一次功能与交付规范修订。
- 原始位置：`C:\Users\王\.codex\skills\ide-lesson-video\`，即 Codex 客户端的个人原生安装位置。
- 入库位置：本目录 `skills/ide-lesson-video/`，为**团队权威副本**。
- 版本标识：无上游版本号。以本技能首次入库的提交作为版本基线，后续修改在本目录内累积，靠 Git 历史区分。

## 两份副本的关系

根 [AGENTS](../../AGENTS.md) 规定项目技能只维护在仓库根 `skills/`，禁止为项目技能向 `.` 开头的目录写入、安装、复制或建立链接。个人 `.codex/skills/` 里那份属于规则中豁免的「既有客户端配置」，不要求删除，Codex 仍可用 `$ide-lesson-video` 原生调用。

但两份**不会自动同步**。本目录是唯一权威来源：要改技能，改这里、走 PR；改完再自行同步回个人客户端目录。不要把个人目录里的改动当作已入库。

## 版本记录

### 2026-10-02 修订（当前版本，18 个文件）

由原作者在 Windows 侧用 Codex 完成，本次按原样入库：

- **新增红圈与气泡注释**：课程 JSON 的 `stages[].annotations` 支持 `text` 与可选 `highlight`；只有显式提供非空 `highlight` 才画红色椭圆，气泡固定在编辑器右侧，连接线首节点按整行实测宽度落在目标代码行末尾。`scripts/lesson_style.py`、`scripts/render_lesson.py`、`scripts/verify_lesson.py` 相应扩展。
- **新增连续机械键盘音效**：`assets/list-demo/keyboard-continuous.wav`，17,584,040 字节，实测 48 kHz / 单声道 / 16-bit PCM / 183.17 秒，符合 `references/IDE-workflow.md` 第 6 节对素材格式的要求。课程 JSON 顶层新增 `typing_sound`（示例为 `enabled: true`、`volume: 0.75`、`source_start_seconds: 90`）。
- **字体改为显式失败**：`scripts/lesson_style.py` 不再有 Windows 字体默认值，未设置 `IDE_VIDEO_CODE_FONT` / `IDE_VIDEO_UI_FONT` 或路径无效时直接抛错，不回退系统字体。
- **依赖锁定版本**：`scripts/requirements.txt` 改为 `Pillow==12.3.0`、`imageio-ffmpeg==0.6.0`、`numpy==2.3.5`。
- **文档改名并去掉个人环境**：`references/workflow.md` → `references/IDE-workflow.md`，`references/lesson-format.md` → `references/IDE-lesson-format.md`；两份文档中的代码块均为 `~~~bash`，示例路径改为 `<输出目录>` 等占位符。`SKILL.md` 新增「新对话快速恢复」与「交付限制」两节，`agents/openai.yaml` 的简介与默认提示词同步更新。

### 2026-09-30 首次成形（已被上面版本取代）

同步版流程：旁白与逐字编辑同帧开始、每字符 0.1 秒、打完停 1 秒点击运行、指针 1.2 秒淡出。该版本随首次入库提交进入 Git 历史。

## 许可证

技能正文与脚本为自制，未附第三方许可证，随本仓库一同管理。运行时依赖 `Pillow==12.3.0`、`imageio-ffmpeg==0.6.0`、`numpy==2.3.5`（见 `scripts/requirements.txt`）各有自己的许可证，本目录不重复分发。

- `assets/list-demo/voice-1.wav`、`voice-2.wav`、`voice-3.wav`：阿里百炼 Ethan 中文男声生成的示例配音，实测 24 kHz / 单声道 / 16-bit PCM，只对应 `lesson.json` 中的示例旁白文本。对外分发或商用前需自行核实该服务的授权条款。
- `assets/list-demo/keyboard-continuous.wav`：据 `references/IDE-workflow.md` 第 6 节记载，来自 Freesound 的 “Mechanical Keyboard Typing (Treble Version)”，页面标注为 CC0。**本次入库未回访该页面复核许可证与来源链接**，替换或对外分发前请自行确认。

## 入库时做过的清理

只做下列必要清理，**没有改动任何渲染逻辑、时间轴参数或视觉样式**：

- 排除 `__pycache__/`、`*.pyc`、`.venv/`、`node_modules/` 与中间帧、临时 MP4。2026-10-02 版源目录本身已不含这些生成物（首次入库的 2026-09-30 版含 4 个 `.pyc`，约 51 KB）。
- 文件权限从 DrvFs 的 777 规范为目录 755 / 文件 644，与仓库其余文件一致。
- 行尾按源文件原样保留：`assets/style-reference.html`、`scripts/lesson_style.py`、`scripts/render_lesson.py` 为 CRLF，其余文本文件为 LF。这一混合状态与首次入库提交一致，本次未做统一转换，以免产生大面积纯空白差异。
- 本次未再改写文档内容：2026-10-02 版源文件已经不含个人绝对路径、`~~~powershell` 代码块和会话专用 `--runtime-dir`。
- 复核项：全目录无 `C:\`、`/mnt/c`、Windows 用户名目录、Codex 私有运行时路径；无 API 密钥或凭据样式字符串；单文件最大 17,584,040 字节，未超过根 AGENTS 的 100 MB 上限。

## 已知限制（使用前必读）

1. **产出不是真实 IDE 录屏。** `SKILL.md` 已写明当前实现是 Pillow 绘图与 FFmpeg 编码，源码单独真实执行。根 AGENTS 要求「动画中的编辑器外观不能冒充真实执行」，需要真实录屏的交付应改用 `studio/list-demo/` 那样的 code-server ＋ Playwright 方案，不能用本技能顶替。

2. **字体必须由运行环境提供。** `scripts/lesson_style.py` 现在直接读取 `IDE_VIDEO_CODE_FONT` 与 `IDE_VIDEO_UI_FONT`，缺失或路径无效即抛错，不自动回退。开发机 WSL 实测 `fc-list :lang=zh` 无输出，即发行版内没有中文字体，需自行安装或指向实际存在的字体文件；代码字体还必须是等宽的，否则光标与高亮的前缀宽度计算会错位。

3. **现成镜像都不能直接运行本技能。**
   - `docker/Dockerfile.studio`（基于 `mcr.microsoft.com/playwright:v1.58.2-noble`）已有 `python3`、`python3-numpy`、`ffmpeg`、`fonts-noto-cjk`、`fonts-dejavu-core`，以及装了 `edge-tts==7.2.8` 的 venv；缺 Pillow 与 imageio-ffmpeg。
   - `docker/Dockerfile.ide`（基于 `python:3.12-slim-bookworm`）只有 `curl`、`ca-certificates`、`git` 和上述两个字体包；**没有 ffmpeg，也没有 numpy**。
   - 要在容器内运行，需另建环境或临时安装 `scripts/requirements.txt`；按根 AGENTS，不要为此顺手升级现有镜像里的 Playwright、浏览器、字体或渲染引擎。

4. **锁定版本尚未在任何环境实测。** `scripts/requirements.txt` 的 `Pillow==12.3.0`、`imageio-ffmpeg==0.6.0`、`numpy==2.3.5` 是原作者 Windows 环境的结果，本仓库没有对应锁文件，也没在 WSL 或上述两个镜像里安装验证过。

5. **示例配音与键盘音效不可挪用。** 三个 voice WAV 只对应 `lesson.json` 中的示例旁白，换内容必须重新准备配音；`keyboard-continuous.wav` 是 183 秒的连续录音，按 `source_start_seconds` 与每段打字时长截取，换素材需保持 48 kHz / 单声道 / 16-bit PCM 并记录来源。

6. **历史验证记录已不在技能包内。** 首次入库版本的 `references/workflow.md` 末尾有两份 Windows 本机验证记录（同步版 810 帧 / 27 秒、历史打包版 1256 帧 / 41.867 秒），改名为 `references/IDE-workflow.md` 后未保留。需要那份记录时从 Git 历史的首次入库提交查阅，不要把它当作当前版本的验证结果。

7. `agents/openai.yaml` 是 Codex 客户端专有适配层，其他客户端忽略即可，不代表本技能已在那些客户端注册为原生技能。

## 验证状态

- **2026-10-02 版的验证记录：无。** 技能包内不再包含任何验证记录，原作者也未随本次修订提供新的成片实测结果。
- **本次入库没有在 WSL 或 Docker 内实际运行 `render_lesson.py` / `verify_lesson.py`**，跨机复现状态为「未执行」。上面第 2、3、4 条是据代码与镜像定义推断的风险点，尚未实测确认。
- 本次入库做过的实际检查只有静态项：文件清单与字节数、WAV 头部（用 Python `wave` 读取声道/位深/采样率/时长）、`lesson.json` 结构与 JSON 可解析性、行尾、权限、个人路径与密钥样式字符串扫描、单文件大小上限。
- 使用本技能前，请先在自己的环境跑一次 `assets/list-demo/` 离线复现，并把实际结果记入所属制作线的 `status.md`；按 `SKILL.md` 的「交付限制」，未执行的验证必须写「未执行」。
