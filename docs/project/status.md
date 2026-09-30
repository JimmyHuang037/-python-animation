# 当前状态

更新时间：2026-09-29。

## 本机 Docker 工作台搭建：2026-09-29

- 在新的 WSL2 发行版 `Ubuntu-24.04`（用户 `yanghua0`，仓库在 `/home/yanghua0/python-animation`）从零搭建 Docker 工作台。开始前该发行版内没有 docker CLI、没有 `/var/run/docker.sock`；Windows 侧 Docker Desktop 4.93.0（引擎 29.8.1、Compose v5.5.1）在运行，但 0 容器 0 镜像。
- 根因是 Docker Desktop 未对该发行版开启 WSL integration，Windows 侧 `docker.exe` 也因此无法挂载 `\\wsl.localhost`。用户在 GUI 勾选后，发行版内自动出现 `/usr/bin/docker`、`/var/run/docker.sock` 与 `docker` 组成员身份；已登录会话需重开终端或临时用 `sg docker -c` 才带该组。
- 首次 `./docker/course build` 失败于 `ide` 目标：本网络对 `auth.docker.io`／`registry-1.docker.io` 做 DNS 污染，只返回无关 IPv6 且无 A 记录。处理办法已写入 [Docker 工作台说明](../../docker/README.md)；本次采用临时方式，从 `docker.m.daocloud.io` 拉取 `python:3.12-slim-bookworm` 再打回原 tag，未修改仓库内 Dockerfile。该 tag 只在本地镜像库，不随仓库迁移。
- 第二次构建成功：`python-animation-studio:local` 3.95GB、`python-animation-ide:local` 1.4GB。`./docker/course up` 后 motion 与 ide 均 healthy，发布在回环 9030／9042；本机无旧样片服务占用，未改用 29030／29042。
- 容器内实测：motion 侧 Node v24.13.0、npm 11.6.2、Python 3.12.3、numpy 1.26.4、ffmpeg 6.1.1、edge-tts 7.2.8、Playwright 1.58.2，Chromium 145.0.7632.6 无头启动成功；ide 侧 Python 3.12.14、code-server 4.139.1、git 2.39.5。两容器 `/workspace` 均可写，promo30 与 list-demo 的 node_modules 已就位。
- HTTP 核对：`http://127.0.0.1:9030/` 与 `/render.html` 均 200，`http://127.0.0.1:9042/healthz` 返回 `{"status":"alive"}`。仓库 `git status` 干净，容器未污染工作区。
- 已建 `~/docker/python-animation` → 仓库 `docker/` 软链，恢复文档所述集中入口。
- 按用户要求本轮未跑 `preview`／`demo`／`animation`，样片验收推迟；本机因此没有新的预览或成片产物，不能据此声称制作链已在新机器验收通过。
- 文档中的测试机路径本次不可用：`~/.ssh/config` 缺失、本机 12000 CONNECT 端口未监听、`python-animation-tunnel` 用户服务不存在。历史记录里的 `qwer@172.25.233.189` 隧道与 `/home/jimmyhuang` 路径属旧开发机，本机未复现也未改写。

## 旧大写目录清理：2026-09-28

- `/home/jimmyhuang/Python_Animation` 仅剩 Vite 临时缓存目录；结束旧路径启动的本机 Vite 进程后，该目录已删除。
- Claude Desktop 三条会话登记中的工作目录已改为 `/home/jimmyhuang/python-animation`。历史对话、日志和导入材料中的旧名称保留为来源记录，不作为运行入口。
- 本机 Docker 工作台仍使用小写目录挂载；`127.0.0.1:29030` 和 `127.0.0.1:29042` 对应的容器保持健康。旧 Vite 独立监听端口 `127.0.0.1:9030` 已关闭。

## README 状态与材料索引同步：2026-09-28

