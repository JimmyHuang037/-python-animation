# Linux 上的课程工作台

本目录是 Docker 配置的版本管理正文。四位开发者在各自 WSL2 仓库根目录使用共用入口 `./docker/course`，
课程工作台服务与这里的样片制作命令在 Linux Docker 内运行。个人可建立 `~/docker/python-animation/course`
软链指向本仓 `docker/course`，但新克隆不默认带有该入口。协作与任务范围遵守[根 AGENTS](../AGENTS.md)；文档任务不要求启动容器或制作视频。

## 环境和启动

需要 Linux x86_64、Docker Engine、支持本配置的 Docker Compose，以及用户能访问 Docker socket。

用 Docker Desktop 承载引擎时，必须在 Settings → Resources → WSL integration 勾选目标发行版。
未勾选的表现是：WSL 内没有 `docker` 命令、没有 `/var/run/docker.sock`，从 Windows 侧
`docker.exe` 挂载 `\\wsl.localhost\<发行版>\...` 报
`stat /run/guest-services/distro-services/<发行版>.sock: no such file or directory`。
勾选后发行版内自动出现 CLI 与 socket，用户被加入 `docker` 组；已登录的会话要重开终端才带上该组，
临时可用 `sg docker -c '<命令>'` 执行。

首次运行：在本机实际仓库根目录执行。下面 `~/python-animation` 是示例路径，按自己的克隆位置替换。

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
# 在 WSL 原生终端执行；把 user@host 换成已授权的测试机账号和地址。
# 浏览器访问本机 19030 / 19042，远端端口按该机实际配置调整。
ssh -N -L 19030:127.0.0.1:9030 -L 19042:127.0.0.1:9042 user@host
```

本机已有服务占用 9030/9042 时，可换宿主端口；不同成员电脑使用相同端口不会互相影响：

```bash
MOTION_PORT=29030 IDE_PORT=29042 ./docker/course up
```

### 2026-09-29 Docker Hub 拉取失败的排查记录

当时网络下 `auth.docker.io` 与 `registry-1.docker.io` 只解析到无关的 IPv6 地址且没有 A 记录，
`ide` 镜像的 `FROM python:3.12-slim-bookworm` 会以
`DeadlineExceeded: failed to fetch anonymous token ... i/o timeout` 失败。
当时 `mcr.microsoft.com`（studio 基础镜像）、GitHub releases（code-server）、PyPI 与 apt 源不受影响，
这次故障定位为 Hub 拉取超时。其他成员遇到构建失败时，先核对实际报错和网络，不直接套用这一结论。

确认是同类拉取故障后，可在本机 Docker Desktop → Settings → Docker Engine 配置镜像加速：

```json
{ "registry-mirrors": ["https://docker.m.daocloud.io"] }
```

临时做法是先从镜像源拉取再打回原 tag，不修改本仓任何文件：

```bash
docker pull docker.m.daocloud.io/library/python:3.12-slim-bookworm
docker tag docker.m.daocloud.io/library/python:3.12-slim-bookworm python:3.12-slim-bookworm
./docker/course build
```

该 tag 只存在于本地镜像库；换机器或清理镜像后要重做，长期使用请改用上面的持久配置。

## 制作与文件

以下命令只对应现有五行列表 IDE 样片和 promo30 动画，不是任意新小节的通用入口。任务所需区间和验收以任务正文为准。

```bash
./docker/course demo       # 真 IDE 输入、保存、运行 Python、录屏和配音字幕合成
./docker/course preview    # 仅前 10 秒：IDE 录制 + 300 帧动画，原指定测试机的有限验证
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

`build/docker/` 被当前 `.gitignore` 忽略；其他 `build/` 路径不能一概视为被忽略或已经随 Git 交付。
交接时核对文件是否实际可取得，并提供团队可访问地址和哈希；共享产物位置尚待选定并验证。

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

同机多任务还须隔离源码目录、Compose 项目、宿主端口、可写卷与输出。当前 `docker/course`
尚未提供全部任务隔离参数，不能仅改端口就宣称完成隔离；由 DevOps 按任务实现和核对。

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

## 原开发机与指定测试机记录：2026-09-28

以下保留原开发机的已执行配置与来源，不是四位成员的环境前提；其他机器须自行核对账号、路由、代理与服务。

用户当时指定 `qwer@172.25.233.189`，实际为 Ubuntu 25.04 x86_64、约 4GB 内存。
它不是旧的 `ubuntu@127.0.0.1:2222` 测试入口，也不是生产服务器。

原开发机当时的 WSL 使用 mirrored 网络，没有镜像 Windows 的 Hyper-V Default Switch 网段。
直接连接该 IP 会走校园网默认路由并超时。当时实测的连接方式是 WSL OpenSSH 经该机已有的
`127.0.0.1:12000` HTTP CONNECT 通道转接到测试机。原开发机 SSH 配置对该 IP 和 `qwer-test`
设置 `ProxyCommand /usr/bin/nc -X connect -x 127.0.0.1:12000 %h %p`。
这是一条转接路径，不是修复了底层路由；该本机端口需要保持可用。不依赖 Windows ssh.exe 启动任务。

原开发机 WSL 的 `/var/run/docker.sock` 当时实测连接 Docker Desktop Linux 引擎，因此该机从 WSL
执行 `course up` 后，Docker Desktop 能看到 `python-animation` 项目与 motion/ide 容器。
Docker Desktop 不会自动显示这台独立 Linux 测试机的容器。远端可在 WSL 用
`ssh qwer-test '~/docker/python-animation/course status'` 查看；这依赖原有 SSH 别名和远端软链。
当时的前台转发命令如下，浏览器通过 SSH 隧道操作：

```bash
ssh -N -L 19030:127.0.0.1:9030 -L 19042:127.0.0.1:9042 qwer@172.25.233.189
```

原开发机当时使用 WSL 用户级 systemd 服务保持隧道，断线会重连。检查／关闭（仅在已安装该服务的 WSL 执行）：

```bash
systemctl --user status python-animation-tunnel
systemctl --user stop python-animation-tunnel
systemctl --user start python-animation-tunnel
```

该服务在原开发机当时已 enable，在 WSL 用户服务启动后自动拉起，依赖该机 12000 CONNECT 端口和测试机在线。
本目录 `python-animation-tunnel.service` 是原配置模板，复制仓库不等于已经安装或启动服务。
使用前调整本机配置；不要在同一端口重复运行前台隧道。

依据：[Playwright Docker](https://playwright.dev/docs/docker)、
[Compose 健康检查](https://docs.docker.com/compose/how-tos/startup-order/)、
[WSL 网络](https://learn.microsoft.com/en-us/windows/wsl/networking)。
