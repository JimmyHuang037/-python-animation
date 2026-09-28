# Motion Canvas 技能与高星实践核验

检索日期：2026-09-28。通过 GitHub REST API 实时读取星数，快照见 motion-canvas-github-2026-09-28.json。当前 GitHub 插件没有暴露可调用能力，使用 GitHub 公开 API、原始文件和网页检索。

| 来源 | Stars | 类型与结论 |
| --- | ---: | --- |
| [motion-canvas/motion-canvas](https://github.com/motion-canvas/motion-canvas) | 19,189 | 官方框架，含文档及示例；本次主要技术依据 |
| [motion-canvas/examples](https://github.com/motion-canvas/examples) | 1,164 | 官方完整动画案例；本次主要实践依据 |
| [VideoZero/skills](https://github.com/VideoZero/skills/blob/main/motion-canvas/SKILL.md) | 68 | 社区专用 skill；已阅读，用户认为星数过少，因此不作为主要依据，未全局安装 |
| [Vincentwei1021/anything2explainer](https://github.com/Vincentwei1021/anything2explainer) | 2,120 | 较高星动画 skill，但使用 Remotion，不适用于本次指定 Motion Canvas 的实现 |

检索包括 GitHub 仓库关键词 motion canvas skill、motion-canvas、motion canvas animation examples，按 stars 降序；并检查 skills.sh。npx skills find 的网络请求未完成，已停止，未将其当作有效检索结果。本次未发现比上述官方示例更适合、且高星的专用 Motion Canvas skill；这不表示穷尽所有仓库。

已读主要来源：
- https://motioncanvas.io/docs/quickstart/
- https://motioncanvas.io/docs/rendering/
- https://github.com/motion-canvas/examples/blob/master/README.md
- https://github.com/motion-canvas/examples/blob/master/examples/motion-canvas/src/scenes/signalsCode.tsx
- https://github.com/motion-canvas/examples/blob/master/examples/logo/src/scenes/logo.tsx

采用的实践：使用原生节点与场景；signals 驱动状态和位置联动；生成器管理固定时长；中文字体现实装载后再渲染；分帧导出、随后编码；保留源工程与锁文件。未复制官方成片或将官方旧版 CodeBlock 直接套入新版项目。

本次导出：Motion Canvas Renderer + 本地 CaptureExporter，Playwright 接收帧，FFmpeg 合成 MP4。全部视觉由 Motion Canvas 生成，FFmpeg 只负责编码与音轨合成。服务仅绑定 WSL 回环地址。
