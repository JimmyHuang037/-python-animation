# ide-lesson-video 来源与版本记录

## 来源

- **自制技能，不是从外部仓库下载**，因此没有上游仓库地址、tag 或 commit 可引用。
- 由王旭晖在本机用 Codex 生成并迭代，首次成形于 2026-09-30。
- 原始位置：`C:\Users\王\.codex\skills\ide-lesson-video\`，即 Codex 客户端的个人原生安装位置。
- 入库位置：本目录 `skills/ide-lesson-video/`，为**团队权威副本**。
- 版本标识：无上游版本号。以本技能首次入库的提交作为版本基线，后续修改在本目录内累积，靠 Git 历史区分。

## 两份副本的关系

根 [AGENTS](../../AGENTS.md) 规定项目技能只维护在仓库根 `skills/`，禁止为项目技能向 `.` 开头的目录写入、安装、复制或建立链接。个人 `.codex/skills/` 里那份属于规则中豁免的「既有客户端配置」，不要求删除，Codex 仍可用 `$ide-lesson-video` 原生调用。

但两份**不会自动同步**。本目录是唯一权威来源：要改技能，改这里、走 PR；改完再自行同步回个人客户端目录。不要把个人目录里的改动当作已入库。

## 许可证

技能正文与脚本为自制，未附第三方许可证，随本仓库一同管理。运行时依赖 `Pillow`、`imageio-ffmpeg`、`numpy`（见 `scripts/requirements.txt`）各有自己的许可证，本目录不重复分发。

`assets/list-demo/voice-1.wav`、`voice-2.wav`、`voice-3.wav` 是阿里百炼 Ethan 中文男声生成的示例配音，只对应 `lesson.json` 中的示例旁白文本。对外分发或商用前需自行核实该服务的授权条款。

## 入库时做过的清理

只做下列必要清理，**没有改动任何渲染逻辑、时间轴参数或视觉样式**：

- 排除 `scripts/__pycache__/` 下 4 个 `.pyc`（约 51 KB）。仓库根 `.gitignore` 已有 `__pycache__/` 规则，无需另加。
- `SKILL.md` 与 `references/workflow.md` 中的 `~~~powershell` 代码块改为 `~~~bash`。
- 删除 `references/workflow.md` 第 8 节的个人绝对路径：Windows 用户名目录、Codex 私有 Python 运行时、某次会话专用的 `--runtime-dir`。改为技能目录内相对路径加 `<输出目录>` 占位符，符合 [Windows 接入说明](../../docs/production/windows-access.md)「外部个人绝对路径要落实为本机取得步骤或团队素材清单」的要求。
- 按脚本实际的 argparse 定义补充参数说明：`--lesson`、`--output`、`--manifest` 必填，`--runtime-dir`、`--compare-audio` 可选。
- 文件权限从 DrvFs 的 777 规范为 644，与仓库其余文件一致。
- `agents/openai.yaml` 原样保留，未改动。

## 已知限制（使用前必读）

1. **产出不是真实 IDE 录屏。** `SKILL.md` 已写明当前实现是 Pillow 绘图与 FFmpeg 编码，源码单独真实执行。根 AGENTS 要求「动画中的编辑器外观不能冒充真实执行」，因此**本技能不能用于交付「列表5分钟样片」后 2分30秒的真实 Python 演示**；那部分需要 `studio/list-demo/` 那样的 code-server ＋ Playwright 真实录屏。

2. **字体默认值是 Windows 路径。** `scripts/lesson_style.py` 第 8–9 行默认取 `C:/Windows/Fonts/consola.ttf` 与 `C:/Windows/Fonts/msyh.ttc`。在 WSL 或本项目 Docker 内必须显式设置 `IDE_VIDEO_CODE_FONT`、`IDE_VIDEO_UI_FONT`，否则渲染取不到字体即失败，脚本不会回退到系统字体。**这两行按原样保留未改**，因为改动会影响 Windows 侧既有行为。

3. **现成镜像都不能直接运行本技能。**
   - `docker/Dockerfile.studio`（基于 `mcr.microsoft.com/playwright:v1.58.2-noble`）已有 `python3`、`python3-numpy`、`ffmpeg`、`fonts-noto-cjk`、`fonts-dejavu-core`，以及装了 `edge-tts==7.2.8` 的 venv；缺 Pillow 与 imageio-ffmpeg。
   - `docker/Dockerfile.ide`（基于 `python:3.12-slim-bookworm`）只有 `curl`、`ca-certificates`、`git` 和上述两个字体包；**没有 ffmpeg，也没有 numpy**。
   - 开发机 WSL 实测 `fc-list :lang=zh` 无输出，即发行版内没有中文字体，需自行安装或指向 Windows 侧字体。

4. **依赖未锁版本。** `scripts/requirements.txt` 只有 `Pillow`、`imageio-ffmpeg`、`numpy` 三个裸包名。`docs/production/windows-access.md` 要求生产依赖使用现有 Dockerfile 或锁文件，此处尚未落实。

5. **示例内容只覆盖列表操作的一小部分。** `assets/list-demo/stage1.py`、`stage2.py`、`stage3.py` 只演示 `+` 与 `+=`；「列表5分钟样片」要求的五个操作还缺 `*`、`append()`、`extend()`、`insert()`。

6. **示例配音不可复用。** 三个 WAV 只对应 `lesson.json` 中的示例旁白，换内容必须重新准备配音。

7. `agents/openai.yaml` 是 Codex 客户端专有适配层，其他客户端忽略即可，不代表本技能已在那些客户端注册为原生技能。

## 验证状态

- `references/workflow.md` 末尾的两份验证记录（2026-09-30 同步版、历史打包版）是**原作者在 Windows 本机**的结果，随技能原样保留。
- **本次入库没有在 WSL 或 Docker 内实际运行 `render_lesson.py` / `verify_lesson.py`**，跨机复现状态为「未执行」。上面第 2、3 条是据代码与镜像定义推断的风险点，尚未实测确认。
- 使用本技能前，请先在自己的环境跑一次 `assets/list-demo/` 离线复现，并把实际结果记入所属制作线的 `status.md`，不要沿用本文件里 Windows 侧的历史记录当作自己的验证。
