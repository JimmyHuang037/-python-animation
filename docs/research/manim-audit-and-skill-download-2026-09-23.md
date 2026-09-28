# Manim技能审查及两项技能下载

日期：2026-09-23。用户要求仔细核查manim-video来源，并下载Remotion与Frontend Design技能。

## 来源和时间证据

- 真实路径：`/home/jimmyhuang/.hermes/skills/creative/manim-video`。
- Codex入口：`/home/jimmyhuang/.codex-wsl/skills/01-p1-hermes`是指向`/home/jimmyhuang/.hermes/skills`的软链接；链接birth/mtime为2026-08-26 17:26:54（北京时间）。
- SKILL.md的birth为2026-08-06 11:36:45，mtime为2026-08-06 11:31:20。时间戳只能证明当前文件及链接记录，不能直接确定谁执行了安装。
- Hermes `.bundled_manifest`包含manim-video；技能目录共17个文件，与`/home/jimmyhuang/.hermes/hermes-agent/skills/creative/manim-video`逐文件字节一致，无差异。
- SKILL.md SHA256：3459a6af999f0c9bfd61eb867836c8de90b33253493eb1b6aa4118d82fd320f4。
- Hermes `.usage.json`显示created_at=2026-08-20T02:24:41.308521+00:00、use_count=0、view_count=0、last_used_at=null、patch_count=0。该日期是使用统计记录日期，不是技能首次安装时间；统计不覆盖所有外部代理的读取。
- 上游存在对应文件：https://github.com/NousResearch/hermes-agent/blob/main/skills/creative/manim-video/SKILL.md 。本轮未将最新远端全文与本地旧版做字节比较。

结论：这是Hermes自带技能，经整套软链接进入Codex可发现范围，不是本轮新增，也没有证据说明用户曾专门配置过Manim视频环境。未确定具体安装操作人或原始命令。

## 环境检查

已审读并执行其setup.sh，脚本只检查依赖，不安装或修改环境。

- 当前Python为3.12.3，import manim失败；python3 -m pip show manim显示未安装；PATH没有manim。
- pdflatex和ffmpeg存在。
- 结论仅限当前终端Python环境，未全盘扫描其他虚拟环境、容器或Windows。

## 内容审查

1. setup.sh在发现缺失依赖后仍执行最后的echo，实际退出码为0，不能用退出码判断环境就绪。
2. SKILL.md要求“一次渲染即完美、无需修订”，但流程又要求预览迭代；不可把该宣称当质量保证。
3. 要求每个场景改变主色与布局，不适合课程长期保持代码、变量与输出位置和语义颜色；只能按需采用。
4. 所有文字必须等宽字体、Pango在所有字号均无法正确排比例字体的断言缺少可复现实证；不能据此限制中文教学标题和正文字体。
5. “Never Animate Non-Added Mobjects”标题及“must add first”注释容易误导：官方Create示例直接self.play(Create(Square()))，无需预先self.add。https://docs.manim.community/en/stable/reference/manim.animation.creation.Create.html
6. 渲染时间表没有本机基准支撑，不能承诺秒数。

只读审查SKILL.md、README、setup脚本，核对全目录一致性并扫描参考文件的外联/执行模式；未发现实际setup脚本联网、提权、删除或读取凭据行为。这不是所有参考示例的运行验证。未修改或删除原技能。

## 已下载

通过skill-installer脚本从两个官方GitHub仓库下载到当前CODEX_HOME技能目录：

- remotion-dev/skills → `/home/jimmyhuang/.codex-wsl/skills/remotion-best-practices`，137个文件，1,133,214字节，SKILL声明版本4.0.527。
- anthropics/skills → `/home/jimmyhuang/.codex-wsl/skills/frontend-design`，2个文件，19,564字节，包含LICENSE.txt。

两个SKILL.md均存在且具有name/description；检查所有Markdown中的显式./相对链接，没有缺失目标。下载不是渲染依赖安装；未创建视频工程、未安装Manim或Remotion运行时。本轮未做完整新技能安全审计。

来源和逐文件SHA256另存skills-download-manifest-2026-09-23.json。通过main下载，未锁定上游Git提交；哈希记录本次实际下载内容。
