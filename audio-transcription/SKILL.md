---
name: audio-transcription
description: >-
  Transcribe local audio or video files with local MLX Whisper, Doubao Speech
  ASR 2.0, or both engines for cross-validation. Use whenever the user asks to
  转写、语音识别、听写、提取录音文字、分析面试/会议录音, mentions Whisper or
  豆包录音文件识别模型 2.0, asks for offline/private transcription, or asks two
  models to cross-check a recording. Default to dual recognition unless the
  user explicitly requests online-only or offline-only.
---

# Audio Transcription

把本地音频或视频转成带时间戳文本。支持三种执行值：

- `dual`：本地 MLX Whisper + 豆包录音文件识别模型 2.0。默认。
- `offline`：只用本地 MLX Whisper。
- `online`：只用豆包。

用户所说的“单模型识别”对应 `offline` 或 `online`；“双路识别”对应 `dual`。

## 先决定模式

按以下优先级选择，不要因为凭据缺失而静默改变模式：

1. 用户明确说“只用本地 / 只用 Whisper / 离线 / 不上传”时，选 `offline`。
2. 用户明确说“只用豆包 / 只走在线 / 只走云端”时，选 `online`。
3. 用户明确说“双路 / 两个都跑 / 交叉验证”，或没有指定模式时，选 `dual`。
4. “不上传”优先于其他指令；若同时要求双路，说明在线分支无法执行并改走 `offline`。

`dual` 和 `online` 会把转码后的完整音频上传给豆包。只有以下任一条件成立时才可上传：

- 用户本轮或当前任务中明确要求豆包、在线或双路识别；
- 用户已明确同意把该文件上传到豆包。

仅因本 Skill 默认 `dual`，不等于用户已同意上传。缺少同意时，先说明会上传什么文件、用于什么目的，取得确认后再执行。不要先跑在线分支。

## 运行前检查

1. 确认输入文件存在，且不要改写或删除原文件。
2. 用 `ffprobe` 检查时长、音频流、编码和采样率。
3. `offline` / `dual` 需要：
   - Apple Silicon macOS；
   - 可直接调用的 `mlx_whisper` CLI；建议由 `uv tool` 安装和升级；
   - MLX 可访问 Metal；
   - 首次运行由 CLI 下载约 1.5 GB 的 `mlx-community/whisper-large-v3-turbo`，后续复用 Hugging Face 默认缓存。
4. `online` / `dual` 需要：
   - `ffmpeg`；
   - 新版控制台优先使用环境变量 `DOUBAO_API_KEY`；
   - 旧版控制台兼容 `DOUBAO_APPID` + `DOUBAO_ACCESS_TOKEN`；
   - 已取得云端上传同意。
5. 不打印、不写入凭据；不要把凭据复制进命令、日志、文档或 Skill。

输出目录遵循：

- 用户指定目录时使用该目录；
- 任务属于某个仓库时，可放进该仓库明确的产物目录；
- 否则省略 `--output-dir`，脚本会写入系统临时目录；
- 不要把产物直接放在聚合目录或无关仓库根目录。

## 执行

先定位本 Skill 的绝对路径，记为 `$SKILL_DIR`。输入路径和输出路径始终加引号。

### 默认：双路识别

取得上传同意后运行：

```bash
python3 "$SKILL_DIR/scripts/transcribe.py" \
  "<input>" \
  --mode dual \
  --online-consent \
  --output-dir "<output-dir>"
```

脚本并行启动两个独立分支；任一分支失败时保留另一分支已经完成的产物，并在 `manifest.json` 中记录失败。

### 只走本地 Whisper

执行本地分支前，读取 [references/mlx-whisper-cli.md](./references/mlx-whisper-cli.md)。本地识别由官方 `mlx_whisper` CLI 执行；编排脚本只负责参数、产物和双路核验。

CLI 不存在时，交给 `uv tool` 使用默认位置安装：

```bash
uv tool install mlx-whisper
```

不要创建 Skill 专用 venv、模型目录或 Hugging Face 缓存目录。`uv tool` 管理 CLI 环境，`mlx_whisper` 和 Hugging Face Hub 管理默认模型缓存。

```bash
python3 "$SKILL_DIR/scripts/transcribe.py" \
  "<input>" \
  --mode offline \
  --output-dir "<output-dir>"
```

本地默认：

- 模型：`mlx-community/whisper-large-v3-turbo`
- 语言：自动检测
- `condition_on_previous_text=false`，降低长录音中的循环复读和静音幻觉
- 不做说话人分离
- 不传自定义模型路径；通过 Hugging Face repo ID 使用 CLI 默认缓存

