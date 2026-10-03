# vehicle sample：列表五个操作的150秒概念动画

本目录是当前修正版v2的可修改工程，对应仓库根deliverables/vehicle-list-150s-v2.mp4。车型已修正，只有外层列表使用车库；嵌套小列表使用浅托盘。范围是列表相加、相乘、append、extend、insert，1920×1080、30fps、150秒，中文云希TTS和内嵌中文字幕。

## 修改入口

- engineering/src/full-v1.tsx：全片场景、分层、动作、运镜及状态时序；沿用full-v1文件名，内容已包含v2车型修正。
- engineering/src/full-project-v1.ts：Motion Canvas项目和原版混音入口。
- engineering/src/depth-parts.tsx、cards.tsx、theme.ts：汽车、接触影、标签、画风与中文字体。
- assets/：实际组件引用的原始SVG，含车型、场景与轨道素材。
- audio/full-v1/：35段原始配音、文字时间表、旁白/原始轻节拍/事件音效/最终混音WAV。
- subtitles/full-v1.srt、engineering/src/full-cues.ts：外挂字幕及实际画面字幕。
- director-full-v1.md、script-full-v1.md、requirements.md、status.json：当前导演方案、旁白、需求与批准来源。
- reviews/：教学语义、音频时序、车型修订和检查记录。
- references/：采用的非Remotion技能来源、固定版本和现有许可声明。
- engineering/README.md：安装、预览、导出和验证说明。
- manifest.json：文件清单与SHA256，用于核对传输和交接。

采用用户要求恢复的“新增BGM前v2”原音轨，原片本身的极轻节拍仍在。本工程不包含后来额外生成的BGM或其生成脚本；不是声称原音轨完全没有音乐。

源码、素材和音频通过Linux目录/持久卷保存，制作与验证在Docker Linux中执行。未复制node_modules、构建缓存、中间帧、历史废稿或重复MP4。9042 IDE用于查看和修改代码，不代表它已安装动画渲染依赖。

[查看交付MP4](../../../deliverables/vehicle-list-150s-v2.mp4)

## 验证范围

整理后的工程已执行npm ci、TypeScript检查、Vite构建和79秒代表性画面导出；场景、车型、字幕和原混音与制作成片时的对应文件一致。脚本使用项目相对路径。MP4已验证150秒/4500帧、完整解码及若干关键画面。

工程迁移验证不等于重新渲染整片或完整实时视听；完整播放和主观试听仍待核验。历史检查记录的原视频路径采用制作阶段位置，最终交付位置以本文和status.json为准。
