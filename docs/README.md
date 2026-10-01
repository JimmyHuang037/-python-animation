# 参考文档导航：按需读取

适用于四位开发者及各自的 AI。共同规则与优先级以根 [AGENTS](../AGENTS.md) 为准。成员日常制作围绕小节 README和本组 req/status；`docs/` 提供跨课程方法、研究与历史，不是每次开工必读的一套规范。全课范围见[课程 README](../course/README.md)，每课细纲暂保留，实际用到再处理。

| 你现在要做什么 | 需要读取 | 写入位置 |
|---|---|---|
| 接续制作任务 | 根 AGENTS、当前小节 README、本组 req/status及任务所需输入 | 执行者更新本组正文和证据；负责人检查共同目标与衔接 |
| 接续“列表”5分钟样片 | [共同样片 README](../course/lessons/list-5min/README.md)、本组 req/status及共享输入 | 两组成员分别创建和维护自己的 req/status；负责人维护共同架构和接口 |
| 派工、交接、协作 | [四人工作流](research/team-workflow-2026-10-01.md)、[任务模板](research/task-template-2026-10-01.md) | 完整任务正文、PR 和交付证据；尚无 Issue 时可用仓库文件或明确授权的聊天任务 |
| 调整课程范围／课时 | [课程 README](../course/README.md)、[来源更新](project/context-updates.md)、当前附件模块汇总 | 按用户决定更新范围与来源；本轮不改每课细纲 |
| 查参考视频与作者工具 | linlili-tools、sources、对应 evidence | research；不把猜测写进需求 |
| 做视觉拆解／分镜 | [视觉分析](production/visual-analysis.md)、对应参考片段 | 小节 storyboard；研究发现写 research |
| 选工具或开发制作链 | [课程架构](production/course-architecture.md)、[小节工作流](production/lesson-workflow.md)、官方文档 | 实施后新增真实代码目录，不先造空框架 |
| Windows AI、WSL 与技能接入 | [Windows 接入说明](production/windows-access.md) | 按实际客户端和本机环境记录验证，不把提案写成已部署 |
| 搜索、保存和使用项目 skill | 根 AGENTS、[skills入口](../skills/README.md)、当前小节与本组需求 | 技能完整目录放根 `skills/`；显式读取，不向隐藏目录安装或复制 |
| 录音、动画、录屏、交付 | [小节工作流](production/lesson-workflow.md)、对应小节包 | 小节源文件；生成文件写 build |
| 汇报进度 | 本组 status、实际交付结果 | 更新本组正文和证据；跨组汇报引用两组结果，不再同步第三份 status |
| 追溯旧需求或机器验证 | [归档索引](archive/archive-index.md)、[来源更新](project/context-updates.md) | 历史正文保留，新的决定记录来源；历史文件不继续维护当前需求或进度 |

## 全部 Markdown 怎样适用

| 文档范围 | 性质与用法 |
|---|---|
| 根 `AGENTS.md`、`course/README.md` | 共用规则与课程范围；根 AGENTS按制作线指向成员文档，用户最新明确要求优先 |
| 四人工作流、任务模板 | 四人共用协作入口；已采用约定与待实施建议分别标注，具体任务按完整正文执行 |
| 根 README、本文、`docker/README.md`、`studio/*/README.md` | 导航与现有工程操作；个人环境、缓存和历史产物不视为全员已有 |
| 根 `skills/` | 团队共用的项目技能与完整辅助资源；与 docs平级，使用规则由根 AGENTS规定，不保证客户端自动发现 |
| `docs/production/*.md` | 跨小节制作方法；当前基线与尚未实现的目标结构分开说明 |
| `docs/research/*.md`（上述协作入口除外） | 日期研究快照；观察与候选建议不覆盖当前需求或实际实现 |
| `docs/project/context-updates.md` | 持续维护用户决定与被替代版本的来源，不复制当前需求或进度 |
| `docs/archive/` | 旧需求、进度、自审、范围比较与机器验证；日期保留在正文或数据中，不作为当前需求、进度或环境入口 |
| `course/catalog.md` | 旧每课细纲建议稿；按用户要求暂不修改，使用时再处理 |
| `course/lessons/**/README.md` | 指定小节/样片的共同范围、接口、成员及读取入口 |
| `course/lessons/**/requirements.md`、`status.md` | 动画与真实 Python 两条制作线分别维护详细需求和实际进度；成员创建，Issue/PR引用，不扩大为所有课程规则 |
| `course/lessons/**/script.md`、`storyboard.md`等 | 指定小节内容与分镜；不扩大为所有课程的时长、音色或风格要求 |
| 根 `animation_step.md`、`python_step.md` | 用户提供的特定样片来源便笺；缺项与后续覆盖以当前需求、分镜和任务正文为准 |
| `references/imported/**/*.md` | 只读来源资料；含复制的 AGENTS、旧细纲、课件摘录，均不承担当前团队指令 |

这是全仓文档分类，不要求每次接续全量读取。修改共用文档可由明确授权的文档任务或 PR 完成，项目负责人统筹合并；不会把普通制作任务自动扩大为重写共同范围和历史资料。

## 为什么这样分

这是一个小团队课程制作项目。文件围绕三类问题组织：**现在要教什么、依据什么设计、这一节怎样做出来**。必要约定聚焦教学代码正确、画面与执行一致、声音字幕同步、制作复现及协作边界，不另建前后端或数据库开发规范。

- `project/` 保存仍在维护的决定来源，不另维护第三套当前 req/status。
- `archive/` 保存已过时的项目记录和历史机器验证，入口见[归档索引](archive/archive-index.md)。
- `research/` 保存外部参考、作者工具调查与原始检索证据。
- `production/` 保存跨小节的制作架构、视觉方法和验收办法。
- 全课范围放 `course/README.md`，小节目标、两组 req/status、讲稿和例题放 `course/lessons/<lesson-id>/`；正式课制作包按任务逐步建立。
- 现有样片工程在 `studio/`，生成文件在 `build/`；共享组件与全课组织方案尚未全部实现。

`project/`、`production/`、`archive/` 的文档与记录文件使用两个小写英文单词，以一个 `-` 连接，例如 `context-updates.md`、`course-architecture.md`、`docker-verification.json`；日期放在正文或数据字段中。本次不改研究快照、课程文件、只读导入材料及固定入口 `README.md`、`AGENTS.md` 的名称。

教程、操作指南、解释、参考等文档应服务不同问题，借鉴 [Diátaxis](https://diataxis.fr/) 的区分方式；本项目当前规模不需要为四类各建一套目录。根 AGENTS 承担接续规则，README 只提供入口，避免详细需求出现多个可编辑副本。
