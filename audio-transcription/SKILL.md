---
name: audio-transcription
description: >-
  Transcribe or extract transcripts from local audio/video files. Use only when
  the user explicitly requests transcription or transcript extraction. Local
  offline transcription requires macOS Apple Silicon (arm64). Online Doubao
  transcription uploads audio and requires explicit cloud/upload intent.
---

# Audio Transcription

默认用本 Skill 内置的 `local-transcribe` 运行 Qwen 与 MOSS，本地顺序执行、完全离线、分别保留结果。本地离线路径只支持 macOS Apple Silicon（arm64）。

## 路由

1. 多个媒体按用户给出的顺序逐个完成；前一个命令退出后再开始下一个，不并发启动 Agent、进程或在线任务。
2. 每个媒体先运行 `scripts/local-transcribe plan "<media>" --json`。
3. `SETUP_REQUIRED`：读取 [setup.md](references/setup.md)。用户明确要求 setup 后再安装。
   用户明确要求外置盘、持久化运行时或持久化转写目录时，先运行
   `scripts/manage-runtime storage status --json`；在其确认四个独立目录后，运行
   `storage configure`，再继续 setup。此配置只保存路径，不迁移既有数据，也不构成上传授权。
4. 普通转写：运行 `scripts/local-transcribe "<media>" --json`，再读取 manifest 指向的产物。
5. 用户明确要求豆包、在线、云端或允许上传：读取 [online-transcription.md](references/online-transcription.md)。仅“双模型、并行、交叉验证”不构成上传授权。
6. 需要核对多份结果：读取 [transcript-review.md](references/transcript-review.md)。
7. CLI 给出的 `next_actions` 无法解决失败时，读取 [troubleshooting.md](references/troubleshooting.md)。

## 事实源

参数、默认值、副作用、输出协议、错误码和恢复动作以各脚本的 `--help`、`help <topic>` 与 `--json` 为准；不要从本文或 reference 猜测。

平台限制、在线上传和第三方许可证见 [setup.md](references/setup.md)、[online-transcription.md](references/online-transcription.md) 与 [NOTICE.md](NOTICE.md)。

不要改写或删除输入文件。不要把完整逐字稿塞进回复；除非用户要求，返回模式、状态、产物路径和重要存疑点即可。
