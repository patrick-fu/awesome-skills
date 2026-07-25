# MLX Whisper CLI 与模型选择

本 Skill 的本地识别只调用 `mlx_whisper` CLI。不要在 Skill 内维护 Python venv、模型安装目录或 Hugging Face 缓存目录。

## 默认管理边界

- CLI 环境：交给 `uv tool`。
- 模型解析和下载：交给 `mlx_whisper`。
- 模型缓存：交给 Hugging Face Hub 默认缓存。
- Skill：只传模型 repo ID、识别参数和输出位置。

安装：

```bash
uv tool install mlx-whisper
```

升级：

```bash
uv tool upgrade mlx-whisper
```

查看：

```bash
command -v mlx_whisper
uv tool list
mlx_whisper --help
```

不要执行：

- 不要创建 `~/.local/share/audio-transcription/venv` 一类专用环境。
- 不要设置 Skill 专属 `HF_HOME` 或 `HF_HUB_CACHE`。
- 不要把 Hugging Face snapshot 路径硬编码进 Skill。
- 不要复制已缓存的模型到另一份自定义目录。

## 模型缓存

当 `--model` 是 Hugging Face repo ID 时，MLX Whisper 会自动下载模型，并复用 Hugging Face Hub 的默认缓存。macOS 上当前通常位于：

```text
~/.cache/huggingface/hub
```

这是 Hugging Face 的默认行为，不是 Skill 自己约定的路径。用户已经配置 `HF_HOME` 或 `HF_HUB_CACHE` 时尊重其配置，不覆盖。

`Fetching 4 files` 表示 CLI 在解析模型文件；文件已经缓存且版本未变化时，不会重复下载完整权重。需要提前填充默认缓存时可运行一次：

```bash
mlx_whisper "<short-audio>" \
  --model mlx-community/whisper-large-v3-turbo \
  --output-format json \
  --verbose False
```

也可以使用 Hugging Face 官方 CLI 的默认缓存：

```bash
hf download mlx-community/whisper-large-v3-turbo
```

不要附加 `--local-dir` 或自定义 `--cache-dir`。

如果用户明确要求断网运行，先确认模型已缓存，再为该次命令设置：

```bash
HF_HUB_OFFLINE=1
```

普通运行保持官方默认，不强制离线。

参考：

- [MLX Whisper README](https://github.com/ml-explore/mlx-examples/blob/main/whisper/README.md)
- [Hugging Face 下载和默认缓存](https://huggingface.co/docs/huggingface_hub/en/guides/download)
- [Hugging Face 缓存机制](https://huggingface.co/docs/huggingface_hub/en/guides/manage-cache)

## 当前默认

```text
mlx-community/whisper-large-v3-turbo
```

选择它的原因：

- 支持中文和中英混合内容；
- 相比完整 Large V3 更快；
- 对技术面试比 small/base/tiny 更适合作为交叉验证基准；
- 当前权重约 1.5 GB，已经存在于本机 Hugging Face 默认缓存。

## 主流模型

以下为 MLX Community 当前主流通用模型的近似仓库大小。实际磁盘占用可能包含缓存元数据和历史 revision。

| Repo ID | 近似大小 | 用途 |
|---|---:|---|
| `mlx-community/whisper-large-v3-turbo` | 1539 MiB | 默认；速度与准确率平衡 |
| `mlx-community/whisper-large-v3-turbo-8bit` | 824 MiB | 更省内存和磁盘 |
| `mlx-community/whisper-large-v3-turbo-4bit` | 443 MiB | 资源紧张设备 |
| `mlx-community/whisper-large-v3-fp16` | 2941 MiB | 优先追求多语言准确率 |
| `mlx-community/whisper-large-v3-8bit` | 1570 MiB | Large V3 折中版 |
| `mlx-community/whisper-large-v3-4bit` | 838 MiB | 更小的 Large V3 |
| `mlx-community/whisper-medium-fp16` | 1455 MiB | 中等规模 |
| `mlx-community/whisper-medium-8bit` | 778 MiB | 中等规模量化版 |
| `mlx-community/whisper-small-fp16` | 460 MiB | 快速预览 |
| `mlx-community/whisper-small-8bit` | 247 MiB | 轻量预览 |
| `mlx-community/whisper-base-fp16` | 138 MiB | 简单、清晰录音 |
| `mlx-community/whisper-tiny-fp16` | 72 MiB | 最轻量预览 |

模型选择：

1. 中文技术面试默认保持 `large-v3-turbo`。
2. 只有用户明确优先准确率时才改用 `large-v3-fp16`。
3. 只有用户明确受内存或磁盘限制时才选 8-bit / 4-bit。
4. `.en` 是英语专用模型，不用于中文或中英混合录音。
5. 模型 repo ID 直接传给 CLI；不要为每个模型设计独立安装流程。

OpenAI 的模型说明：

- `turbo` 是 Large V3 的加速版本，转写速度更快，准确率小幅下降。
- `tiny`、`base`、`small`、`medium`、`large` 是逐级增大的模型。
- `turbo` 不适合作为非英语到英语的翻译模型；本 Skill 默认只做 `transcribe`。

参考：

- [OpenAI Whisper 模型列表](https://github.com/openai/whisper/blob/main/README.md)
- [MLX Community Whisper Large V3 Turbo](https://huggingface.co/mlx-community/whisper-large-v3-turbo)
