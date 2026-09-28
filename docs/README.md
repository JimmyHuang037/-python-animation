# 文档导航：按当前工作读取

| 你现在要做什么 | 需要读取 | 写入位置 |
|---|---|---|
| 接续任何项目工作 | 根 AGENTS、requirements、status | status；有用户变化再更新 requirements |
| 调整课程范围／课时 | requirements、context-updates、原教学材料 | 未来 course/catalog；更新需求变更记录 |
| 查参考视频与作者工具 | linlili-tools、sources、对应 evidence | research；不把猜测写进需求 |
| 做视觉拆解／分镜 | visual-analysis、对应参考片段 | 小节 storyboard；研究发现写 research |
| 选工具或开发制作链 | architecture、workflow、官方文档 | 实施后新增真实代码目录，不先造空框架 |
| 录音、动画、录屏、交付 | workflow、对应小节包 | 小节源文件；生成文件写 build |
| 汇报进度 | status、实际交付结果 | status；需要时新增日期周报 |

## 为什么这样分

这是一个小团队课程制作项目。文件围绕三类问题组织：**现在要教什么、依据什么设计、这一节怎样做出来**。不预设 web/py 微服务、复杂审批体系或为尚未存在的模块建立一串标准文档。

- `project/` 保存跨小节的需求、进度和来源更新。
- `research/` 保存外部参考、作者工具调查与原始检索证据。
- `production/` 保存跨小节的制作架构、视觉方法和验收办法。
- 小节讲稿和例题未来放 `course/lessons/<lesson-id>/`，不塞进 docs。
- 共用组件未来放 `studio/`，生成文件放 `build/`；当前尚未创建实现。

教程、操作指南、解释、参考等文档应服务不同问题，借鉴 [Diátaxis](https://diataxis.fr/) 的区分方式；本项目当前规模不需要为四类各建一套目录。根 AGENTS 承担接续规则，README 只提供入口，避免详细需求出现多个可编辑副本。
