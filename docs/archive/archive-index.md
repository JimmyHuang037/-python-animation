# 过时文档与历史证据索引

整理日期：2026-10-01。此目录保存已经被当前课程入口替代的项目文档，以及指定机器、指定时段的验证证据。历史正文、机器记录、日期与数据保留；链接按新位置调整，不继续维护当前需求或进度。

当前规则见根 [AGENTS](../../AGENTS.md)，课程范围见[课程 README](../../course/README.md)，当前里程碑见[“列表”5分钟样片](../../course/lessons/list-5min/README.md)。新的决定来源仍写入 [context-updates](../project/context-updates.md)；仍有效的跨小节方法在 `docs/production/`，见[文档导航](../README.md)。

| 归档文件 | 原位置 | 归档原因与日期 |
|---|---|---|
| [project-requirements.md](project-requirements.md) | `docs/project/requirements.md` | 全课范围已转入课程 README，制作需求由两组成员维护；正文更新至2026-10-01 |
| [project-status.md](project-status.md) | `docs/project/status.md` | 制作进度由两组成员维护；保留原有机器、产物及检查记录，正文更新至2026-10-01 |
| [project-review.md](project-review.md) | `docs/project/review-2026-09-15.md` | 2026-09-15 自审快照，不能代表当前实现或用户批准 |
| [scope-comparison.md](scope-comparison.md) | `docs/project/scope-comparison-2026-09-19.md` | 2026-09-19 范围和课时建议，已被当前 DOCX 模块汇总替代 |
| [docker-verification.json](docker-verification.json) | `docs/production/docker-verification-2026-09-28.json` | 2026-09-28 指定机器及10秒预览验证；不是四台成员电脑或完整课程的验收 |

文件名使用两个小写英文单词，以一个 `-` 连接；原日期保留在正文或 JSON 字段中。原路径列用于追溯，不是现行文件入口。

本次整理前，Git 索引中的 `docs/project/status.md` 已有未解决合并项，工作区正文没有冲突标记并含双方机器记录。归档保留了该正文，未暂存文件或修改 Git 索引；归档不代表原合并已经解决。

2026-10-01 后续合并修复：用户明确要求解决 Git 合并冲突。执行者为本任务 Codex，审查人为用户（未执行）。逐节核对双方索引版本，确认历史记录均已保留在 `project-status.md`；按现行归档规则暂存该文件及原路径删除，解决原索引冲突。归档正文未改动，其他任务的源码与文档改动保留；本次不创建提交，合并提交仍待完成。
