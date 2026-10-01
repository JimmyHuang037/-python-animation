# Python教学动画技能筛选

> 文档性质：按下述日期保留的历史研究、证据或提案，不是当前开发指令。四位开发者及各自 AI 执行时，以[根 AGENTS](../../AGENTS.md)、[课程范围](../../course/README.md)和[四人工作流](team-workflow-2026-10-01.md)为准；旧建议不覆盖当前约束。
>
> 当前课程动画采用 Motion Canvas；下文 Remotion 优先及引擎候选排序属于旧选型建议。技能安装与实现状态以当前进度和工程为准。

日期：2026-09-23。本轮研究，未安装技能、未渲染视频。

用户参考：https://www.bilibili.com/video/BV1Jgf6YvE8e/?p=18
用户要求：现代简洁、有动效、突出重点。

## 推荐

现成技能优先试用 remotion-best-practices（Remotion官方），辅助 frontend-design（Anthropic官方）。前者负责动画、时间轴、字幕、导出；后者辅助配色、字体、留白和重点层级。Python列表、变量、执行焦点组件仍需编写。frontend-design面向网页，不能直接搬用网页导航、悬停和首页结构。

本机manim-video可作为算法图解备选，已读SKILL.md，未验证渲染依赖。旧研究的Motion Canvas仍保留为引擎候选；本次按现成技能可用性推荐，不代表冻结或实测通过了引擎。

## 核验来源

- https://www.remotion.dev/docs/ai/skills ：官方技能说明。
- https://github.com/remotion-dev/skills/blob/main/skills/remotion-best-practices/SKILL.md ：已读，路由创建、排版、字幕、渲染等资料。
- https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md ：已读，强调有目的的设计与克制动效。
- https://skills.sh/remotion-dev/skills/remotion-best-practices ：页面约537.6K安装、4.7K仓库星标。
- https://skills.sh/anthropics/skills/frontend-design ：页面约914.1K安装、177.6K仓库星标。
- https://www.skills.sh/apoorvlathey/motion-canvas-skills/motion-canvas ：社区技能，搜索快照134安装、1仓库星标；不作为首选，不代表引擎能力弱。

数字为检索页面快照，可能缓存并会变化，不是质量保证。本机manim-video未核验公开安装量。

## 视觉建议

固定代码、对象状态、输出、字幕区域；大字号和留白；一次突出一条代码及对应变化。append移到末端，pop移出并显示返回值，循环移动执行指针。保留既定的前段动画、后段真实编程环境演示。建议append/extend做60–90秒对照样片，检查中文、语义、重点与口播节奏后再定工具。

## 限制

本次B站直接读取失败，未重新观看P18，也未确认P18与历史本地三段视频的对应关系。已有抽帧观察见video-observations-2026-09-15.md。作者软件仍未知。npx skills find的manim和motion canvas查询持续未输出，已结束进程；推荐依据为网页、官方正文与本地文件，不声称CLI查询成功。

后续安装命令（本轮未执行）：

```bash
npx skills add remotion-dev/skills --skill remotion-best-practices
npx skills add anthropics/skills --skill frontend-design
```
