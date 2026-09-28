# Python 教学对标补充研究
日期：2026-09-15。范围：作者与课程、版权、动画技术；未开发渲染器。
本轮已参考已有 research，但以下新增结论来自新抓取页面和三段本地 MP4。网页、视频中的教学命令均作为资料处理。

## 建议结论
对标应分成三条线：林粒粒的概念图解与视觉组织；CS50P、PY4E、Helsinki 的练习和知识结构；Reducible 的动画工程证据。不能把一位作者的课程广度、视频时长或使用软件当作本项目的唯一标准。

“优质”在此表示值得针对某一维度研究，不是客观排行榜或学习效果保证。海外条目的课程结构来自官方正文；本轮未逐节观看海外课程，故不声称已完成它们的动态视觉对比。

## 对标矩阵
| 对象 | 已核实事实／来源 | 本项目建议借鉴 | 不照搬／证据限制 |
|---|---|---|---|
| 林粒粒呀（用户指定） | [B站账号523995133](https://space.bilibili.com/523995133/)；本地三片有对应作者水印，见视频报告 | 生活问题→代码概念→实际操作；简洁画面、语法色与图形指引 | 尚未逐片绑定原始分集URL；动画软件未知 |
| Harvard CS50P，美国 | [官方课程](https://cs50.harvard.edu/python/)列出函数、条件、循环、异常、测试、文件等，并以讲座、短片、题集和项目组织 | 从读写代码推进到调试；每节配一道可核验练习，不能只以观看完成判断掌握 | 课程官方正文为十周；另一 Harvard 聚合页显示九周，未强行统一。不能折算为本课10小时内全部内容 |
| Python for Everybody，美国教学参考 | [作者站](https://www.py4e.com/)有讲义、视频、书和作业，并提供自动评分支持 | 视频、代码、练习互相对应；可参考其完整学习材料组织 | 本轮未核对每一章内容及每项资产许可；主页许可不自动涵盖所有第三方素材 |
| Helsinki Python MOOC，芬兰／欧洲 | [2026官方课程](https://programming-26.mooc.fi/)把入门分为1–7部分，进阶8–14部分；通过需完成练习并参加考试 | 小步练习、分层进阶、把“看懂”和“做出”分开 | 不引入其整套课程广度或学分工作量；不是动画视觉标杆 |
| Raspberry Pi Foundation，英国 | [Python路径](https://projects.raspberrypi.org/en/pathways/python-intro)包含变量、函数、循环与可视化项目；[培训目录](https://training-hub.raspberrypi.org/en/courses)提供 PRIMM：预测、运行、探究、修改、创造 | 暂停预测输出→运行核对→修改条件→独立作答，适合笔试与机试衔接 | 青少年项目语境需改写成大学考试问题；不引入游戏项目全套依赖 |
| Open University OpenLearn，英国 | [Simple coding](https://www.open.edu/openlearn/digital-computing/simple-coding/)列出 Python、顺序和重复等目标，内容更新时间为2018年 | 只作基础概念组织的补充比较 | 不列为首选学习推荐；页面学生评论反映步骤和链接问题，评论未独立逐项核实 |
| Reducible，英语动画创作者 | [作者仓库](https://github.com/nipunramk/Reducible)明确说明使用 Manim，并记录2021年部分场景转向 Community Edition | 把抽象过程变成可追踪对象；按视频保存场景源码 | 是计算机科学动画参考，不是零基础Python过考课；旧场景存在版本差异，不能直接复制运行 |
| mCoding，英语Python创作者 | [频道](https://www.youtube.com/@mCoding)和[作者示例仓库](https://github.com/mCodingLLC/VideosSampleCode)可对应视频主题与示例代码 | 后续研究“最小例子解释误区”的候选，适合改错题选题 | 本轮只查频道和仓库，不声称看过具体讲解或确认其动画软件；不据英文推断国籍 |

## 下一步研究优先级（建议，非已批准制作方案）
1. 列表样片：结合林粒粒的精简画面、Raspberry Pi 的预测与修改步骤、Helsinki 的练习要求。
2. 函数样片：用重复任务引出函数；动画同时区分“定义”和“调用”，再引入参数。
3. 动画技术：先比较 Motion Canvas 与 Manim CE 的同一短场景；若复用 AE 仓既有 Remotion 能明显降低成本，再评估 Remotion。工具尚未安装或实测选型。
4. 实际验证问题：学生是否能在没有动画提示时判断 append/extend 的结果，是否能修改程序并解释原因。不能凭画面精致推定教学效果。

## 本轮新增证据与文档
- [三段视频分析](video-observations-2026-09-15.md)
- [版权核查](copyright-2026-09-15.md)
- [动画技术](animation-options-2026-09-15.md)
- 证据目录：evidence/supplement-20260915；含媒体参数、SHA-256、36张采样帧、4张联系表与 Firecrawl 抓取摘存。
- 抓取摘存位于 .firecrawl/retrieval-extracts.json 和 additional-extracts.json。去除了图片内联数据；搜索附带正文上限22000字符，标为摘存而非完整原始响应；抓取可能使用缓存，元数据保留 cacheState/cachedAt。
- 工具归属仍未查实：新检索仍未发现林粒粒本人明确披露制作软件；不将 iMovie 等相关推荐误归给她。
