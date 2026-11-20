---
name: animatic
description: >-
  Produce narrated explainer videos with editable storyboards, progressive
  reveals, continuous animation and MP4 export. Trigger on animatics or
  animated explanations of concepts, code changes or supplied material.
disable-model-invocation: true
---

# Animatic

把解释编排为可修改的分镜，再生成带旁白的视频。内容、画面和时序都保留为源文件。

默认用中文讲解：旁白、字幕、标题与图中标签使用简体中文，技术名称保留原名。
材料和技能说明的语言不改变成片语言。默认配音为火山语音合成 2.0 的
**甜美桃子 2.0**：`zh_female_tianmeitaozi_uranus_bigtts`，资源 `seed-tts-2.0`。
用户明确指定其他语言、音色或已有录音时按其选择执行；服务失败时停止并报告。

## 内容与分镜

沿用用户的受众和用途；信息不足时，从已有材料推断一个小范围样例。
影响内容方向的未知项用普通对话询问。解释代码变更时先核实实际行为与证据，
概念讲解则先确定读者需要理解的机制。视频的长度由讲清楚所需的内容决定。

每个场景围绕一个意思，每段旁白讲清一个完整意群，可包含多句话和多个画面动作。画面承担关系、
顺序或代码定位，旁白解释原因；屏幕上只放理解所需的内容。
根据真实材料编排，保留影响结论的条件与未知项。

已有成片参考时，核对配音来源、显现节奏、连续动作与构图，并将这些观看效果
纳入验收。制作链路通过后，继续检查声音和画面的实际表现。

同一场景通过逐步显现、连线和焦点移动展开，主题改变时再切换场景。
先确定完整构图，再用各段的 `show` 控制显现数量，保留已出现元素的位置。
旁白按完整段落串行合成，通过共享上下文延续讲述状态。保持全片基准语速与语气一致，
用自然重音和停顿形成抑扬顿挫；画面的显现、高亮和切镜跟随字词时间戳。

默认画面采用纸笔工程白板：浅纸底、墨色手绘线条、黄色重点、少量语义 emoji。
阅读 [画面与动作](references/visuals.md)，按内容选择构图和动作；
保留视觉语言的一致性，流程、对照、时间线和代码讲解各用合适的布局。

按 [分镜契约](references/storyboard.md) 写 JSON。
可从 [中文样例](assets/example.zh.json) 起步；样例已指定甜美桃子与中文旁白。
默认渲染器包含标题错落入场、流程逐步显现与连线绘制、焦点滑动、代码行显现、
镜头缓慢推进与场景转场；带字词时间戳时支持逐词字幕和关键词触发的焦点移动。
内容需要其他构图时修改 `player.html`，
保留其 `window.animatic` 契约。

## 本地制作

以下路径相对于本技能目录，执行时换成已解析的绝对路径：

```bash
uv run --no-project scripts/animatic.py doctor
uv run --no-project scripts/animatic.py validate /path/to/storyboard.json
uv run --no-project scripts/prepare_speech.py /path/to/storyboard.json --out /path/to/artifacts/speech
uv run --no-project scripts/animatic.py build /path/to/artifacts/speech/storyboard.json --out /path/to/artifacts/video --fps 30
uv run --no-project scripts/animatic.py verify /path/to/artifacts/video
```

依赖为 `uv`、`ffmpeg`、`ffprobe` 和 Playwright 的 headless Chromium；
Python 依赖由脚本声明。缺少渲染浏览器时执行：

```bash
uv run --no-project --with playwright==1.65.1 python -m playwright install chromium --only-shell
```

默认使用 `prepare_speech.py` 准备甜美桃子配音和字词时间戳，凭据使用环境变量
`DOUBAO_APPID`、`DOUBAO_ACCESS_TOKEN`。这是官方计费接口；合成前说明本次文本量，
沿用已有授权。已确认的音色与音频可直接复用，新选音色先用一句旁白试听。
替代服务的 `tts_command`、已有录音与本机语音配置见
[分镜契约](references/storyboard.md#配音工具)，仅在选择该方案时使用。

需要抑扬顿挫或词与画面同步时，按完整意群写 `narration`，用 `anchors` 安排段内多个
焦点或显现动作。默认沿用统一语气与语速；确需改变演绎时设置 `delivery.instruction`、
`delivery.speed`，段间额外停顿用 `pause_ms`。
参考 [节奏配音样例](assets/example.rhythm.zh.json) 与
[逐段演绎契约](references/storyboard.md#逐段演绎与关键词同步)。
先准备并核对声音，再按实际时间戳编排动作；变更画面复用音频。
准备器在同一次制作中串行共享 `section_id`，完整缓存可离线复用。部分失败、缺段或
旁白顺序变化时使用新目录重做连续旁白；本地音频缓存不会恢复服务端历史。
缓存细节与已有录音的边界见[逐段演绎契约](references/storyboard.md#逐段演绎与关键词同步)。
语气指令影响生成结果，不能保证词语在指定毫秒发声。段尾静音按毫秒配置，
导出时间向上对齐到视频帧；30 fps 的一帧约为 33.3 毫秒。

联网 TTS 会发送段落文本，沿用已选服务和音色。个人声纹使用明确授权的样本或
已有 voice ID；密钥通过环境变量传入。渲染器使用离屏引擎，画面制作在本机完成。
导出的 `player.html` 包含字体和画面样式，离线重建无需其他风格技能。

输出目录使用新目录，或复用由本工具标记的目录；源码与媒体留在任务产物位置。
保留 `storyboard.json`、`player.html`、`timeline.json`、逐段音频与 `captions.srt`。
使用 `--player /path/to/player.html` 重新生成自定义样式；旁白修改后重新制作配音。

## 验收与交付

`verify` 解码成品，检查音视频轨道、时长、分镜时间轴与字幕范围。
再查看实际 MP4 的开头、场景切换和结尾，检查中文排版、裁切、声音与字幕。
同一段内检查显现前后与焦点移动中途的画面，确认内容区域有预期的连续变化。
使用词级同步时，从实际 MP4 核对关键词前后的帧、逐词字幕与音频，并检查往回跳转
后能还原状态。记录时间戳误差与帧精度；声音的自然程度仍需听审。
技术检查与观看检查分别记录；标明未听审或未验证的部分。
再按画面指引自查：当前问题一眼可见，图形关系清楚，emoji 有明确所指，
重点稳定可读，动作与关键词对应，贴纸和线条未挡住内容。

交付可播放的 MP4、可编辑源文件位置和简短复现命令。说明使用的配音方式与
实际验证结果。发布、上传或附加到 PR 需要对应的明确授权。
