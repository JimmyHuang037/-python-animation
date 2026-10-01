# 五行购物列表：真实 Python 自动实操

2026-09-28 用户确认 code-server＋Playwright 方案，仅演示截图的五行代码，复用 `zh-CN-YunxiNeural` 云希男声。独立实操样片，不拼入内容无关的宣传片；这些范围与声音只用于本样片。

- `shopping.py`：教学代码唯一源；最终输出 `['键盘']`。
- `prepare.py`：实际执行核对，并使用既有 edge-tts 7.2.8 环境生成七句对应口播。
- `editor-settings.json`：大字号、关闭自动补全与自动缩进、精简真实编辑器界面。
- `setup.py`：安装固定 code-server 4.139.1 到 `build/list-demo/tools/`，创建隔离配置和工作区；本地依赖/会话路径按根 `.gitignore` 排除，不代表整个 `build/` 被忽略。
- `record.mjs`：Playwright 在 Chromium 中逐字输入、保存，核对磁盘源码；通过集成终端执行 Python，核对 tee 保存的真实标准输出。绿色校准帧只用于剪辑，不进入成片。
- `compose.py`：根据实际录制事件对齐逐句声音，烧录字幕，导出 H.264/AAC MP4，完整解码并再次执行 Python 校验。

## 共用 Docker 样片入口

四位成员在各自 WSL2 仓库根目录按[Docker 工作台说明](../../docker/README.md)构建和启动，用 `./docker/course demo` 制作本样片；Docker 输出在 `build/docker/list-demo/`。此入口不自动支持其他新小节，验收仍以各自任务为准。

## 可选本机原生复现

以下保留原样片的本机原生复现步骤，不要求四位成员都配置此路径。在本目录运行；需要 Python 3.12+（`setup.py` 使用 tarfile 解包过滤参数）、Node.js、FFmpeg、中文字体及匹配的 Chromium。原开发机的 TTS 虚拟环境位于 `../promo30/.venv-tts`；新克隆须先按[配音工程说明](../promo30/README.md)创建该环境和安装锁定依赖，或使用上述 Docker 路线。

```bash
npm ci --ignore-scripts
python3 setup.py
# 在另一个终端执行 setup.py 打印的本地 code-server 启动命令。
../promo30/.venv-tts/bin/python prepare.py
node record.mjs
python3 compose.py
```

Playwright 固定为 1.58.2。默认使用该版本管理的 Chromium；本机首次安装可执行 `npx playwright install chromium`，也可用 `CHROMIUM_PATH` 显式覆盖。服务本地默认监听 `127.0.0.1:9042`；Docker 内部监听 `0.0.0.0`、宿主端口仅绑定回环地址。录制过程中不用人工按键。

Linux Docker 启动与实际录制见 [Docker 入口](../../docker/README.md)。`IDE_URL`、`IDE_WORKSPACE` 和 `DEMO_OUTPUT_DIR` 可配置服务地址与共享路径；新声音时间表使用相对文件名，合成也兼容旧绝对路径时间表中的同名本地声音文件。

原生复现产物默认位于 `../../build/list-demo/`：`shopping-list-yunxi.mp4`、`captions.srt`、逐句声音、`events.json`、`verification.json` 和关键帧。浏览器源录像为 25fps，MP4 交付为 30fps，转换不增加动作采样信息。声音按实际事件对齐，不截断口播；网络 TTS 再生成的时长可能变化。克隆后核对所需缓存和媒体是否实际存在；团队交接提供可访问地址与哈希，个人本机路径不作为共享交付地址。

历史样片检查范围：真实 UI 输入、保存源码一致性、真实输出、独立执行退出码、1080p 媒体参数、完整解码、关键帧排版。尚未由用户连续听审；不将机器检查称作人工验收或所有成员电脑的复现通过。新交付按任务记录已执行/失败/未执行及指定审查人。