- 根 README 的旧说明称尚未安装动画框架、未部署 Docker，已与实际进度不符；现已更新为当前工作台和样片状态，并标注核对日期。
- 本次只读核对：WSL 本机 `motion`、`ide` 容器均 healthy（回环端口 29030/29042）；指定 Ubuntu 测试机同两容器均 healthy（9030/9042）；`python-animation-tunnel` 用户级服务 active 且 enabled。
- README 的材料概览现包含导入资料、未定稿课程目录、宣传动画多个版本、列表 IDE 实操样片和制作环境入口；详细制作与验收记录仍以本文件各条目为准。
- 根 README 保留概览；启动与端口细节仍由 [Docker 工作台说明](../../docker/README.md) 维护。完整课程仍未完成，课数和分钟数也未定稿。

## Linux Docker 工作台与测试机验证：2026-09-28

- 用户授权 Docker 落地，并指定 `qwer@172.25.233.189`；最新要求测试仅跑前 10 秒。实际测试机为 Ubuntu 25.04、16 个逻辑 CPU、约 4GB 内存，不与原 KVM 两核测试环境混用。
- 两个镜像、三个角色已实现；本机 WSL 命令连接 Docker Desktop Linux 引擎，独立测试机使用 Docker 28.2.2 / Compose 2.37.1。两边镜像文件系统层逐项一致，motion / ide 均 healthy。
- 本机完整 IDE 样片约 40.43 秒，核对真实保存源码与终端输出 `['键盘']`；测试机按用户要求只交付 10 秒 IDE 预览和 10 秒／300 帧动画，均为 1080p，完整解码通过。前 10 秒 IDE 预览尚未到运行代码镜头，不能称其包含终端输出验收；独立源码执行结果另记。
- 修复浏览器硬编码路径、容器内服务地址、监听范围、共享工作区与声音路径；同时修复 Vite 服务名白名单、文件搜索等待和隐藏终端误匹配。
- WSL 原生 SSH 通过本机既有 12000 CONNECT 端口连测试机；用户级 systemd 隧道暴露本机 19030／19042。底层 mirrored 网络没有到 Default Switch 的直连路由，转接依赖该端口可用。
- [启动说明](../../docker/README.md)、[验证记录](../production/docker-verification-2026-09-28.json)。测试输出在 `build/docker/`，不覆盖既有定稿视频；镜像、会话和测试输出不提交 Git。未做真人连续听审。


## 五行列表实操云希样片：2026-09-28

- 按用户确认的 code-server＋Playwright 方案完成真实 IDE 自动输入、保存与 Python 执行，使用截图五行代码，输出 `['键盘']`；复用既有云希男声环境生成本段对应讲解。
- [成片](../../build/list-demo/shopping-list-yunxi.mp4)：约 40.43 秒、1920×1080、H.264/AAC，带同步字幕与自动输入标识。本次仅五行实操片段，不混入内容无关的宣传片。
- [工程](../../studio/list-demo/README.md)、[验证记录](../../build/list-demo/verification.json)。已检查 UI 输入后的磁盘源码、真实终端输出、独立运行退出码、完整解码与关键帧。源录像 25fps，交付 30fps；尚未用户连续听审。
- 独立本地 code-server 4.139.1 服务用于录制；未部署公网、未提交或推送。


## Qwen3-TTS API 试听完成：2026-09-28

- 已使用用户提供的本机凭据调用百炼 API，生成[Qwen 晨煦男声视频](../../build/promo30/python-course-promo-30s-qwen-ethan.mp4)，模型 qwen3-tts-instruct-flash-2026-01-26、音色 Ethan。凭据未复制到工程、日志或输出。
- 八段口播包含“一站式解决！”；该句音频 1.04 秒，画面延长至 5–7 秒，声音从 5.4 秒开始。学分目标调整为 7–10 秒，后续主要分镜保持原时点；重新渲染 Motion Canvas 并同步音乐提示音。
- TypeScript 检查、900 帧渲染、1920×1080／30 秒、完整解码及八段时间窗检查通过；抽查“一站式解决”画面。证据见 build/promo30/qwen-ethan/verification.json，尚未真人听审。
- 八次 API 返回共 196 计费字符；按 0.8 元／万字符估算 0.01568 元，未核实免费额度或账单。API／组装脚本与复现说明见 studio/promo30/README.md；没有部署本地 Qwen 模型。

