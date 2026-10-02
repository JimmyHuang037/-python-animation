---
name: ide-lesson-video
description: 制作或修改 IDE 风格的 Python 分步教学视频：中文旁白与逐字输入同步开始，带可选红色重点椭圆、贴近代码的气泡注释、准确光标、连续机械键盘音效、运行点击和真实输出。
---

# IDE 分步教学视频

默认继承本次确认的流程与样式；用户的新要求优先。完整制作流程见 [IDE-workflow.md](references/IDE-workflow.md)，课程 JSON 见 [IDE-lesson-format.md](references/IDE-lesson-format.md)。

## 新对话快速恢复

新对话接手本项目时，先读取本文件和 `references/IDE-workflow.md`，再检查用户最后认可的成片与当前工程。沿用以下已确认约定：复用已有 IDE 容器；旁白与打字同帧开始；默认每字符 0.1 秒；打字结束后先等 1 秒，只有显式 `highlight` 才显示红圈，再等 1 秒进入气泡；气泡固定在代码右侧，连接线首节点落在代码行末尾；气泡完整出现后再点击运行；每段使用连续机械键盘录音；每段代码完成后才运行并展示真实 stdout；最后运行验收脚本并返回成品绝对路径。用户没有明确要求时，不自动画红圈，不重生成已有旁白，不新建 worker/work 容器。

## 默认效果

每段按「旁白与逐字编辑同步开始 → 打字完成后等待 → 红圈（仅在用户明确指定重点时）→ 气泡缓慢浮现 → 鼠标点击运行并显示结果 → 气泡退出、鼠标淡出」执行。旁白与输入之间不留间隔。

- 每字符默认 0.1 秒，30 fps 时为 3 帧；总时长随内容变化。
- 保留上一段代码，仅模拟本段必要编辑；段首即开始旁白和首个编辑事件。
- 气泡注释写在课程 JSON 的 `stages[].annotations` 中，固定在编辑器右侧近距离栏；连接线首节点定位到所指向代码行的实际末尾，不依赖红圈范围。
- 气泡可以单独存在。只有 annotation 显式提供非空 `highlight` 时才绘制红色椭圆；没有明确重点时不要自动圈选。
- 打字结束后默认等待 1 秒显示红圈（若有），再等待 1 秒开始气泡；气泡以颜色渐变、透明度、位移、缩放和轻微模糊完成约 1.4 秒进入，完整出现后等待约 0.4 秒再点击运行。
- 气泡退出采用渐隐、位移、缩放、模糊和连接线延迟收回的组合动画，通常在本段结束前 1.2 秒开始。
- 打字期间使用一段真实、连续的机械键盘录音；按每段打字时长截取连续片段，不为每个字符单独合成或拼接音效。通过顶层 `typing_sound` 调整开关、音量和素材起点。
- 默认阿里百炼 Ethan 中文男声。自带配音只对应示例文本，换内容须准备新配音。
- 深色圆角编辑器、青色强调、字符串绿色、运算符和函数蓝色、独立终端。
- 点击后结果在点击帧出现；指针淡出约 1.2 秒，每段重复。
- 光标、红色椭圆和语法高亮共用同一字体和完整前缀宽度计算。
- 不加“等待讲解完成再写这段代码”等提示文字。

## 使用流程

1. 首次制作或接手项目，读 [完整开发流程](references/IDE-workflow.md)。
2. 创建新课时，读 [配置说明](references/IDE-lesson-format.md)，复制 `assets/list-demo/` 后换源码、讲解文字、WAV 和注释。
3. 在目标环境设置 `IDE_VIDEO_CODE_FONT` 与 `IDE_VIDEO_UI_FONT`，再运行 `scripts/render_lesson.py`。
4. 运行 `scripts/verify_lesson.py --manifest <生成的 manifest 路径>`，检查实际成片、音频和截图拼图；最终 MP4 音轨必须与经响度处理的混音一致，不能仅凭中间 WAV 判定声音通过。
5. 把成品放到 `<输出目录>`；技能目录只保留源文件和小型示例资产。

## 环境与真实性

- 用户要求既有 IDE 容器时，先识别容器和挂载并复用，不自行新建 worker/work 容器。
- 当前实现是 Pillow 绘图与 FFmpeg 编码，源码单独真实执行；不能称为实时 IDE 录屏。
- 源码验证支持本机 Python 或指定的已运行 Docker 容器；容器失败时不偷偷切换。
- 不保存对话、API 密钥或凭据文件。已有配音缓存不再次请求 API。
- 默认固定 1920×1080，最多 8 行代码、3 行输出；超限先拆段或调整布局，不裁切文字。
- Linux 侧必须显式设置 `IDE_VIDEO_CODE_FONT` 和 `IDE_VIDEO_UI_FONT`；未设置或路径无效时脚本直接失败，不自动回退到系统字体。

## 快速复现

自带三段列表源码、Ethan WAV 和连续机械键盘 WAV，可离线复现，无须 API 密钥。依赖版本锁定在 `scripts/requirements.txt`。

~~~bash
export IDE_VIDEO_CODE_FONT='<代码字体文件>'
export IDE_VIDEO_UI_FONT='<界面字体文件>'
python3 scripts/render_lesson.py \
  --lesson assets/list-demo/lesson.json \
  --output '<输出目录>/list-demo.mp4'
python3 scripts/verify_lesson.py \
  --manifest '<输出目录>/list-demo.manifest.json'
~~~

`--runtime-dir` 可指向已安装依赖目录；`--preflight` 只执行源码、测量音频、检查编辑和布局，不编码。

## 交付限制

技能目录不应包含 `__pycache__/`、`*.pyc`、`.venv/`、`node_modules/`、中间帧或临时 MP4。视频、音频和大图片交付前逐个检查，单文件不得超过 100 MB。验证记录必须写明真实执行结果；未执行的项目写“未执行”。
