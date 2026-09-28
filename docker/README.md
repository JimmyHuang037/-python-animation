# Linux 上的课程工作台

本目录是 Docker 配置的版本管理正文。集中管理入口为 `~/docker/python-animation/course`，
它链接到本仓的 `docker/course`，不复制两套配置。所有服务与制作任务在 Linux Docker 内运行。

## 环境和启动

需要 Linux x86_64、Docker Engine、Compose v2，以及用户能访问 Docker socket。
首次运行（仓库已经复制到 `~/python-animation`）：

```bash
cd ~/python-animation
./docker/course build
./docker/course up
./docker/course status
```

浏览器入口：Motion Canvas `http://127.0.0.1:9030/`，真实 Python IDE `http://127.0.0.1:9042/`。
服务在容器内监听 `0.0.0.0`，宿主机仅发布到回环地址；远程访问使用 SSH 转发。
不把无认证的录课 IDE 暴露到局域网或公网。

```bash
# 在 WSL 原生终端执行，浏览器访问本机 19030 / 19042。
ssh -N -L 19030:127.0.0.1:9030 -L 19042:127.0.0.1:9042 qwer@172.25.233.189
```

本机旧样片服务已占用 9030/9042 时，本机 Docker 可换端口：

```bash
MOTION_PORT=29030 IDE_PORT=29042 ./docker/course up
```

## 制作与文件

```bash
./docker/course demo       # 真 IDE 输入、保存、运行 Python、录屏和配音字幕合成
./docker/course preview    # 仅前 10 秒：IDE 录制 + 300 帧动画，测试机验收使用此命令
./docker/course animation  # Motion Canvas 渲染 900 帧、音乐合成、完整解码验证
./docker/course all        # 依次运行，避免小内存测试机同时编码
./docker/course logs
./docker/course down       # 停容器；保留依赖卷和宿主机产物
```

输出独立保存在 `build/docker/list-demo/` 与 `build/docker/promo30/`，不覆盖既有样片。
IDE 和 worker 将同一仓库挂载到相同 `/workspace` 路径，录制脚本读取的 `.py` 和输出就是 IDE
实际保存及执行的文件。音频时间表用相对文件名，支持从 WSL 迁到测试机。
录制测试可复用 `build/list-demo/voice-00.mp3` 至 `voice-06.mp3` 的已保存云希声音，
没有缓存时才调用 Edge TTS。动画测试生成原音乐版，不冒充配音版完整验收。

两个镜像对应三个角色：

| 角色 | 镜像 | 工作 |
|---|---|---|
| motion | studio | Vite / Motion Canvas 编辑器与动画页面 |
| ide | ide | code-server 4.139.1 与真正的 Python 解释器 |
| worker | studio | Playwright 1.58.2 对应 Chromium、FFmpeg、制作脚本 |

worker 按需启动、运行完退出；motion 与 ide 保持运行。Compose 检查两个服务健康后才执行 worker。
Vite 仅额外允许容器服务名 `motion`，不使用无限制的主机名允许设置。
源文件通过挂载直接生效；系统依赖变化执行 `build` 并重新 `up`。
Node 依赖放独立命名卷，启动脚本按锁文件哈希更新。依赖变化后应先停止服务，构建并重新启动，
不要在渲染中途修改锁文件或并发运行同一个小节的任务。

预览录像只保留时间轴前 10 秒，可能停在一行代码输入途中；核对已保存源码是否为预期源码前缀。
此段不含最后的 IDE 执行镜头，所以 `real_recorded_output` 为 null；另执行完整教学源码的结果
单独标为 `independent_execution_source: expected.py`，不当作录像里的运行证据。
完整实操用 `demo` 命令，声音和字幕分别按预览／完整时长导出。

## 已处理的迁移差异

- 不再硬编码开发机 Chromium 路径；默认由 Playwright 定位匹配浏览器，仍支持 `CHROMIUM_PATH`。
- worker 使用 `http://ide:9042` 与 `http://motion:9030`；容器间不用 `localhost`。
- `DEMO_OUTPUT_DIR` 控制实操输出位置，`IDE_WORKSPACE` 可覆盖 IDE 端工作区路径。
- `FRAMES_DIR`、`RENDER_URL`、`MUSIC_PATH` 控制动画产物与服务地址。
- 镜像使用构建者 UID/GID 写挂载目录，避免生成 root 所有的课程文件。

## 指定测试机与 WSL SSH

本次用户指定 `qwer@172.25.233.189`，实际为 Ubuntu 25.04 x86_64、约 4GB 内存。
它不是旧的 `ubuntu@127.0.0.1:2222` 测试入口，也不是生产服务器。

当前 WSL 使用 mirrored 网络，没有镜像 Windows 的 Hyper-V Default Switch 网段。
直接连接该 IP 会走校园网默认路由并超时。已经实测的连接方式是 WSL OpenSSH 经本机已有的
`127.0.0.1:12000` HTTP CONNECT 通道转接到测试机。用户 SSH 配置对该 IP 和 `qwer-test`
设置 `ProxyCommand /usr/bin/nc -X connect -x 127.0.0.1:12000 %h %p`。
这是一条转接路径，不是修复了底层路由；该本机端口需要保持可用。不依赖 Windows ssh.exe 启动任务。

本开发机 WSL 的 `/var/run/docker.sock` 实测连接 Docker Desktop Linux 引擎，因此本机从 WSL
执行 `course up` 后，Docker Desktop 能看到 `python-animation` 项目与 motion/ide 容器。
Docker Desktop 不会自动显示这台独立 Linux 测试机的容器。远端可在 WSL 用
`ssh qwer-test '~/docker/python-animation/course status'` 查看，浏览器通过 SSH 隧道直接操作。

本次已用 WSL 用户级 systemd 服务保持隧道，断线会重连。检查／关闭（在 WSL 执行）：

```bash
systemctl --user status python-animation-tunnel
systemctl --user stop python-animation-tunnel
systemctl --user start python-animation-tunnel
```

服务已 enable，在 WSL 用户服务启动后自动拉起，仍依赖本机 12000 CONNECT 端口和测试机在线。
服务模板为本目录 `python-animation-tunnel.service`。不要在同一端口重复运行前台隧道。

依据：[Playwright Docker](https://playwright.dev/docs/docker)、
[Compose 健康检查](https://docs.docker.com/compose/how-tos/startup-order/)、
[WSL 网络](https://learn.microsoft.com/en-us/windows/wsl/networking)。