## Qwen3-TTS API 试听准备：2026-09-28

- 已获用户授权使用 API，并要求朗读“一站式解决”。新增 studio/promo30/qwen_voiceover.py，按官方 HTTP 接口调用，可选 Ethan／Cherry；八段口播共 110 字符，dry-run 通过。
- 脚本仅负责分段合成与测量、提出总长 30 秒的新时间表；待实际音频到位后修改并渲染对应动画、混音和验收。当前尚无百炼 API Key，未调用 API、未产生 Qwen 配音或成片。用户已询问开通网站。

## Gitee 独立仓库：2026-09-28

- 已初始化独立 Git 仓库，主分支 `main`，主远端 `origin` 为 `git@gitee.com:ljcc21/python-animation.git`。
- 首次提交前检查待纳入文件，没有单个超过 100 MB；补充排除 `.venv-*`、Python 缓存与本地 Claude 配置，允许 `.env.example`。
- 此记录更新了下方历史记录中的“尚非独立仓库”状态；推送结果以 Git 远端验证为准。

## AI 自动完成后段实操：2026-09-28

- 已按用户最新要求更新后段制作方式：AI 准备代码、自动输入、运行、修改及录屏，不要求用户手敲。
- 已抽查列表参考视频六个时间点，核对 11 个 GitHub 仓库的实时 star 与维护信息，形成[选型研究](../research/python-auto-demo-2026-09-28.md)。
- 建议 WSL2 内采用 code-server＋Playwright，Demo Time＋OBS 为桌面备选，VHS 为终端风格备选。均未据此安装或完成制作链实测，未冻结选型。


## 项目目录改名：2026-09-28

- 用户确认统一命名为 `python-animation`，本地目录已迁至 `/home/jimmyhuang/python-animation`；全局入口、项目入口、需求及架构目录示例同步更新。
- 已修正项目内 TTS 虚拟环境启动脚本的绝对路径；历史记录、导入原件保持原貌。
- 项目尚未建立独立 Git 仓库，本次没有远端仓库改名或推送。

## 宣传片改中文男声：2026-09-28

- 按用户“用中文男声”的要求，已生成[云希男声版](../../build/promo30/python-course-promo-30s-tts-male.mp4)，原女声版保留；脚本默认改为 zh-CN-YunxiNeural。
- 男声逐句重新生成、测量和对齐，独立音频／字幕／时间表保存于 build/promo30/tts-male；30 秒、900 帧、完整解码和分段时长检查通过。具体音量见该目录 verification.json；尚未真人听审。

## 宣传片 AI 配音试作：2026-09-28

- 用户回复 go 后按前述推荐执行 edge-tts，使用 zh-CN-XiaoxiaoNeural，已产出[30 秒 AI 配音版](../../build/promo30/python-course-promo-30s-tts.mp4)。原音乐版保留；未将试作选择升级为全课程音色定稿。
- 七句分段合成并测量，对齐已有分镜；音乐在口播时压低，视频流直接复用。脚本及依赖锁定见 [工程 README](../../studio/promo30/README.md)。独立字幕未烧录到视频。
- [验证记录](../../build/promo30/tts/verification.json)：30 秒、900 帧、完整解码通过、视频流哈希一致、所有口播未超出对应时间窗；约 -18 LUFS、真峰值 -5 dBFS。尚未真人听审，未宣称读音或表达效果通过人工验收。

## 协作材料共享：2026-09-28

