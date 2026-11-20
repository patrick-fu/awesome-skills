# 分镜与渲染契约

JSON 顶层包含 `version: 1`、`title` 和非空 `scenes`。可设置 `language`
（默认 `zh-CN`）、`voice`、`speech_rate`（本机 `say` 默认每分钟 180 词）。
新分镜默认中文、甜美桃子 2.0，通过 `prepare_speech.py` 准备声音；省略 `voice`
时准备器写入 `zh_female_tianmeitaozi_uranus_bigtts`。其他语言需同时选择适用的音色。

## 配音工具

首选下节的甜美桃子准备流程。明确选择其他配音工具时，`tts_command` 是命令参数数组，
支持 `{text_file}`、`{output}` 和 `{voice}`。例如 Edge：

```json
{
  "voice": "zh-CN-YunxiNeural",
  "tts_command": [
    "uv", "run", "--no-project", "--with", "edge-tts==7.3.1",
    "edge-tts", "--voice", "{voice}", "--file", "{text_file}",
    "--write-media", "{output}"
  ]
}
```

命令直接作为 argv 执行。`{text_file}` 是 UTF-8 旁白文件，`{output}` 是临时
音频输出路径。配置必须包含这两个占位符。声音 ID 由所选工具解释，可以是
标准音色或该服务已创建的个人音色。个人声纹的创建由对应服务处理，
这里负责调用现有声音生成旁白。密钥留在环境变量中。

Edge 会将旁白发送到联网语音服务。已有音频可通过 `audio` 使用。
明确选择本机配音时移除 `tts_command`，把 `voice` 设为 `Tingting`。
旧分镜的 `build` 保留本机语音回退；新任务按首选流程先准备声音。

### 火山语音合成 2.0

默认音色为甜美桃子 2.0；批量准备使用 `scripts/prepare_speech.py`，单段合成可使用
`scripts/volcengine_tts.py`（省略 `--voice` 同样选择甜美桃子）。凭据由环境变量
`DOUBAO_APPID`、`DOUBAO_ACCESS_TOKEN` 提供；这是官方计费接口，按账户额度或
付费规则结算。先说明本次文本量，再按已选音色合成，失败后停止。

```json
{
  "voice": "zh_female_tianmeitaozi_uranus_bigtts",
  "tts_command": [
    "uv", "run", "--no-project", "/absolute/path/to/animatic/scripts/volcengine_tts.py",
    "--voice", "{voice}", "--text-file", "{text_file}", "--output", "{output}"
  ]
}
```

