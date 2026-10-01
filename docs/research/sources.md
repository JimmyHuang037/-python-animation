# 研究来源与用途

> 文档性质：按下述日期保留的历史研究、证据或提案，不是当前开发指令。四位开发者及各自 AI 执行时，以[根 AGENTS](../../AGENTS.md)、[课程范围](../../course/README.md)和[四人工作流](team-workflow-2026-10-01.md)为准；旧建议不覆盖当前约束。

检索日期：2026-09-15。下表记录实际读取过的页面／仓库；“借鉴”是本项目的判断，不表示来源提出了本项目完整架构。

| ID | 来源 | 支持什么 | 不支持什么 |
|---|---|---|---|
| R01 | [林粒粒呀参考视频](https://www.bilibili.com/video/BV1Jgf6YvE8e/) | Firecrawl已读到简介、37个分集和时长；B站公开元数据核对作者 | 没有披露动画制作软件；不是视频画面分析 |
| R02 | [作者早期课程预告](https://www.bilibili.com/video/BV1hf4y1u7CH/) | 公开元数据、首屏热门评论核对 | 观众评价“PPT很棒”不能证明PowerPoint或Keynote |
| R03 | [出版社合作视频](https://www.bilibili.com/video/BV14X4y127MT) | 页面列出林粒粒呀担任视频制作 | 不证明具体动画、录屏、剪辑软件 |
| R04 | [Motion Canvas Code](https://motioncanvas.io/docs/code/) | 代码高亮、选择与代码变化动画 | 不执行Python，不保证运行结果正确 |
| R05 | [Motion Canvas Time Events](https://motioncanvas.io/docs/time-events/) | 以命名事件对齐口播时间，可在编辑器调整 | 不自动完成双音轨对齐 |
| R06 | [Motion Canvas官方实例](https://github.com/motion-canvas/examples) | 多个独立作品示例；音频建议使用WAV | 不是现成Python过考课程系统 |
| R07 | [Media](https://motioncanvas.io/docs/media/) / [Rendering](https://motioncanvas.io/docs/rendering/) | 音频/图像/视频素材与导出路径 | 不代表WSL2无人值守渲染已验证 |
| R08 | [Remotion Sequence](https://www.remotion.dev/docs/sequence) / [Recorder](https://www.remotion.dev/docs/recorder) | 时间片组合、录制工作流候选 | 不代表当前已有可复用工程或无需适配 |
| R09 | [3Blue1Brown视频源码](https://github.com/3b1b/videos) | 实际视频场景源码，按作品组织的参考 | 数学动画不等于代码课；仓库可读不代表所有素材可复用 |
| R10 | [100 Days of Code Python](https://github.com/CodeWithHarry/100-days-of-code-youtube) | 视频课程对应源码的组织案例 | 不主张其课程范围适合本项目，也非完整动画流水线 |
| R11 | [Carpentries Episode Structure](https://carpentries.github.io/sandpaper-docs/episodes.html) | 教学小节可关联问题、目标、练习、答案与关键点 | 无需引入其整套发布框架 |
| R12 | [OBS录制指南](https://obsproject.com/kb/standard-recording-output-guide) | 真实录屏素材的制作参考 | 录屏不是代码语义验证 |
| R13 | [Diátaxis](https://diataxis.fr/) | 按读者问题区分说明、操作、教程和参考 | 不强制本项目建四套目录 |
| R14 | [Firecrawl本地MCP](https://docs.firecrawl.dev/mcp-server/local) | 现有服务接入能力 | 本轮未部署任何MCP/Docker服务 |

## 原始证据

`evidence/` 内 JSON 保存本次 Firecrawl 检索/抓取和B站公开接口的实际结果，包括时间或请求地址、状态与错误。未保存密钥。B站页面包含推荐和播放器UI，分析时不能把推荐内容归给作者。

研究使用了通用网页搜索、Firecrawl两次关键词搜索及一次参考页抓取、B站两条视频的公开元数据和各一页热门评论。评论检查有边界，没有穷举所有评论或私信作者。

## 排除的错误关联

- [即刻推荐帖](https://m.okjike.com/originalPosts/65e1a53ade5f287348d06d1a)：同帖推荐多个博主，“剪映”段落属于“阿猪不是猪”，不能归给林粒粒呀。
- [视频聚合页](https://tanvibecoding.com/zh/videos)：“Keynote动画制作全流程”对应“马克的技术工作坊”，不是林粒粒呀。
- 作者讲过 [AI做PPT](https://www.bilibili.com/video/BV1KKD5BVEVg/)，只能证明其发布过该主题，不能证明早期Python课程制作工具。

## 素材处理

本轮只研究与归档本地证据，没有从这些项目复制实现代码或把他人视频加入课程成片。若后续需要具体字体、图标、图片、源码或音轨，按该资产明确许可记录来源；公开网页与公开源码的使用边界不能混为一谈。
