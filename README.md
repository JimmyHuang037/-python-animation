# python-animation

为大一学生制作 Python 过考录播课程：用动画解释执行过程，用代码演示连接真实操作，用题目检验迁移。项目已进入制作链实施与样片阶段；课程范围和完整课时仍在整理。

## 先看这里

- [项目记忆](AGENTS.md)：新任务在这个目录开始，先读这里。
- [当前需求](docs/project/requirements.md)：最新时长方向、课程范围、职责、样片和截止时间。
- [当前进度](docs/project/status.md)：已完成、未完成与下一步。
- [作者工具调查](docs/research/linlili-tools.md)：查到什么、哪些猜测排除、哪些还未知。
- [架构建议](docs/production/architecture.md)：每小节制作包＋共享动画组件＋独立音轨时间轴。
- [制作与验收](docs/production/workflow.md)、[视觉研究](docs/production/visual-analysis.md)。
- [文档导航](docs/README.md)、[研究来源](docs/research/sources.md)。

## 已有资料与产物

- **课程资料：**[导入索引](references/imported/README.md)列出历史大纲、课件、试题和参考截图；原件保留作依据，不代表当前课程定稿。
- **课程编排：**[34 课、510 分钟共同主课建议稿](course/catalog.md)，另含 Pandas 校别补充建议；课数、分钟数和补充范围尚未定稿。
- **动画样片：**[Motion Canvas 源工程](studio/promo30/README.md)及 30 秒宣传片版本：[无配音](build/promo30/python-course-promo-30s.mp4)、[云希男声](build/promo30/python-course-promo-30s-tts-male.mp4)、[Qwen Ethan](build/promo30/python-course-promo-30s-qwen-ethan.mp4)。它们是宣传样片，不是正式课程。
- **代码实操样片：**[列表五行代码 IDE 演示](build/list-demo/shopping-list-yunxi.mp4)，对应[制作工程](studio/list-demo/README.md)；实际输入、保存并运行 Python。
- **制作环境：**[Linux Docker 工作台](docker/README.md)包含 Motion Canvas、真实 Python IDE 与录制流程。

## 运行状态

截至 2026-09-28，Motion Canvas 与真实 Python IDE 的 Docker 工作台已搭建。WSL 本机和指定 Ubuntu 测试机上的 `motion`、`ide` 容器均报告 healthy；WSL 用户级测试机隧道服务 active 且 enabled。当前本机容器使用回环端口 `29030/29042`，测试机容器使用 `9030/9042`。

已制作 30 秒 Motion Canvas 宣传片，以及约 40 秒的列表代码 IDE 实操样片；这不代表完整课程已完成。启动、端口、SSH 转发和制作命令见 [Linux Docker 工作台](docker/README.md)，详细进度与验证记录见[当前进度](docs/project/status.md)。Firecrawl 仍复用云 API，未部署本地服务。
