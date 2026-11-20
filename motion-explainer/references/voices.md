# Recommended Voices (Non-Mandatory Priority Guide)

These lists are **priority-ordered recommendations** based on listening tests
for technical and conceptual explainers. They are **never mandatory**—always
honor any voice ID or custom recording the user explicitly prefers.

When `voice` is omitted from a storyboard, `prepare_speech.py` defaults to the
#1 voice for the selected provider and target language.

---

## 1. Doubao / Volcengine Seed-TTS 2.0 (`doubao`)

Official catalog: `https://docs.volcengine.com/docs/doubao-voice/tone-list-3?lang=zh`
(uses `seed-tts-2.0` / `uranus_bigtts` voices over HTTP V3 unidirectional stream).

### Chinese (`zh-CN`)
1. **甜美桃子 2.0** — `zh_female_tianmeitaozi_uranus_bigtts` *(default)*: relaxed, warm conversational explainer tone; strong prosody and pacing.
2. **Vivi 2.0** — `zh_female_vv_uranus_bigtts`: natural flagship bilingual female voice.
3. **小何 2.0** — `zh_female_xiaohe_uranus_bigtts`: clear, approachable conversational voice.
4. **知性灿灿 2.0** / **儒雅青年 2.0**: good alternatives for calmer or male technical narration (verify exact `uranus_bigtts` ID in the official catalog).

### English (`en-US` / `en-GB`)
Ordered with warm, conversational Sweet-Peach-like female voices first, followed by crisp explainer male and British voices:

1. **Sunny** — `en_female_myra_cmb_uranus_bigtts` *(default)*: warm, bright, relaxed conversational young female voice—closest English match to Sweet Peach (unidirectional stream only, compatible with `volcengine_tts.py`).
2. **Elaine** — `en_female_pleasant-female_uranus_bigtts`: softer, gentle, soothing conversational female voice.
3. **Hayley** — `en_female_hayley_uranus_bigtts`: lively, youthful YouTube-explainer female voice.
4. **Megan** — `en_female_wenrouzhishijieshuonv_uranus_bigtts`: warm, articulate knowledge-explainer female voice.
5. **Tim** — `en_male_tim_uranus_bigtts`: crisp, natural American male explainer voice with almost no synthetic feel.
6. **Russell** — `en_male_russell_uranus_bigtts` *(UK male)* / **Charlotte** — `en_female_authoritative-british_uranus_bigtts` *(UK female)*: clear British teaching voices.
7. **Alex** — `en_male_alex_uranus_bigtts`: deeper podcast/documentary American male voice.

### Other Languages
`zh_female_tianmeitaozi_uranus_bigtts` and `zh_female_vv_uranus_bigtts` support 30+ languages, or select a native-locale `uranus_bigtts` voice (e.g. `ja_`, `de_`, `es_`) from the official Volcengine tone list.

---

## 2. Local Qwen3-TTS 1.7B CustomVoice MLX (`qwen3-mlx`)

All 9 built-in speakers support 10 languages (`Chinese`, `English`, `Japanese`,
`Korean`, `French`, `German`, `Spanish`, `Portuguese`, `Italian`, `Russian`)
plus natural-language `delivery.instruction`. Matching a speaker's native
language yields the best accent and cadence:

### Chinese (`zh-CN`)
1. **`serena`** *(default)*: warm, gentle young female voice with natural breaths.
2. **`vivian`**: bright, crisp young female voice; punchy for technical pacing.
3. **`uncle_fu`**: seasoned, mellow deep male voice.
4. **`dylan`** *(Beijing dialect)* / **`eric`** *(Sichuan dialect)*: regional conversational male voices.

### English (`en-US`)
1. **`aiden`** *(default)*: sunny, clean American male voice with natural explainer pacing.
2. **`ryan`**: dynamic, slightly deeper American male voice with strong rhythm.

### Japanese & Korean
- **Japanese (`ja-JP`)**: **`ono_anna`** *(default)* — light, nimble Japanese female voice.
- **Korean (`ko-KR`)**: **`sohee`** *(default)* — warm, expressive Korean female voice.

---

## 3. Zero-Key Online Edge TTS (`edge`)

Not all Edge voices emit `WordBoundary` timestamps; the voices below are verified
or mainstream neural voices. Run `uv run --no-project --with edge-tts==7.3.1 edge-tts --list-voices`
for the full catalog.

- **Chinese (`zh-CN`)**:
  1. `zh-CN-XiaoxiaoNeural` *(default)* — clear, reliable explainer female voice (verified `WordBoundary`).
  2. `zh-CN-YunxiNeural` — clean young male voice.
  3. `zh-CN-XiaoyiNeural` — livelier young female voice.
- **English (`en-US` / `en-GB`)**:
  1. `en-US-AndrewNeural` *(default)* — podcast-grade natural American male explainer (verified `WordBoundary`).
  2. `en-US-AvaNeural` / `en-US-JennyNeural` — natural American female voices.
  3. `en-GB-SoniaNeural` — clear British female voice.
- **Other languages (defaults)**: `ja-JP-NanamiNeural`, `ko-KR-SunHiNeural`, `es-ES-ElviraNeural`, `fr-FR-DeniseNeural`, `de-DE-KatjaNeural`, `pt-BR-FranciscaNeural`, `it-IT-ElsaNeural`, `ru-RU-SvetlanaNeural`.

---

## 4. macOS `say` (Fallback Only)

- **Chinese**: `Tingting` · **English**: `Samantha` · inspect local voices via `say -v '?'`.
