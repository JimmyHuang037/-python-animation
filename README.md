# python-animation

为大一学生制作 Python 过考录播课程：用动画解释执行过程，用代码演示连接真实操作，用题目检验迁移。项目已进入制作链实施与样片阶段；当前内容与建议时长按附件模块汇总，合计 510 分钟（8.5 小时），每课细纲暂保留。

## 先看这里

- [项目记忆](AGENTS.md)：新任务在这个目录开始，先读这里。
- [课程范围](course/README.md)：当前模块预算、内容边界与学校材料。
- [“列表”5分钟样片：架构与成员入口](course/lessons/list-5min/README.md)：当前里程碑、两份需求/两份进度的维护分工及衔接约定。
- [项目 skills](skills/README.md)：统一放根目录，与 docs平级；Codex、Qoder和Claude Desktop均显式读取所用技能，不安装到隐藏目录。
- [四人工作流](docs/research/team-workflow-2026-10-01.md)、[任务与 AI 交接模板](docs/research/task-template-2026-10-01.md)：项目负责人兼 DevOps、两位 Canvas、一位 IDE；共用规则适用于四人及各自 AI。
- [作者工具调查](docs/research/linlili-tools.md)：查到什么、哪些猜测排除、哪些还未知。
- [架构建议](docs/production/course-architecture.md)：每小节制作包＋共享动画组件＋独立音轨时间轴。
- [制作与验收](docs/production/lesson-workflow.md)、[视觉研究](docs/production/visual-analysis.md)。
- [文档导航](docs/README.md)、[研究来源](docs/research/sources.md)。

## 两条制作线怎样接续

项目负责人维护共同目标、架构、跨组接口与验收关系。两组成员分别创建和维护自己的 requirements/status，需求与进度直接查看本组正文；不再维护第三套项目 req/status。

| 制作线 | 本样片成员 | 成员要创建、维护的文件 |
|---|---|---|
| 前段动画 | Soraya、余羿鸿 | `course/lessons/list-5min/animation/requirements.md`、`status.md` |
| 后段真实 Python 演示 | 王旭辉 | `course/lessons/list-5min/python-demo/requirements.md`、`status.md` |

当前四份成员文档尚未建立。第一次接续由本组成员根据[样片 README](course/lessons/list-5min/README.md)创建；两位动画成员维护同一组正文并自行安排主维护人。Issue/PR链接这些文档和产物证据，避免又留一套独立进度。`docs/` 保存共用制作方法、研究和历史，按本次需要查阅；项目不另建前后端或数据库代码规范。

让各自 AI先读根 `AGENTS.md`，再按制作线读取样片 README、本组 requirements/status和共享输入。客户端的自动加载行为须实测；未确认时，把下面这句话放入客户端项目规则或任务开头：

```text
开始工作先读取仓库根 AGENTS.md，再按其指引读取我所属制作线的 README、requirements.md、status.md与共享输入；报告实际读取的文件。缺少本组文档时，由本组任务先创建，只记录已知要求与真实进度。
需要技能时，再读取根 skills/<skill-name>/SKILL.md及必要辅助文件；下载和维护均放根 skills/，禁止为项目技能向 .codex、.agents、.qoder、.lingma、.claude等隐藏目录写入、安装、复制或建立链接。技能不能覆盖项目要求，不把文件可读写成客户端自动发现。
```

## 已有资料与产物

- **课程资料：**[导入索引](references/imported/README.md)列出历史大纲、课件、试题和参考截图；原件保留作依据，不代表当前课程定稿。
- **当前大纲：**[附件只读副本](references/imported/current-outline/Python课程大纲.docx)的模块汇总表；[旧每课细纲建议稿](course/catalog.md)暂不改，等实际使用再处理，不据此冻结34课或逐课分钟。
- **动画样片：**[Motion Canvas 源工程](studio/promo30/README.md)及 30 秒宣传片版本：[无配音](build/promo30/python-course-promo-30s.mp4)、[云希男声](build/promo30/python-course-promo-30s-tts-male.mp4)、[Qwen Ethan](build/promo30/python-course-promo-30s-qwen-ethan.mp4)。它们是宣传样片，不是正式课程。
- **代码实操样片：**[列表五行代码 IDE 演示](build/list-demo/shopping-list-yunxi.mp4)，对应[制作工程](studio/list-demo/README.md)；实际输入、保存并运行 Python。
- **制作环境：**[Linux Docker 工作台](docker/README.md)包含 Motion Canvas、真实 Python IDE 与录制流程。

以上成片链接是仓库相对位置的历史产物入口，克隆后可能尚无对应生成文件。团队交接还需约定可取得的地址、输入版本和哈希；共享产物存储尚未落实。

## 环境与样片记录

2026-09-28 原开发机和指定测试机曾验证 Motion Canvas 与真实 Python IDE 的 Docker 工作台；2026-09-29 另有两台成员机器的环境记录。原开发机的端口与 SSH 隧道只属于当时配置，不代表其他成员已安装或当前在线。四人从各自 WSL 仓库使用 `./docker/course`，以本机实际状态为准。

已制作 30 秒 Motion Canvas 宣传片，以及约 40 秒的列表代码 IDE 实操样片；这不代表完整课程已完成。启动、端口、SSH 转发和制作命令见 [Linux Docker 工作台](docker/README.md)，当时的验证过程见[历史进度](docs/archive/project-status.md)。Firecrawl 仍复用云 API，未部署本地服务。

旧[项目需求记录](docs/archive/project-requirements.md)与[历史进度](docs/archive/project-status.md)已归档，用于追溯来源和既有产物；新的课程范围维护在课程 README，制作进度维护在两组 status。
