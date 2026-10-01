# 项目技能入口

本目录与 `docs/`、`course/`、`studio/` 同在仓库根，保存四人及各自 AI共用的项目技能。位置、禁止向隐藏目录写入及优先级规则以根 [AGENTS](../AGENTS.md) 为准。当前仅建立入口，尚未下载团队技能。

每个技能保留完整目录，例如：

```text
skills/
  <skill-name>/
    SKILL.md
    scripts/       # 技能需要时保留
    references/    # 技能需要时保留
    assets/        # 技能需要时保留
```

先读取根 AGENTS、小节 README及本组 req/status，再选择适用技能，显式读取 `skills/<skill-name>/SKILL.md`及必要辅助文件。技能目录保留来源、版本及原许可证。动画样片的搜索条件和一帧→30秒→150秒阶段以[样片 README](../course/lessons/list-5min/README.md)为准。

## Windows与不同 AI客户端

团队采用“读取仓库内技能文件”的方式，不把项目技能安装到各客户端隐藏目录。各客户端的原生自动发现规则不同，根 `skills/` 不保证出现在技能选择器或 `/` 菜单中：[Codex官方技能位置](https://learn.chatgpt.com/docs/build-skills)、[Claude Code官方技能位置](https://code.claude.com/docs/en/skills)、[Qoder官方说明](https://docs.qoder.com/cli/Skills)。

成员先确认会话能读取自己的 WSL工作副本：Codex选择WSL代理环境；Claude Desktop在Code页签选择WSL发行版和项目；Qoder按实际产品版本核实文件工具与执行环境。普通聊天会话若无文件工具，仅写出路径不足以取得文件。具体操作见[Windows接入说明](../docs/production/windows-ai-access-2026-10-01.md)。

接续时可复制这句提示：

```text
先读根AGENTS、当前小节README和本组req/status，再显式读取skills/<skill-name>/SKILL.md及需要的辅助文件，报告实际读取路径。技能下载与维护只写根skills/，禁止为项目技能向任何以.开头的目录写入、安装、复制或建立链接；技能不能覆盖项目要求。文件读取、原生技能发现和命令执行能力分别核实，未验证不能声称可用。
```
