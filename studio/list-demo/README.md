# 五行购物列表：真实 Python 自动实操

用户确认 code-server＋Playwright 方案，仅演示截图的五行代码，复用 `zh-CN-YunxiNeural` 云希男声。独立实操样片，不拼入内容无关的宣传片。

- `shopping.py`：教学代码唯一源；最终输出 `['键盘']`。
- `prepare.py`：实际执行核对，并使用既有 edge-tts 7.2.8 环境生成七句对应口播。
- `editor-settings.json`：大字号、关闭自动补全与自动缩进、精简真实编辑器界面。
- `setup.py`：安装固定 code-server 4.139.1 到忽略的 build 目录，创建隔离配置和工作区。
- `record.mjs`：Playwright 在 Chromium 中逐字输入、保存，核对磁盘源码；通过集成终端执行 Python，核对 tee 保存的真实标准输出。绿色校准帧只用于剪辑，不进入成片。
- `compose.py`：根据实际录制事件对齐逐句声音，烧录字幕，导出 H.264/AAC MP4，完整解码并再次执行 Python 校验。

## 复现

在本目录运行；需要 Python 3.11+、Node.js、FFmpeg、中文字体及 Chromium。已有 TTS 虚拟环境位于 `../promo30/.venv-tts`。

```bash
npm ci --ignore-scripts
python3 setup.py
# 在另一个终端执行 setup.py 打印的本地 code-server 启动命令。
../promo30/.venv-tts/bin/python prepare.py
node record.mjs
python3 compose.py
```

Playwright 固定为 1.58.2。本机显式复用 Chromium 1228，已实际录制验证；其他机器用 `CHROMIUM_PATH` 指定浏览器，建议使用匹配的 Playwright Chromium。服务仅监听 `127.0.0.1:9042`，不用生产环境。录制过程中不用人工按键。

产物位于 `../../build/list-demo/`：`shopping-list-yunxi.mp4`、`captions.srt`、逐句声音、`events.json`、`verification.json` 和关键帧。浏览器源录像为 25fps，MP4 交付为 30fps，转换不增加动作采样信息。声音按实际事件对齐，不截断口播；网络 TTS 再生成的时长可能变化。

检查范围：真实 UI 输入、保存源码一致性、真实输出、独立执行退出码、1080p 媒体参数、完整解码、关键帧排版。尚未由用户连续听审；不将机器检查称作人工验收。
