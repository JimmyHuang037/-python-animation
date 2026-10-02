# promo40 购物清单欢迎动画

来源：Gitee [PR #3](https://gitee.com/ljcc21/python-animation/pulls/3)，分支 `lesson06-video`，原始提交 `27f867a`。2026-10-02 用户要求将其中的新动画移入独立 `promo40` 文件夹并修复错误。执行者为本任务 Codex；审查人为用户，真人审片尚未执行。

当前片段是 **5秒**，文件夹名称不代表时长为40秒。使用 Motion Canvas，逻辑画布1280×720，成片1920×1080、30 fps、150帧。它是购物清单欢迎动画，不是当前“列表”5分钟里程碑的交付。PR附带的40秒视频 `deliverables/lesson06-revised-qwen-ethan.mp4` 保留原貌，本工程不宣称能够重建该视频。

本工程从 `studio/promo30` 分离新场景及其必要配置，原宣传片源码恢复为当前 `main` 版本。修复 `tween` 的归一化进度与秒数混用、列表行重复叠加纵坐标及左侧文字越出画布；独立端口、输出路径与渲染时长避免复用原宣传片的30秒入口。新工程将 `@motion-canvas/ui` 排除在Vite依赖预打包之外，避免2D编辑插件与UI使用不同上下文而导致编辑器空白。未重新调用配音API，本次输出无音轨。

## 复用现有 Docker 工作台

本工程与promo30使用相同依赖和锁定版本，无需修改Dockerfile或新增Compose服务。在已有工作台的 `motion` 容器中开发、渲染即可；先按 [Docker说明](../../docker/README.md)确认现有容器已经运行。

在仓库根目录进入容器：

```bash
docker compose -f docker/compose.yaml exec -w /workspace/studio/promo40 motion bash
```

在容器内准备项目依赖，再启动本工程的Vite进程；9033属于现有容器内的新进程，不新增制作服务：

```bash
npm ci --ignore-scripts
npm run serve -- --host 127.0.0.1 --port 9033 --strictPort
```

另一个终端进入同一容器和目录，执行下方的检查、渲染和合成命令。渲染入口默认为容器内 `http://127.0.0.1:9033/render.html`，不需要发布新宿主端口。宿主机源码经现有 `/workspace` 挂载进入容器，产物保存到 `build/promo40/`。现有Docker配置只发布9030；容器内9033不作为宿主浏览器编辑入口。

## 可选本机复现

在本目录使用Node.js、FFmpeg、Playwright Chromium和Noto Sans CJK SC字体：

```bash
npm ci
npx playwright install chromium
npm run serve -- --strictPort
```

在本机同目录，或上述容器的同目录中，执行：

```bash
npx tsc --noEmit
node render.mjs
ffmpeg -y -framerate 30 -i ../../build/promo40/frames/%05d.png -frames:v 150 -t 5 -c:v libx264 -preset fast -crf 18 -pix_fmt yuv420p -movflags +faststart ../../build/promo40/promo40.mp4
```

`CHROMIUM_PATH` 可指定已有Chromium，`RENDER_URL` 可指定渲染入口，`FRAMES_DIR` 可指定独立帧目录。`PREVIEW_SECONDS` 仅允许大于0且不超过5秒，并至少包含一帧。默认生成150帧，逐帧PNG作为中间产物忽略，不提交到Git。成片与技术验证记录可随工程交付。

2026-10-02 已在现有 `python-animation-motion-1` 容器内完成两份工程的TypeScript检查、promo40浏览器编辑器检查、150帧渲染、5秒视频编码及完整解码。复用 `python-animation-studio:local` 镜像，没有重建镜像或增加Compose服务。已检查第30和149帧，文字未越界，最终三件物品、加号和结尾均显示正常。技术记录与视频分别位于仓库根目录 `build/promo40/verification.json` 和 `build/promo40/promo40.mp4`；真人连续审片与跨机复现未执行。