用户提供了语言或专有词时，可加：

```bash
--language zh --initial-prompt "产品名、姓名、技术术语"
```

不要自行塞入与本次录音无关的面试公司名或技术词。Prompt 可能诱导误识别。除非用户明确选择其他模型，否则不要下载多个模型。

### 只走豆包

执行在线分支前，读取 [references/doubao-asr-2.0-api.md](./references/doubao-asr-2.0-api.md)。它记录了当前标准版 HTTP API 的鉴权、输入方式、参数、返回字段和错误码；不要凭旧脚本猜 API。

取得上传同意后运行：

```bash
python3 "$SKILL_DIR/scripts/transcribe.py" \
  "<input>" \
  --mode online \
  --online-consent \
  --output-dir "<output-dir>"
```

在线分支使用录音文件识别标准版 HTTP API 和模型 2.0 资源 `volc.seedasr.auc`。本地文件默认先真正转码为 16 kHz、单声道 MP3，再以 `format=mp3` 提交。MP3 不要声明 `codec=raw`；`codec` 只用于文档列出的 raw / opus 编码。严禁把 M4A 原始字节伪装成 MP3。

官方标准版文档当前明确列出 `audio.url`。如果已有外网可访问、格式正确的音频 URL，可加：

```bash
--doubao-audio-url "https://example.com/audio.mp3" --doubao-audio-format mp3
```

该 URL 必须指向与 `<input>` 相同的录音；双路模式下若两者不是同一内容，交叉验证结果无效。

脚本默认的 `audio.data` Base64 路径用于直接处理本地文件：生产接口实测可用，但不在当前标准版字段表中。需要严格遵循公开文档或排查兼容问题时，改用 `--doubao-audio-url`。

默认关闭 `enable_ddc`，保留口语原貌；只有用户要求润色式转写时才使用 `--enable-ddc`，并明确说明文本不再严格逐字。

豆包使用异步 submit/query：

- resource ID：`volc.seedasr.auc`
- 完成状态：`20000000`
- 处理中：`20000001`、`20000002`
- 默认每 5 秒轮询，最长 30 分钟

## 双路核验

双路不是简单地挑较顺的一份。脚本先生成机械对比报告 `cross-validation.md`；之后还要读取两份带时间戳文本，完成以下核验：

1. 检查两路覆盖的起止时间，发现整段缺失、重复或异常长空白。
2. 优先核对姓名、公司名、产品名、英文缩写、数字、百分比、日期和否定词。
3. 将 MLX Whisper 的连续重复、静音区有字、时间戳异常视为疑似幻觉。
4. 将豆包的说话人标签只视为聚类编号；聚类可能把两人拆成三四人，不要擅自绑定真实身份。
5. 两路一致时提高置信度；两路冲突时结合音频上下文判断。无法判断的内容标成 `[存疑 HH:MM:SS]`，不要凭语言流畅度猜。
6. 不要用一条模型的输出作为另一条模型的 Prompt；两路必须独立产生后再比较。

如用户需要一份可读的最终稿，以在线结果的断句和说话人聚类作为结构参考，以两路一致内容为正文；只在有证据时修正。保留原始 JSON 和两份独立文本，确保可追溯。

## 产物

脚本生成：

```text
<output-dir>/
├── manifest.json
├── offline/
│   ├── raw.json
│   └── transcript.txt
├── online/
│   ├── raw.json
│   └── transcript.txt
└── cross-validation.md
```

单模型模式只生成对应分支，不生成交叉验证报告。

最终回复至少包含：

- 实际模式：`dual` / `offline` / `online`
- 每个分支是否成功
- 产物目录
- 双路时最重要的差异和存疑点
- 是否启用了 DDC
- 未完成原因，例如凭据、Metal、网络或 API 超时

不要把完整转写直接粘贴进聊天，除非用户明确要求查看。

## 常见失败

- `mlx_whisper CLI is missing`：运行 `uv tool install mlx-whisper`，不要自建 venv。
- MLX / Metal 初始化失败：说明当前宿主不能执行本地模型；不要擅自改走在线。
- 豆包凭据缺失：列出缺失的环境变量；不要询问或回显密钥值。
- 豆包超时：保留任务 ID、非敏感状态码和已有本地产物，可稍后重试查询。
- 音频格式异常：先用 `ffprobe` 确认；在线分支仍须转成真实 MP3。
- 说话人数异常：保留聚类标签并注明不可靠，不要人工伪造 speaker。
