# 豆包录音文件识别模型 2.0：标准版 HTTP API

用于维护或排查本 Skill 的豆包在线分支。执行普通转写时不必把整份文档复述给用户。

## 文档基线

- 官方文档：[录音文件识别标准版 HTTP](https://docs.volcengine.com/docs/6561/1354868?lang=zh)
- 文档 ID：`1354868`
- 官方页面更新时间：`2026-06-26T08:23:54Z`
- 本 Reference 核对日期：`2026-07-25`
- 本 Skill 目标：标准版 HTTP、豆包录音文件识别模型 2.0

不要混用以下产品：

| 产品 | 接口形态 | Resource ID |
|---|---|---|
| 标准版模型 2.0，本 Skill 使用 | `/api/v3/auc/bigmodel/submit` + `/query` | `volc.seedasr.auc` |
| 标准版模型 1.0 | 同上 | `volc.bigasr.auc` |
| [极速版](https://www.volcengine.com/docs/6561/1631584?lang=zh) | `/api/v3/auc/bigmodel/recognize/flash` | `volc.bigasr.auc_turbo` |
| [闲时版](https://www.volcengine.com/docs/6561/1840838?lang=zh) | `/api/v3/auc/bigmodel/idle/submit` + `/idle/query` | `volc.bigasr.auc_idle` |

“接口更新”不等于擅自切换极速版或闲时版。除非用户明确要求，否则保持标准版模型 2.0。

## 调用流程

1. 生成随机 UUID，作为整个任务的 `X-Api-Request-Id`。
2. 向 Submit 地址发送 JSON。
3. 从响应 Header 读取业务状态码和 `X-Tt-Logid`；Submit 响应 Body 为空。
4. 使用同一个 `X-Api-Request-Id` 轮询 Query 地址，Body 为 `{}`。
5. Header 状态码为 `20000000` 时读取 JSON 结果；`20000001`、`20000002` 时继续等待。

接口：

```text
POST https://openspeech.bytedance.com/api/v3/auc/bigmodel/submit
POST https://openspeech.bytedance.com/api/v3/auc/bigmodel/query
```

HTTP 200 只表示 HTTP 请求成功。任务是否成功必须读取 `X-Api-Status-Code`。

## 鉴权

### 新版控制台：优先

只需要 APP Key：

```http
X-Api-Key: <APP_KEY>
X-Api-Resource-Id: volc.seedasr.auc
X-Api-Request-Id: <UUID>
X-Api-Sequence: -1
Content-Type: application/json
```

本 Skill 对应环境变量：

```text
DOUBAO_API_KEY
```

### 旧版控制台：兼容

```http
X-Api-App-Key: <APP_ID>
X-Api-Access-Key: <ACCESS_TOKEN>
X-Api-Resource-Id: volc.seedasr.auc
X-Api-Request-Id: <UUID>
X-Api-Sequence: -1
Content-Type: application/json
```

本 Skill 对应环境变量：

```text
DOUBAO_APPID
DOUBAO_ACCESS_TOKEN
```

选择规则：

1. 存在 `DOUBAO_API_KEY` 时使用新版鉴权。
2. 否则仅当旧版两个变量同时存在时使用旧版鉴权。
3. 不要同时发送两套鉴权 Header。
4. 不要打印或写入任何密钥值。

`X-Api-Sequence: -1` 用于 Submit；官方 Query Header 表不要求该字段。`X-Tt-Logid` 是服务端诊断 ID，应记录在非敏感日志里，但不是 Query 的任务主键。

## 音频输入

官方标准版字段表当前要求：

```json
{
  "audio": {
    "url": "https://example.com/audio.mp3",
    "format": "mp3"
  }
}
```

关键字段：

| 字段 | 含义 | 当前文档约束 |
|---|---|---|
| `audio.url` | 服务端可访问的音频 URL | 官方标准版文档列为必填 |
| `audio.language` | 指定语言 | 为空时支持中英文及部分中文方言；指定时使用 `zh-CN`、`en-US` 等 |
| `audio.format` | 容器格式 | 必填；`raw` / `wav` / `mp3` / `ogg` |
| `audio.codec` | 编码格式 | 可选；`raw` / `opus`，默认 raw |
| `audio.rate` | 采样率 | 默认 `16000` |
| `audio.bits` | 采样位数 | 默认且仅支持 `16` |
| `audio.channel` | 声道数 | `1` / `2`，默认 `1` |

注意：

- `format=mp3` 时不要附加 `codec=raw`。MP3 已经表达了容器/编码，`raw` 会造成语义冲突。
- 本 Skill 会把本地文件转成 16 kHz、单声道、64 kbps MP3。
- 本 Skill 的 Base64 `audio.data` 路径在标准版生产接口上于 `2026-07-25` 实测成功，但当前标准版公开字段表只列出 `audio.url`。严格文档模式使用 `--doubao-audio-url`。
- `--doubao-audio-url` 必须与本地 `<input>` 指向同一录音，否则双路核验没有意义。
- 官方错误码显示单文件大小必须小于 512 MB。

## 请求参数

基础结构：

```json
{
  "user": {
    "uid": "audio-transcription-skill"
  },
  "audio": {
    "url": "https://example.com/audio.mp3",
    "format": "mp3"
  },
  "request": {
    "model_name": "bigmodel",
    "ssd_version": "200",
    "enable_itn": true,
    "enable_punc": true,
    "enable_ddc": false,
    "show_utterances": true,
    "enable_speaker_info": true
  }
}
```

本 Skill 的核心参数：

| 参数 | 官方默认值/约束 | 本 Skill | 原因 |
|---|---|---|---|
| `model_name` | 必填，目前为 `bigmodel` | `bigmodel` | 标准版要求 |
| `ssd_version` | 字符串；说话人分离开启且语言为空或 `zh-CN` 时生效 | `"200"` | 使用当前说话人分离版本 |
| `enable_itn` | 默认 `true` | `true` | 将口语数字等转成书面形式 |
| `enable_punc` | 默认 `false` | `true` | 输出可读标点 |
| `enable_ddc` | 默认 `false` | `false` | 保留语气词、重复和原始表达，便于复盘 |
| `show_utterances` | 可选 | `true` | 获取分句和毫秒时间戳 |
| `enable_speaker_info` | 默认 `false` | `true` | 获取说话人聚类 |

`enable_speaker_info` 官方说明为 10 人以内效果较好；音量、距离变化明显时不能保证区分。输出只能称为 speaker 聚类编号，不能直接当作真实身份。

### 按需参数

不要为了“信息更全”默认全部开启：

| 参数 | 用途 |
|---|---|
| `enable_channel_split` | 双声道分别识别，结果用 `channel_id` 标识左右声道 |
| `vad_segment` | 使用 VAD 分句；双声道识别通常配合开启 |
| `end_window_size` | 静音强制判停，范围 300–5000 ms；设置后不使用语义分句 |
| `show_speech_rate` | 分句 `additions` 返回 token/s |
| `show_volume` | 分句 `additions` 返回分贝 |
| `enable_lid` | 返回中英文及部分中文方言的语种标签 |
| `enable_auto_lang` | 自动选择 25 个小语种模型；不要与普通 `enable_lid` 混为一谈 |
| `enable_emotion_detection` | 返回情绪标签 |
| `enable_gender_detection` | 返回 male/female 标签；通常不应为普通转写开启 |
| `sensitive_words_filter` | 保留、删除或星号替换敏感词 |
| `callback` / `callback_data` | 用回调代替主动轮询 |

### 热词与上下文

`request.corpus` 支持：

- `boosting_table_name`：自学习平台热词表。
- `correct_table_name`：替换词表。
- `context`：JSON 字符串，不是直接嵌套对象。

`context` 的两类用法：

1. 直传最多 5000 个热词。
2. 对话上下文最多 800 tokens、20 轮，按从新到旧传入。

模型 2.0 还支持在上下文中传 1 张 `image_url`，图片需为 JPEG/JPG/PNG 且不超过 500 KB。普通面试转写不要自动上传额外图片或拼接无关上下文；它们可能诱导错误识别。

## 返回结果

成功的 Query Body 主要包含：

```json
{
  "audio_info": {
    "duration": 3696
  },
  "result": {
    "text": "整段文本",
    "utterances": [
      {
        "start_time": 0,
        "end_time": 1705,
        "text": "分句文本",
        "words": []
      }
    ]
  }
}
```

- `result.text`：整个音频文本。
- `result.utterances`：仅在 `show_utterances=true` 时返回。
- `start_time` / `end_time`：毫秒。
- `words`：词级时间信息。
- speaker、语速、音量等扩展能力通常出现在 utterance 的附加字段里；解析时兼容字段缺失。

## 状态码

| 状态码 | 含义 | 处理 |
|---|---|---|
| `20000000` | 成功 | Submit 表示已受理；Query 表示结果可读 |
| `20000001` | 正在处理中 | 继续轮询 |
| `20000002` | 任务在队列中 | 继续轮询 |
| `20000003` | 静音音频 | 停止轮询，报告未检测到人声 |
| `45000001` | 请求参数无效 | 检查缺失字段、字段值和重复 UUID |
| `45000002` | 空音频 | 检查转码和文件内容 |
| `45000131` | 半小时窗口内提交总时长超限 | 降低提交速率 |
| `45000132` | 音频超过大小限制 | 保持小于 512 MB |
| `45000151` | 音频格式不正确 | 检查真实格式与 `audio.format` 是否一致 |
| `550xxxx` | 服务内部错误 | 记录 Log ID，有限重试 |
| `55000031` | 服务器繁忙 | 退避后重试，避免高频提交 |

## 实现检查清单

- 使用标准版 Submit / Query，不混用 Flash 或 Idle。
- 使用模型 2.0 Resource ID：`volc.seedasr.auc`。
- 优先新版 `X-Api-Key`，旧版双 Header 只作兼容。
- Submit 和 Query 使用同一个 UUID。
- 只在 Submit 发送 `X-Api-Sequence: -1`。
- 读取 Header 业务状态码，不只看 HTTP 状态。
- 记录 `X-Tt-Logid`，不记录凭据。
- `format` 与真实文件一致；MP3 不声明 `codec=raw`。
- 逐字稿保持 `enable_ddc=false`。
- 说话人标签只当聚类结果。
