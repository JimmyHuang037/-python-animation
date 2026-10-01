# 510 分钟课程的 Motion Canvas 编排与 Git 管理建议

> 文档性质：按下述日期保留的历史研究、证据或提案，不是当前开发指令。四位开发者及各自 AI 执行时，以[根 AGENTS](../../AGENTS.md)、[课程范围](../../course/README.md)和[四人工作流](team-workflow-2026-10-01.md)为准；旧建议不覆盖当前约束。
>
> Docker 样片工作台后续已实施；下文“若采用”、拟建目录与提交矩阵仍为当日提案，不代表当前实际忽略规则。四人当前分工和素材提交要求以共用工作流、具体任务及仓库现行规则为准。

日期：2026-09-28。状态：研究提案，未实施目录迁移、Docker 或自动构建，不代表用户已批准。使用 explore 架构路由，以官方实现和本地文件为依据。

## 范围与现状

课程总计 510 分钟，按用户约一半动画的估算为 255 分钟；各课比例应随教学目标调整。不得将旧版 34 课细纲当作已确认课表。当前 studio/promo30 是 30 秒样片工程，不能视为全课生产链。

本次测量 build/promo30：900 张 PNG 共 125,586,378 字节；原音乐成片 1,881,175 字节。以同样 30fps 与平均帧大小线性外推，255 分钟为 459,000 帧，约 64.05GB PNG。这是容量估算，不是全课性能实测。在线 TTS 的定稿音轨无法保证再次生成完全一致。

## 官方证据

