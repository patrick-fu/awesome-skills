#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///

import argparse
import copy
import hashlib
import json
import math
import os
from pathlib import Path
import shutil
import subprocess
import sys
import unicodedata
import uuid

from animatic import media_info, read_storyboard, validate_visual, validate_word_times, write_json
from volcengine_tts import DEFAULT_INSTRUCTION, DEFAULT_VOICE, synthesize


def normalized(text):
    return "".join(char for char in text if char.isalnum())


def align_words(text, words):
    validate_word_times(words, "speech")
    usable = [word for word in words if normalized(word["text"])]
    if normalized("".join(word["text"] for word in usable)) != normalized(text):
        raise ValueError("Returned word text differs from narration; inspect the saved audio and word times")
    positions = [i for i, char in enumerate(text) if char.isalnum()]
    result, mapping = [], []
    offset = raw_start = 0
    for word in usable:
        count = len(normalized(word["text"]))
        offset += count
        raw_end = positions[offset] if offset < len(positions) else len(text)
        if offset < len(positions):
            for index in range(positions[offset - 1] + 1, raw_end):
                char = text[index]
                if char in "“‘（([<{〈《「『【" or unicodedata.category(char).startswith("S"):
                    raw_end = index
                    break
        item = {"text": text[raw_start:raw_end], "start": word["start"], "end": word["end"]}
        result.append(item)
        mapping.extend([item] * count)
        raw_start = raw_end
    if not result:
        raise ValueError("Narration has no alignable words")
    return result, mapping


def anchor_ranges(text, anchors):
    plain = normalized(text)
    ranges = []
    for anchor in anchors:
        if isinstance(anchor, str):
            anchor = {"word": anchor}
        target = normalized(anchor["word"])
        start = -len(target)
        for _ in range(anchor.get("occurrence", 1)):
            start = plain.find(target, start + len(target))
            if start < 0:
                raise ValueError(f"Keyword occurrence not found in narration: {anchor['word']!r}")
        ranges.append((start, start + len(target) - 1, anchor))
    return sorted(ranges, key=lambda item: item[0])


def make_cues(mapping, ranges):
    return [{"word": anchor["word"], "start": mapping[start]["start"], "end": mapping[end]["end"],
             **{key: anchor[key] for key in ["focus", "show"] if key in anchor}}
            for start, end, anchor in ranges]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_audio_words(path, words):
    info = media_info(path)
    if not any(stream.get("codec_type") == "audio" for stream in info.get("streams", [])):
        raise ValueError(f"{path.name}: no audio stream")
    duration = float(info["format"]["duration"])
    if not math.isfinite(duration) or duration <= 0:
        raise ValueError(f"{path.name}: audio duration must be positive and finite")
    if any(word["end"] > duration + 0.05 for word in words):
        raise ValueError(f"{path.name}: word timing exceeds audio duration")