- 按用户要求移除项目 `.gitignore` 中 `references/imported/**`、其 README/manifest 例外及 `docs/research/evidence/` 规则，允许材料与抓取证据纳入版本管理。
- 单个文件超过 100 MB（100,000,000 字节）不上传 Gitee；本次检查上述两个目录共 72 个文件，无超限文件。Git 忽略规则不能按文件大小自动过滤，后续新增材料提交前需重新检查。
- 本次仅修改本地规则，未提交或推送。项目尚非独立 Git 仓库，上层 `/home/jimmyhuang` 仓库的忽略规则仍影响当前 Git 跟踪。

## 宣传片 AI 配音调研：2026-09-28

- 已读取 promo30 工程与分镜，核对 GitHub 上 edge-tts、Qwen3-TTS、CosyVoice 官方仓库，形成[配音接入建议](../research/promo30-tts-2026-09-28.md)，README 已增加入口。
- 建议按分镜逐句生成、测时长、对齐并混合原创音乐；快速试音候选 edge-tts，语气控制候选 Qwen3-TTS。尚未安装、试音或生成配音成片，未冻结服务选型。

## 30 秒宣传动画：2026-09-28

- 已更新根 AGENTS 与 requirements：课程前段 Motion Canvas、后段真实 Python 实操；本次 animation_step 宣传片单独按用户澄清制作全 Motion Canvas 动画，不含 Python 逐字输入。
- 已产出 [30 秒成片](../../build/promo30/python-course-promo-30s.mp4)：1920×1080、30fps、900帧、H.264/AAC，原创合成轻音乐，无配音。
- 工程：[studio/promo30](../../studio/promo30/README.md)；[分镜](../../course/lessons/promo30/storyboard.md)；[检查证据](../../build/promo30/verification.json)。TypeScript 检查、完整解码、时长与帧数验证通过；抽查 9 个时间点及修订后的尾帧，未声称真人连续审片通过。
- 高星实践检索已完成：官方框架 19,189 stars、官方 examples 1,164 stars 为主要依据；68 stars 社区 skill 未全局安装。详见[研究记录](../research/motion-canvas-skills-2026-09-28.md)。
- 这是宣传样片，不是 2 分钟或 30 分钟正式课程交付；未把本次视觉方案写成用户批准的全课规范。

## 技能下载与审查：2026-09-23

- 按用户要求已下载remotion-best-practices与frontend-design到当前Codex技能目录，已核对文件及显式相对引用；没有安装渲染运行时。
- 已查明manim-video为Hermes自带技能，8月6日文件、8月26日软链接；当前Python没有Manim。发现依赖检查退出码与部分制作指导问题；详见[审查记录](../research/manim-audit-and-skill-download-2026-09-23.md)。

## 技能研究：2026-09-23

- 已完成[技能筛选](../research/skills-animation-2026-09-23.md)：推荐试用Remotion官方技能与frontend-design视觉辅助，本机manim-video为备选；引擎未冻结。
- 已记录最新视觉要求，未安装或渲染；本次B站P18读取失败，未重新观看。

## 最新范围核对：2026-09-19

- 最新交付：[课程大纲建议稿](../../course/catalog.md)，共同主课34课510分钟，每课列出前段动画内容、后段编程环境实操；Pandas校别补充3课45分钟。已按用户最新要求替换旧的自由组合形式；本次未讨论或实施制作技术。
- 新参考MP4时长391.16秒，已按35秒间隔抽帧核对前后段形式，未全程观看或转录。课数、分钟与补充范围仍是建议，尚未获用户确认。

- 已按用户要求更新requirements：保留Matplotlib；排除正则爬虫、词频词云、CSV统计专题和独立综合答题模块。
- 已导入111页复习PPT并核对哈希，提取逐页原生文字；重新核对第15讲Pandas范围。图片代码未全量转录，未开展成片制作。
- 新增[共同范围比较](scope-comparison-2026-09-19.md)；其模块预算已进一步拆成上述34课大纲建议，尚未冻结。
- Pandas基础、TXT与Tkinter如何交付仍是差异项；没有把排除CSV统计解释成用户删除全部Pandas或文件读写。

