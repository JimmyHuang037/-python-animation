# 可修改工程与复现

## 环境与路径

全部命令在Linux Docker内执行。依赖：Node 20+、Python 3.11+、FFmpeg/ffprobe、Noto Sans CJK SC字体及Playwright Chromium。Node依赖锁定在package-lock.json，Python依赖在requirements.txt。复用现有环境，不修改Dockerfile、Compose或容器启动脚本。

9042工作区是/workspace/python-animation。同一持久卷在制作容器vehicle-sample-dev中只读挂载于/repo。制作容器已有所需运行环境；9042 IDE容器目前没有Node/FFmpeg。不要在只读/repo中安装依赖或导出。

本机可在制作容器内复制到已有可写绑定目录/project/reproduce-current-v2。例：

```bash
docker exec vehicle-sample-dev python -c "from pathlib import Path; import shutil; src=Path('/repo/python-animation/course/lessons/vehicle sample'); dst=Path('/project/reproduce-current-v2'); assert not dst.exists(), 'Choose a fresh directory'; shutil.copytree(src,dst)"
docker exec -it -w /project/reproduce-current-v2/engineering vehicle-sample-dev bash
```

这只建立本任务的复现副本，不覆盖已有目录。复制后IDE中的后续编辑不会自动同步到副本；核验新编辑版本时选择新的复现目录重新复制。跨机器使用已有Docker环境，将小节放在可写持久挂载目录，进入engineering执行下列命令即可，脚本不依赖个人宿主路径。

## 安装与预览（以下在容器内）

```bash
npm ci --no-audit --no-fund
python -m pip install -r requirements.txt
npx playwright install chromium
npm run check
npm run build
npm run serve
```

预览服务容器内默认端口9031。占用时可用npm run serve -- --port 9033，并在渲染时同步RENDER_URL。宿主访问取决于已有映射，不把容器端口当作已发布端口；9042仍为IDE入口。

## 修改与声音

车型：../assets/{maybach,rolls,mercedes}.svg。动作：src/full-v1.tsx。旁白修改时同步../audio/full-v1/cues.json、src/full-cues.ts和同版文字副本src/full-cues.json。

原始MP3和WAV已保存，不需要重新请求TTS才能播放或导出。仅修改配音时运行：

```bash
python generate-full-voice.py
python make-audio-full-v1.py
```

配音生成需要网络，已有片段默认跳过。重新生成某段时先另存其MP3，再移除对应cue的source_duration缓存字段。音频合成更新当前工程副本的WAV、SRT和时序记录，应在属于自己的可写副本中执行。实际成片使用云希+10%，脚本检查每段时间预算。

## 导出

在一个容器终端保持预览服务；另一终端进入同一engineering目录：

```bash
node capture.mjs
python export-video.py
python verify-video.py
```

默认输出../intermediate/full-v2-frames/和../outputs/vehicle-list-150s-v2.mp4。capture要求帧目录为空，export拒绝覆盖已有MP4。重复导出时使用新的FRAMES_DIR，并指定export-video.py的--frames和--output。源图可能包含末尾额外帧；FFmpeg按150秒编码4500帧。

最小画面验证：

```bash
RENDER_FROM=79 RENDER_TO=79.03333333333333 FRAMES_DIR=../validation/new-frame node capture.mjs
```

RENDER_URL默认http://127.0.0.1:9031/full-v1.html；CHROMIUM_PATH可指定浏览器。短区间仅核对画面，不用于默认150秒全片导出。检查已有成片可执行python verify-video.py <MP4绝对路径>，只读取原片、打印结果。

## 实际检查与限制

已npm ci安装锁定依赖、通过类型检查与构建，导出79秒处2个源帧并查看第一帧；场景、车型、字幕及原混音哈希与原制作文件相同。未在整理过程中重复渲染4500帧。完整实时播放与主观试听仍待验证，不能将迁移检查写成全片主观验收通过。