def prepare(source, output):
    source, output = source.resolve(), output.resolve()
    board = read_storyboard(source)
    board.setdefault("voice", DEFAULT_VOICE)
    board.setdefault("language", "zh-CN")
    marker = output / ".animatic-speech"
    if output.exists() and any(output.iterdir()) and not (marker.is_file() and marker.read_text() == "animatic-speech-v1\n"):
        raise ValueError("Speech output must be empty or owned by prepare_speech")
    session_path = output / "speech-session.json"
    session_exists = session_path.exists()
    if session_exists:
        session = json.loads(session_path.read_text(encoding="utf-8"))
        if not isinstance(session, dict) or session.get("version") != 1 or not isinstance(session.get("section_id"), str):
            raise ValueError("Invalid speech context; inspect it and use a new output directory")
        section_id = str(uuid.UUID(session["section_id"]))
    else:
        section_id = str(uuid.uuid4())
    jobs = []
    for scene in board["scenes"]:
        focus_count = len(scene["items"]) if scene["layout"] == "flow" else len(scene["code"].split("\n")) if scene["layout"] == "code" else 0
        for index, beat in enumerate(scene["beats"]):
            name = f"{scene['id']}-{index}"
            ranges = anchor_ranges(beat["narration"], beat.get("anchors", []))
            state = {key: beat[key] for key in ["focus", "show"] if key in beat}
            for _, _, anchor in ranges:
                state.update({key: anchor[key] for key in ["focus", "show"] if key in anchor})
                validate_visual(state, focus_count, name)
            delivery = beat.get("delivery", {})
            request = {"text": beat["narration"], "voice": board["voice"],
                       "instruction": delivery.get("instruction", DEFAULT_INSTRUCTION), "speed": delivery.get("speed", 1),
                       "format": "wav", "enable_subtitle": True}
            supplied = (source.parent / beat["audio"]).resolve() if "audio" in beat else None
            if supplied:
                if not beat.get("words"):
                    raise ValueError(f"{name}: supplied audio requires words for speech preparation")
                align_words(beat["narration"], beat["words"])
                validate_audio_words(supplied, beat["words"])
                request.update(source_audio_sha256=digest(supplied), supplied_words=beat["words"])
            else:
                request["section_id"] = section_id
            audio = output / f"{name}{supplied.suffix if supplied else '.wav'}"
            timing = output / f"{name}.words.json"
            record = output / f"{name}.request.json"
            present = [path.exists() for path in [audio, timing, record]]
            if any(present):
                if not all(present):
                    raise ValueError(f"{name}: incomplete speech cache; inspect it and choose a new output directory")
                saved = json.loads(record.read_text(encoding="utf-8"))
                if not isinstance(saved, dict) or saved.get("request") != request or saved.get("audio_sha256") != digest(audio) or saved.get("timing_sha256") != digest(timing):
                    raise ValueError(f"{name}: speech settings or cached files changed; use a new output directory")
            jobs.append((beat, supplied, request, audio, timing, record, all(present), ranges))
    sequence = [{"audio": job[3].name, "request": job[2]} for job in jobs]
    fingerprint = hashlib.sha256(json.dumps(sequence, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()
    if session_exists and session.get("request_sha256") != fingerprint:
        raise ValueError("Speech context or narration order changed; use a new output directory")
    generated = [job for job in jobs if job[1] is None]
    pending = [job for job in generated if not job[6]]
    if pending and (session_exists or any(job[6] for job in generated)):
        raise ValueError("Incomplete speech context; use a new output directory to regenerate the continuous narration")
    if pending:
        missing = [name for name in ["DOUBAO_APPID", "DOUBAO_ACCESS_TOKEN"] if not os.environ.get(name)]
        if missing:
            raise ValueError(f"Missing environment variables: {', '.join(missing)}")
    output.mkdir(parents=True, exist_ok=True)
    marker.write_text("animatic-speech-v1\n", encoding="utf-8")
    if pending:
        with session_path.open("x", encoding="utf-8") as stream:
            json.dump({"version": 1, "section_id": section_id, "request_sha256": fingerprint},
                      stream, ensure_ascii=False, indent=2)
            stream.write("\n")
    result = copy.deepcopy(board)
    prepared = [beat for scene in result["scenes"] for beat in scene["beats"]]
    synthesized = 0
    for target, (beat, supplied, request, audio, timing, record, cached, ranges) in zip(prepared, jobs):
        if not cached:
            if supplied:
                shutil.copyfile(supplied, audio)
                write_json(timing, {"text": beat["narration"], "words": beat["words"]})
            else:
                synthesize(beat["narration"], board["voice"], audio, instruction=request["instruction"],
                           speed=request["speed"], timestamps=timing, audio_format="wav", section_id=section_id)
                synthesized += 1
            write_json(record, {"request": request, "audio_sha256": digest(audio), "timing_sha256": digest(timing)})
        data = json.loads(timing.read_text(encoding="utf-8"))
        if not isinstance(data, dict) or data.get("text") != beat["narration"]:
            raise ValueError(f"{audio.name}: saved narration differs from the input")
        words, mapping = align_words(beat["narration"], data["words"])
        validate_audio_words(audio, words)
        target.update(audio=audio.name, words=words)
        if "anchors" in beat:
            target["cues"] = make_cues(mapping, ranges)
    path = output / "storyboard.json"
    write_json(path, result)
    read_storyboard(path)
    return {"storyboard": str(path), "beats": len(jobs), "synthesized": synthesized,
            "reused": len(jobs) - synthesized}


def main():
    parser = argparse.ArgumentParser(description="Prepare continuous Volcengine narration with shared context and keyword timing")
    parser.add_argument("storyboard", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    try:
        print(json.dumps(prepare(args.storyboard, args.out), ensure_ascii=False))
        return 0
    except (OSError, ValueError, KeyError, RuntimeError, subprocess.SubprocessError) as exc:
        message = str(exc)
        for name in ["DOUBAO_APPID", "DOUBAO_ACCESS_TOKEN"]:
            if os.environ.get(name):
                message = message.replace(os.environ[name], "[redacted]")
        print(message[:1000], file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