## 已完成

- 新建独立项目与AGENTS，整理最新需求和冲突来源。
- 读取原大纲任务及“估算Python课程及格学时”的最新用户要求，更新为10h以内方向。
- 导入14份已有大纲、样片脚本、代码、教学材料及截图；与原件哈希一致。
- 复用已有Firecrawl实际抓取B站参考页：成功获得37个分集及其时长。
- 核对参考视频和早期预告的B站元数据、各第一页热门评论；作者动画软件尚未查实。
- 研究Motion Canvas、Remotion、实际视频/课程源码项目、Carpentries和Diátaxis，形成符合本课需求的目录与制作架构提案。

## 尚未完成／不要误报

- 没有获得作者具体动画、录屏、剪辑软件的确定证据。
- 已完成三段MP4的24张粗采样及列表35–46秒逐秒12张加密采样；未完整观看、未转录或验证精确音画同步。
- 已编制10h以内压缩大纲建议稿，尚待用户反馈；9.5h含练习不是当前录播课时口径。
- Motion Canvas 已用于 30 秒宣传片；没有 2 分钟或 30 分钟正式课程新成片。
- Firecrawl Docker共享方案未部署，客户端配置未更改。
- 未部署跨任务自动同步或周报自动化。

## 推荐下一步

1. 根据用户对 30 秒宣传动画的反馈调整视觉与节奏，课程课时仍按已保存的确认状态推进。
2. 后续正式课程样片沿前动画、后真实 Python 实操的规则制作，不把本次宣传片当完整课程验收。

## 本轮交付范围

本次新增 Motion Canvas 宣传动画工程与实际 30 秒成片；尚非完整课程生成系统。早期范围为研究、需求记忆、目录与文档、既有材料导入。自审与文件检查结果见 [review](review-2026-09-15.md)。

## 补充研究：2026-09-15
新增英美欧课程与创作者对标、版权核查、动画技术及三段MP4观察，入口：[补充报告](../research/benchmark-supplement-2026-09-15.md)。新增36张采样帧、4张联系表、媒体哈希与Firecrawl摘存。林粒粒动画软件仍未查实；本轮未开发或生成课程成片。


## Motion Canvas 全课架构研究：2026-09-28

- 新增[510 分钟课程编排与提交建议](../research/motion-canvas-course-architecture-2026-09-28.md)，依据官方 examples、配置、Time Events 与本地样片。
- 明确 255 分钟仅按半数估算，旧 34 课不是新确认；推荐单仓库、多课 project、共享组件、按课交付。
- 实测现有 900 张帧图约 126MB，成片约 1.88MB；识别 build 内定稿音轨/时间表需要持久化，以及 project.meta 与脚本帧率不一致。
- 本轮是研究提案，未迁移目录、修改忽略规则、建立 Docker 或提交推送。


## Git 忽略规则调整：2026-09-28

- 用户同意按课程制作资料分类调整 `.gitignore`：移除 `**/media/` 的整体忽略，build 改为默认忽略加明确例外，允许配音、字幕、时间表、验收 JSON、联系表和海报纳入 Git。
- PNG 帧、MP4 导出、中间混音、运行环境/数据、临时录屏工作区仍忽略；未迁移文件，未更改已有制作脚本。
- build 内发现约 222MB 的 code-server 安装包，已明确排除；后续提交仍需检查单文件 100MB 限制。
- 本轮仅调整规则与记录，不代表已选定所有配音版本，不自动提交或推送。


## 撤销 build 忽略规则：2026-09-28

- 按用户最新要求，删除 `.gitignore` 中整段 build 默认忽略、例外、临时文件及指定大文件规则；替代上方本轮 build 分类忽略方案。其余规则保留。
- 单文件超过 100MB 不上传 Gitee 的既有要求仍在提交前执行；本次未提交或推送。