声音 ID 为 `zh_female_tianmeitaozi_uranus_bigtts`，命令中的脚本路径换成已解析的技能安装路径。
接口与资源为 [HTTP Chunked V3](https://docs.volcengine.com/docs/doubao-voice/http-chunked-sse-unidirectional-streaming-v3?lang=zh)
和 `seed-tts-2.0`。

单段试音可对这个脚本使用 `--instruction` 描述语气，`--speed`
设置 0.5–2 倍语速，`--timestamps` 保存字词起止时间。`--format wav` 接收 PCM
并在本地写 WAV，方便后续剪辑。手动串行调用时传入相同的 `--section-id`，每次只提交新段落，
等待上一请求正常结束再继续。批量制作使用下面的准备流程自动管理上下文。

### 逐段演绎与关键词同步

在源分镜中保留默认甜美桃子或显式设置 `voice`。每段 `narration` 是一个完整意群，
可包含多句话，段内画面动作通过 `anchors` 编排。每段可包含：

| 字段 | 内容 |
| --- | --- |
| `delivery.instruction` | 给 TTS 的语气与演绎指令；默认“自然口语，短句讲清因果，重点词稍加重，句尾落稳” |
| `delivery.speed` | 0.5–2 倍语速，默认 1；只在合成该段时生效 |
| `pause_ms` | 段尾追加静音毫秒数；在自然意群边界使用 |
| `anchors` | 关键词字符串，或含 `word`、`occurrence`、`focus`、`show` 的对象 |

`occurrence` 从 1 开始，默认取第一次出现；匹配时忽略标点和空格。
`focus`、`show` 沿用场景索引，在关键词开始发声时触发，持续至下一个动作。
字符串形式只生成时间标记，供自定义渲染器使用。例子：

```json
{
  "narration": "第一次请求，缓存里还没有答案。去数据库，取回来，再存一份。",
  "pause_ms": 480,
  "focus": [],
  "show": 1,
  "anchors": [
    {"word": "请求", "focus": [0]},
    {"word": "缓存", "focus": [1], "show": 2},
    {"word": "数据库", "focus": [2], "show": 3},
    {"word": "取回来", "focus": [1]}
  ]
}
```

运行 `scripts/prepare_speech.py script.json --out speech`，输出可直接构建的
`speech/storyboard.json`。准备器逐段串行调用火山语音合成 2.0，在一次制作内共享
`section_id`；保持基准语速和整体演绎指令一致，必要时再局部覆盖。
服务端历史有轮数与超时限制，连续听感需核对实际声音。准备器保存 WAV、字词 JSON、
请求参数与文件摘要，并生成下列字段；路径均相对于分镜文件：

- `audio`：实际音频。
- `words`：`[{"text": "数据库，", "start": 0.2, "end": 0.8}]`，时间单位为秒，
  相对于该段音频开头；正文标点与空格会恢复，用于画面逐词字幕。
- `cues`：`[{"word": "数据库", "start": 0.2, "end": 0.8, "focus": [2], "show": 3}]`。
  同一时刻的动作按列表顺序应用，省略的视觉字段保持当前值。

关键词沿用服务返回的字词边界；一个词内的字符不能由此获得更细的时刻。
时间戳、指令和语速均需核对实际声音，无法承诺任意词语在指定毫秒发声。
画面在首个达到关键词时刻的视频帧开始变化，随后完成过渡。30 fps 的量化间隔
约为 33.3 毫秒，段尾静音与帧对齐也计入下一段的开始时间。

同一份源分镜重复运行到同一输出目录，完整缓存按请求参数、旁白顺序与文件摘要离线复用。
只修改布局、焦点、关键词或停顿无需重新合成。文字、音色、演绎参数或缓存内容
变化时停止，检查后使用新目录；失败不会自动换服务或重试。
`speech-session.json` 保存上下文 ID 与有序请求摘要。部分失败、缺段或中断后使用新目录
重做这次连续旁白，避免在未知或过期的服务端历史上续写。旧版独立合成缓存需要新目录
才能改用连续上下文；原来已经准备好的分镜仍可直接 `build`。
已有 `audio` 和 `words` 的段落会直接复用，`delivery` 不会改写现成音频。
已有录音不会上传或进入服务端历史，录音与新合成音频的交界需要单独听审。
需要改变声音时，在新的源版本中移除该段 `audio`、`words`、`cues`，重新准备配音。
`build` 对未准备的 `delivery` 或 `anchors` 报错，避免忽略演绎配置。

## 场景

每个场景：

| 字段 | 内容 |
| --- | --- |
| `id` | 唯一的短标识，只含字母、数字、连字符和下划线 |
| `layout` | `title`、`flow` 或 `code` |
| `title` | 画面标题 |
| `text` | 可选的简短补充文案 |
| `items` | `flow` 使用的 2–5 个短标签；可加 emoji 前缀，例如 `"📦 缓存"`，前缀与标签之间留空格 |
| `code` | `code` 使用的多行文本，最多 12 行 |
| `beats` | 非空旁白段落列表 |

每段包含 `narration`，以及可选的 `focus`（要高亮的项目或代码行，统一从 0 开始）。
`show` 指定该段显示前多少个项目或代码行，从 1 开始；焦点必须位于可见范围。
省略时显示全部。后续元素保留原来的布局位置，在对应段落开始时逐步显现。
可用 `audio` 指定相对于分镜文件的音频路径，替代本机语音合成。
`narration` 仍需提供，用于字幕与人工核对；音频内容与文字的一致性由制作者确认。
`pause_ms` 指定段尾追加静音，范围 0–30000 毫秒，默认 350；最终段落长度
向上对齐视频帧。句内停顿优先通过标点与演绎指令组织；需要精确剪辑时保留完整音频及字词边界。

```json
{
  "version": 1,
  "title": "看懂一次变更",
  "scenes": [{
    "id": "path",
    "layout": "flow",
    "title": "请求经过哪里？",
    "items": ["输入", "校验", "结果"],
    "beats": [{
      "narration": "先接收输入。校验通过后，再生成结果。",
      "focus": [0], "show": 1,
      "anchors": [
        {"word": "校验", "focus": [1], "show": 2},
        {"word": "结果", "focus": [2], "show": 3}
      ]
    }]
  }]
}
```

每段实际音频时长加上 `pause_ms`，再向上对齐到视频帧；同一时间轴驱动画面、
旁白、字幕和 MP4。画面字幕在有 `words` 时分页并按字词高亮，否则显示整段。
外部录音或替代 TTS 没有 `words` 时，每段字幕保持在两行内；较长意群先补字词时间，
或按语义边界拆段。这些音频仍按实际时长构建。
SRT 与 MP4 的可选字幕轨道仍以段落为单位。
旁白按语义选择段落边界，段内多个视觉重点通过字词时间戳同步。

## 输出与重建

- `video.mp4`：H.264 / AAC，默认 1280×720、24 帧。
- `storyboard.json`：可修改分镜；外部音频会复制并改写为相对路径。
- `player.html`：可修改的 HTML/CSS/JS 渲染器。
- `timeline.json`：各段的起止时间、音频时长、视觉焦点与帧数。
- `captions.srt`：逐段字幕；同样嵌入 MP4 的可选字幕轨道。
- `audio/`、`frames/`：逐段音频、每段代表画面。
- `manifest.json`：实际制品参数及检查依据。

修改 `storyboard.json` 后，可对原输出目录运行 `build`；通过 `.animatic`
标记识别本工具目录。需要保留多个版本时选择新的输出目录。
提供外部 `audio` 的段落修改旁白后，也要更新对应音频。

## 自定义渲染器

默认画布为 1280×720，整体等比缩放到输出分辨率。渲染器应为自包含 HTML，
使用本地字体；离屏导出期间网络请求被阻止。
默认模板的手写字体由技能自带，构建时以内嵌数据写入 `player.html`。
自定义构图的色彩、字体、emoji 与动作指引见 [画面与动作](visuals.md)。

提供 `window.animatic`，含以下同步方法：

- `load({storyboard, timeline, width})`：装入分镜、段落时间轴和输出宽度。
- `seek(seconds, settled)`：按指定时刻渲染；`settled=true` 使用当前段落的最终动画状态。
- `audit()`：返回错误字符串数组；至少检查文字裁切、舞台溢出和内容缺失。

导出器按时间逐帧调用 `seek`，不使用屏幕录制或墙上时钟决定动画位置。
自定义动画同样从传入时间计算状态，保证重新生成和静态审查一致。
