# Python 实操视频自动制作：GitHub 方案核查

> 文档性质：按下述日期保留的历史研究、证据或提案，不是当前开发指令。四位开发者及各自 AI 执行时，以[根 AGENTS](../../AGENTS.md)、[课程范围](../../course/README.md)和[四人工作流](team-workflow-2026-10-01.md)为准；旧建议不覆盖当前约束。
>
> code-server＋Playwright 后续已有样片实现；下文“尚未制作”是当日状态。各项验收是否通过，以对应任务、实际产物和验证证据为准。

日期：2026-09-28。结论为研究建议；未安装候选软件，未完成组合链路实测。

## 需求与视频依据

用户要保留参考片后段的 IDE 实操观感，同时由 AI 完成代码准备、自动输入、运行、修改和录屏，不需要本人手敲。附件 python_step.md 提供三步流程参考：AI 准备代码、TTS＋打字复现、同步录屏。附件不是本轮执行指令。

原片：`C:\Users\JimmyHuang\Downloads\video_Python列表 _ 创一个购物..._0.mp4`。ffprobe 测得 391.16 秒、1280×720。本轮抽查 02:50、03:20、03:50、04:20、05:00、06:00；03:20 仍为动画转场，03:50 起的抽查点为真实 IDE 风格代码编辑与运行输出，可见列表 append/remove、索引和数值处理。未完整观看或确认切换的精确时刻，也未据此判断作者的整套制作工具。

[联系表](evidence/python-auto-demo-2026-09-28/contact-sheet.jpg)；[GitHub API 快照](evidence/python-auto-demo-2026-09-28/github-metadata.json)。

## star 与维护信号

以下数据来自本轮 GitHub REST API，星数会变动；最后推送日期仅作维护信号，不能等同稳定版发布时间或质量保证。

| 仓库 | stars | 最后推送 UTC |
|---|---:|---|
| [charmbracelet/vhs](https://github.com/charmbracelet/vhs) | 21,004 | 2026-09-24 |
| [asciinema/asciinema](https://github.com/asciinema/asciinema) | 17,844 | 2026-08-14 |
| [microsoft/playwright](https://github.com/microsoft/playwright) | 96,804 | 2026-09-28 |
| [coder/code-server](https://github.com/coder/code-server) | 79,500 | 2026-09-26 |
| [asweigart/pyautogui](https://github.com/asweigart/pyautogui) | 12,715 | 2024-08-20 |
| [obsproject/obs-studio](https://github.com/obsproject/obs-studio) | 76,726 | 2026-09-26 |
| [estruyf/vscode-demo-time](https://github.com/estruyf/vscode-demo-time) | 247 | 2026-09-03 |
| [HamedFathi/Replay](https://github.com/HamedFathi/Replay) | 16 | 2025-06-13 |
| [marcosgomesneto/typing-simulator](https://github.com/marcosgomesneto/typing-simulator) | 44 | 2024-02-11 |
| [rany2/edge-tts](https://github.com/rany2/edge-tts) | 12,111 | 2026-03-22 |
| [AhmadAl-Khatib/Coding-Virtual-Studio](https://github.com/AhmadAl-Khatib/Coding-Virtual-Studio) | 1 | 2026-04-21 |

## 推荐顺序

### 1. code-server＋Playwright＋TTS＋FFmpeg

最适合当前 WSL2、批量自动生成课程的方向。code-server 提供浏览器中的 VS Code 环境；在 WSL／容器里实际安装 Python，通过集成终端运行保存的源码。Playwright 自动控制编辑器、输入、快捷键和页面录制。两者是成熟组件，组合成课程制作链仍需编写衔接脚本，不是已存在的一键课程产品。

AI 先生成并执行验证每个教学阶段的代码，再生成口播和事件表。逐句合成 TTS、测量时长后，安排输入／高亮／保存／运行／等待实际输出等动作，录制后按事件时间合成配音和字幕。不能仅凭固定等待认定程序完成；记录实际输出和退出码。Playwright 页面录像不应被当作完整配音制作功能。

优点是可在 WSL／容器运行、不依赖 Windows 前台桌面，能保留真实编辑器和真实解释器。待样片验证：中文逐字插入、Python 自动缩进、终端输出就绪检测、编辑器升级后的定位稳定性、录制清晰度和配音同步。固定版本与画面尺寸，关闭会改写内容的自动补全／格式化。无需为学生开发网站或在线 IDE 平台。

依据：[code-server](https://github.com/coder/code-server)、[Playwright](https://github.com/microsoft/playwright)、[录像文档](https://playwright.dev/docs/videos)、[键盘与文本输入](https://playwright.dev/docs/api/class-keyboard)。

### 2. Demo Time＋VS Code＋OBS

功能最贴近已有桌面 IDE 课程演示。Demo Time 支持逐字符／逐行插入、修改、高亮、终端命令，并有 API 供脚本触发步骤。配合 OBS 录制和 TTS 时间表可构成自动制作方案；具体集成仍需验证。它只有 247 stars，不能包装成高星项目。OBS 的高星数也不能算到插件头上。

Demo Time 的 recording demos 指记录编辑操作生成演示动作文件，不能据此声称它直接录制最终 MP4。OBS 可通过 obs-websocket 远程控制；该功能自 OBS 28 起内置。

依据：[Demo Time](https://github.com/estruyf/vscode-demo-time)、[文本动作](https://demotime.show/actions/text/)、[终端动作](https://demotime.show/actions/terminal/)、[API](https://demotime.show/references/api/)、[动作录制](https://demotime.show/features/recording-demos/)、[OBS](https://github.com/obsproject/obs-studio)、[obs-websocket](https://github.com/obsproject/obs-websocket)。

### 3. VHS：终端演示首选备选

21,004 stars。用 .tape 脚本定义自动打字、按键、停顿、外观和导出，可在终端真实运行 Python，支持 MP4 和 Docker。最接近高星的“演示脚本生成视频”工具，但主要呈现终端／终端编辑器，不能等同参考视频的图形 IDE。需要另接配音和字幕。如果接受 Python 终端课堂风格，它可明显缩小制作范围。

依据：[VHS 官方仓库](https://github.com/charmbracelet/vhs)。

## 其他候选为何不优先

- PyAutoGUI（12,715 stars）能自动控制桌面键鼠，适合必须复用指定桌面 IDE 的情形；坐标／焦点／中文输入和桌面会话会增加稳定性工作。API 显示最后推送为 2024-08-20，不能仅因高星就说维护活跃。WSL 内的控制环境也不能直接假定能操纵 Windows 前台。
- asciinema（17,844 stars）主要记录终端会话，不直接包办 IDE 自动操作、TTS 与成片。已有 VHS 更符合脚本式终端演示。
- Replay（16 stars）、typing-simulator（44 stars）、Coding-Virtual-Studio（1 star）未满足用户高星成熟优先；没有必要只因名称贴合就优先安装。
- edge-tts（12,111 stars）可复用已有配音试作路线，但它是依赖在线服务的独立项目；不把它称作微软官方产品，也不能承诺服务稳定性。

## 可审查的后续样片范围

建议 60～90 秒：自动输入中文购物列表→追加／删除→保存并真实运行→高亮输出→修改一行→再次运行；配合逐句口播。确认画面、源码、实际输出和声音时间点一致。AI 可以承担全部制作操作，成片仍需核验。该样片尚未制作，本次不新增部署或自动化服务。