- [官方 examples 仓库](https://github.com/motion-canvas/examples)：一个仓库存放多个视频示例；README 建议制作时用 WAV 以避免 MP3 同步问题。
- [examples package.json](https://github.com/motion-canvas/examples/blob/master/package.json)：npm workspaces 管理多个示例。这是参考结构，不照搬它的旧依赖版本。
- [examples .gitignore](https://github.com/motion-canvas/examples/blob/master/.gitignore)：忽略 node_modules、dist、output。
- [已提交的场景元数据](https://github.com/motion-canvas/examples/blob/master/examples/motion-canvas/src/scenes/signalsCode.meta)：包含 timeEvents 和 seed，说明自动生成的元数据也可能是制作源文件。
- [配置](https://motioncanvas.io/docs/configuration/)：project 可为数组，同一 Vite 服务可选择不同工程；无需每课复制一套依赖。
- [Time Events](https://motioncanvas.io/docs/time-events/)：使用 waitUntil 与编辑器调整口播事件，避免大量硬编码等待时间。
- [Rendering](https://motioncanvas.io/docs/rendering/)：可按范围渲染；预览与正式输出可分别设置帧率和缩放。

## 建议结构

一个 Git 仓库，一套主要 Node 依赖，多课独立 Motion Canvas project，共享组件。

```text
python-animation/
  AGENTS.md
  README.md
  course/
    catalog.yaml                 # 模块、稳定 lesson_id、顺序、时长预算（拟建）
    lessons/<lesson-id>/
      lesson.yaml                # 场景顺序、输入素材、配音版本、责任人（拟建）
      script.md
      storyboard.md
      examples/                  # Python 原码、输入与已核验预期输出
      assets/                    # 选定配音、图片；大素材另存并记清单
      subtitles/                 # 人工校准字幕
  studio/
    package.json                 # 正式迁移后统一依赖
    package-lock.json
    vite.config.ts               # 多 project 入口
    shared/                      # 样式、代码面板、变量/列表视图、强调动作
    lessons/<lesson-id>/
      project.ts
      project.meta
      scenes/*.tsx
      scenes/*.meta
  tools/                         # 代码运行、素材检查、按课渲染、合成
  reports/<lesson-id>/           # 少量发布验收报告与截图
  releases/<version>/manifest.json # 成片地址、源码提交、哈希、时长与音轨版本
  build/<lesson-id>/<variant>/   # 临时帧、缓存、中间音轨、导出成片
```

这是目标结构，不要求立刻创建全部目录。现有 promo30 暂保留，先用一个正式课的 2–3 分钟片段验证结构，再迁移共享部分。Docker 若采用，只需要可重建的制作环境；固定 Node/Python、浏览器、FFmpeg、字体、依赖与镜像版本。每位成员拥有自己的克隆和缓存。

## 课程制作粒度

模块决定内容范围；课是分工、验收和交付单位；场景是动画编辑单位。每课动画可由若干 30–90 秒的教学场景构成，复杂解释可更长，不为了时长硬切。若每课平均 15 分钟，则 510/15=34 个交付单元、每课约 7.5 分钟动画；仅为容量示例，不修改当前大纲。

每课围绕一个目标和同一例子：问题/预测、概念可视化、执行状态、易错点、小结，再进入真实 Python 自动输入与运行录屏。动画内代码展示和真实执行应读取同一 Python 源文件。状态、输出需对照真实运行核验。

跨场景用显式输入或已核验快照，不依赖前一场景的全局可变状态。场景之间保留独立预览能力；跨场景转场仍可能依赖相邻场景，不能把任意分片拼接视为天然无缝。

## 配音与时间轴

先定讲稿，再选定音轨，最后校准事件。用有意义的事件名表示讲解节点。当前建议保留原生 scene.meta 作为编辑器时间事件正文；不要另维护一份可独立编辑的 timing.yaml 与其争夺权威。后续如果引入生成器，须明确哪个文件是输入、哪个是只读生成物。

真人/TTS 的不同版本分别保存音轨、字幕和事件配置；原生共享场景元数据不会自动替你维护多个配音版本，需要小样验证版本装配方案后再批量制作。

## 提交矩阵

| 内容 | Git 策略 |
|---|---|
| 讲稿、分镜、清单、Python 例子、场景 TSX、共享组件 | 提交 |
| project.meta、scene.meta、选定时间事件、人工校准字幕 | 提交 |
| package.json、锁文件、制作脚本、Dockerfile/compose/.dockerignore（建立后） | 提交 |
| 项目必需且可共享的小型图片、字体及许可证、定稿配音 | 选择提交；关注累计体积与变更频率 |
| 大型源素材、原始录屏 | 团队素材存储；Git 保存可获取地址、版本和 SHA-256 |
| node_modules、虚拟环境、缓存、PNG 帧序列、临时混音 | 不提交 |
| 验收 JSON、少量关键截图、发布清单 | 提交到 reports/releases |
| 正式成片 | 团队共享存储/发布附件，Git 记录发布清单；小型演示片可选择提交 |
| 单个超过 100,000,000 字节的文件 | 按用户要求不上传 Gitee；不通过拆分规避 |

小于 100MB 是大小约束，不等于应该提交。Git 历史会累计二进制版本；四人共享必须同时安排素材与交付物的获取方式。未配置可访问的共享存储前，不能宣称项目已完整可复现。Git LFS 不是默认选择，仍需核实主托管平台配额且遵守用户的大文件限制。

## 当前工程需要优先处理的地方

1. build 内选定的 TTS 音轨、时间表、字幕、验收结果应提升到源素材/报告位置，再让脚本读取；本轮只识别问题，未移动。
2. **/media/ 规则过宽，应在正式整理时替换为明确的本地大素材/缓存路径。
3. 当前 project.meta 中渲染 fps 为 60，而样片自定义渲染流程使用 30；正式课程应统一输出入口并核对元数据，避免编辑器与脚本导出不一致。
4. 从真实样片抽取最小共享组件：CodePanel、变量/列表状态、箭头、高亮与主题；不要先搭整套通用动画平台。
5. 四人按课分支负责，一人协调共享组件与发布；素材锁定/版本清单避免多人覆盖同一配音或场景元数据。
6. 先验证一个完整短片段：新克隆获取素材、固定环境、真实输出核验、动画+录屏拼接、字幕和口播对齐；通过后再规模化。
