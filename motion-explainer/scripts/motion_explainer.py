#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["playwright==1.65.1"]
# ///

import argparse
import base64
import copy
import json
import math
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile


ASSETS = Path(__file__).resolve().parents[1] / "assets"
VALID_PROVIDERS = {"auto", "doubao", "qwen3-mlx", "edge", "supplied"}


def bundle_player(source, target):
    html = source.read_text(encoding="utf-8")
    placeholder = next((tag for tag in ["/* motion-explainer-fonts */", "/* animatic-fonts */"] if tag in html), None)
    if placeholder:
        fonts = ASSETS / "fonts"
        css = ["/*\n" + (fonts / "OFL.txt").read_text(encoding="utf-8") + "\n*/"]
        for name in ["lxgw-wenkai-lite-latin.woff2", "lxgw-wenkai-lite-cjk-common.woff2"]:
            encoded = base64.b64encode((fonts / name).read_bytes()).decode("ascii")
            css.append(
                '@font-face{font-family:"Motion Hand";src:url("data:font/woff2;base64,' + encoded +
                '") format("woff2");font-weight:400;font-style:normal;font-display:block}'
            )
            css.append(
                '@font-face{font-family:"Animatic Hand";src:url("data:font/woff2;base64,' + encoded +
                '") format("woff2");font-weight:400;font-style:normal;font-display:block}'
            )
        html = html.replace(placeholder, "\n".join(css))
    kit_placeholder = "/* motion-explainer-kit */"
    if kit_placeholder in html:
        kit_js = (ASSETS / "motion-kit.js").read_text(encoding="utf-8").replace("</script>", "<\\/script>")
        html = html.replace(kit_placeholder, kit_js)
    target.write_text(html, encoding="utf-8")


def run(args, timeout=300):
    result = subprocess.run(args, capture_output=True, text=True, timeout=timeout)
    if result.returncode:
        raise RuntimeError(f"{args[0]} failed: {result.stderr[-4000:]}")
    return result.stdout


def write_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def media_info(path):
    return json.loads(run([
        "ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)
    ]))


def validate_visual(data, focus_count, label):
    focus = data.get("focus", [])
    if focus_count is None:
        if not isinstance(focus, list) or any(type(i) is not int or i < 0 for i in focus):
            raise ValueError(f"{label}: focus indexes out of range")
        if "show" in data:
            shown = data["show"]
            if type(shown) is not int or shown < 1 or any(i >= shown for i in focus):
                raise ValueError(f"{label}: show must include the focused elements")
        return
    if not isinstance(focus, list) or any(type(i) is not int or not 0 <= i < focus_count for i in focus):
        raise ValueError(f"{label}: focus indexes out of range")
    if "show" in data:
        shown = data["show"]
        if type(shown) is not int or not 1 <= shown <= focus_count or any(i >= shown for i in focus):
            raise ValueError(f"{label}: show must include the focused elements")


def validate_word_times(words, label):
    if not isinstance(words, list) or not words:
        raise ValueError(f"{label}: words requires a non-empty list")
    previous = -1
    for word in words:
        if not isinstance(word, dict) or not isinstance(word.get("text"), str) or not word["text"]:
            raise ValueError(f"{label}: each word requires text")
        start, end = word.get("start"), word.get("end")
        if any(type(n) not in [int, float] or not math.isfinite(n) for n in [start, end]):
            raise ValueError(f"{label}: word times must be finite numbers")
        if start < 0 or end < start or start < previous:
            raise ValueError(f"{label}: word times must be ordered and non-negative")
        previous = start


def read_storyboard(path):
    board = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(board, dict) or type(board.get("version")) is not int or board["version"] != 1:
        raise ValueError("storyboard requires version: 1")
    if not isinstance(board.get("title"), str) or not board["title"].strip():
        raise ValueError("storyboard requires a title")
    for key in ["language", "voice"]:
        if key in board and (not isinstance(board[key], str) or not board[key].strip()):
            raise ValueError(f"{key} must be a non-empty string")
    if "speech_provider" in board:
        provider = board["speech_provider"]
        if not isinstance(provider, str) or provider not in VALID_PROVIDERS:
            raise ValueError(f"speech_provider must be one of: {', '.join(sorted(VALID_PROVIDERS))}")
    tts_command = board.get("tts_command")
    if tts_command is not None:
        if not isinstance(tts_command, list) or not tts_command or any(not isinstance(arg, str) or not arg for arg in tts_command):
            raise ValueError("tts_command must be a non-empty argv array")
        for placeholder in ["{text_file}", "{output}"]:
            if not any(placeholder in arg for arg in tts_command):
                raise ValueError(f"tts_command requires {placeholder}")
    scenes = board.get("scenes")
    if not isinstance(scenes, list) or not scenes:
        raise ValueError("storyboard requires non-empty scenes")
    identifiers = set()
    for scene in scenes:
        if not isinstance(scene, dict):
            raise ValueError("each scene must be an object")
        sid = scene.get("id", "")
        if not isinstance(sid, str) or not re.fullmatch(r"[a-zA-Z0-9_-]+", sid) or sid in identifiers:
            raise ValueError(f"invalid or duplicate scene id: {sid!r}")
        identifiers.add(sid)
        if not isinstance(scene.get("title"), str) or not scene["title"].strip():
            raise ValueError(f"{sid}: title required")
        if "text" in scene and not isinstance(scene["text"], str):
            raise ValueError(f"{sid}: text must be a string")
        layout = scene.get("layout")
        if layout == "flow":
            items = scene.get("items")
            if not isinstance(items, list) or not 2 <= len(items) <= 5 or any(not isinstance(s, str) or not s.strip() for s in items):
                raise ValueError(f"{sid}: flow requires 2–5 text items")
            focus_count = len(items)
        elif layout == "code":
            if not isinstance(scene.get("code"), str) or not scene["code"].strip():
                raise ValueError(f"{sid}: code required")
            focus_count = len(scene["code"].split("\n"))
            if focus_count > 12:
                raise ValueError(f"{sid}: split code into at most 12 lines per scene")
        elif layout == "title":
            focus_count = 0
        elif layout == "custom":
            focus_count = None
        else:
            raise ValueError(f"{sid}: unknown layout {layout!r}")
        beats = scene.get("beats")
        if not isinstance(beats, list) or not beats:
            raise ValueError(f"{sid}: beats required")
        for beat in beats:
            if not isinstance(beat, dict) or not isinstance(beat.get("narration"), str) or not beat["narration"].strip():
                raise ValueError(f"{sid}: each beat requires narration")
            validate_visual(beat, focus_count, sid)
            delivery = beat.get("delivery", {})
            if not isinstance(delivery, dict) or not isinstance(delivery.get("instruction", ""), str):
                raise ValueError(f"{sid}: delivery requires an instruction string")
            speed = delivery.get("speed", 1)
            if type(speed) not in [int, float] or not math.isfinite(speed) or not 0.5 <= speed <= 2:
                raise ValueError(f"{sid}: delivery.speed must be between 0.5 and 2")
            for field in ["anchors", "cues"]:
                if not isinstance(beat.get(field, []), list):
                    raise ValueError(f"{sid}: {field} must be a list")
            for anchor in beat.get("anchors", []):
                if isinstance(anchor, str):
                    anchor = {"word": anchor}
                if not isinstance(anchor, dict) or not isinstance(anchor.get("word"), str) or not any(c.isalnum() for c in anchor["word"]):
                    raise ValueError(f"{sid}: anchors require a non-empty keyword")
                occurrence = anchor.get("occurrence", 1)
                if type(occurrence) is not int or occurrence < 1:
                    raise ValueError(f"{sid}: anchor occurrence must be a positive integer")
                validate_visual(anchor, focus_count, sid)
            if "words" in beat:
                validate_word_times(beat["words"], sid)
            if beat.get("cues"):
                if any(not isinstance(cue, dict) for cue in beat["cues"]):
                    raise ValueError(f"{sid}: cues must be objects")
                validate_word_times([{**cue, "text": cue.get("word", "")} for cue in beat["cues"]], sid)
                state = {key: beat[key] for key in ["focus", "show"] if key in beat}
                for cue in beat["cues"]:
                    state.update({key: cue[key] for key in ["focus", "show"] if key in cue})
                    validate_visual(state, focus_count, sid)
            if "audio" in beat and (not isinstance(beat["audio"], str) or not (path.parent / beat["audio"]).is_file()):
                raise ValueError(f"{sid}: audio file does not exist")
            pause = beat.get("pause_ms", 350)
            if type(pause) is not int or not 0 <= pause <= 30000:
                raise ValueError(f"{sid}: pause_ms must be an integer from 0 to 30000")
    rate = board.get("speech_rate", 180)
    if type(rate) is not int or not 80 <= rate <= 400:
        raise ValueError("speech_rate must be an integer from 80 to 400")
    return board


def doctor():
    from playwright.sync_api import sync_playwright
    import manage_runtime

    result = {"tools": {tool: shutil.which(tool) for tool in ["uv", "ffmpeg", "ffprobe", "say"]}}
    with sync_playwright() as playwright:
        try:
            browser = playwright.chromium.launch()
            result["renderer"] = browser.version
            browser.close()
        except Exception as exc:
            result["renderer_error"] = str(exc).splitlines()[0]
    doubao_ready = bool(os.environ.get("DOUBAO_APPID") and os.environ.get("DOUBAO_ACCESS_TOKEN"))
    qwen_info = manage_runtime.inspect_host()
    result["speech_providers"] = {
        "doubao": {"ready": doubao_ready, "note": "Volcengine Seed-TTS 2.0 (recommended; requires DOUBAO_APPID and DOUBAO_ACCESS_TOKEN)"},
        "qwen3-mlx": {
            "ready": qwen_info["status"] == "READY",
            "status": qwen_info["status"],
            "apple_silicon": qwen_info["platform"]["apple_silicon"],
            "unified_memory_gib": qwen_info["unified_memory_gib"],
        },
        "edge": {"ready": bool(result["tools"]["uv"]), "note": "Zero-key online Microsoft Edge TTS (unofficial; explicit opt-in)"},
        "macos_say": {"ready": bool(result["tools"]["say"]), "note": "Local fallback without word timestamps"},
    }
    result["ready"] = all(result["tools"][tool] for tool in ["ffmpeg", "ffprobe"]) and "renderer" in result
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ready"] else 1


def srt_time(seconds):
    milliseconds = round(seconds * 1000)
    hours, milliseconds = divmod(milliseconds, 3600000)
    minutes, milliseconds = divmod(milliseconds, 60000)
    seconds, milliseconds = divmod(milliseconds, 1000)
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"


def make_audio(board, source, root, fps):
    (root / "audio").mkdir()
    timeline = []
    bundled = copy.deepcopy(board)
    voice = board.get("voice") or ("Tingting" if board.get("language", "en-US").lower().startswith("zh") else "Samantha")
    cursor = 0
    for scene_index, scene in enumerate(board["scenes"]):
        for beat_index, beat in enumerate(scene["beats"]):
            name = f"{len(timeline):03}-{scene['id']}-{beat_index}"
            audio = root / "audio" / f"{name}.wav"
            if "audio" in beat:
                original = (source.parent / beat["audio"]).resolve()
                bundled["scenes"][scene_index]["beats"][beat_index]["audio"] = f"audio/{name}.wav"
            else:
                text = root / f"{name}.txt"
                text.write_text(beat["narration"], encoding="utf-8")
                if board.get("tts_command"):
                    original = root / f"{name}.mp3"
                    values = {"{voice}": voice, "{text_file}": str(text), "{output}": str(original)}
                    command = list(board["tts_command"])
                    for placeholder, value in values.items():
                        command = [arg.replace(placeholder, value) for arg in command]
                    try:
                        run(command)
                    except RuntimeError as exc:
                        raise RuntimeError(f"TTS {name} ({voice}): {exc}") from None
                else:
                    if not shutil.which("say"):
                        raise RuntimeError("macOS say is unavailable; run prepare_speech.py, configure tts_command, or supply audio")
                    original = root / f"{name}.aiff"
                    run(["say", "-v", voice, "-r", str(board.get("speech_rate", 180)), "-f", str(text), "-o", str(original)])
            info = media_info(original)
            if not any(s["codec_type"] == "audio" for s in info["streams"]):
                raise ValueError(f"{name}: input has no audio stream")
            audio_duration = float(info["format"]["duration"])
            if not math.isfinite(audio_duration) or audio_duration <= 0:
                raise ValueError(f"{name}: invalid audio duration")
            if any(word["end"] > audio_duration + 0.05 for word in beat.get("words", []) + beat.get("cues", [])):
                raise ValueError(f"{name}: word or cue timing exceeds the audio duration")
            frames = math.ceil((audio_duration + beat.get("pause_ms", 350) / 1000) * fps)
            duration = frames / fps
            run(["ffmpeg", "-v", "error", "-y", "-i", str(original), "-vn", "-ar", "48000", "-ac", "1", "-c:a", "pcm_s16le", str(audio)])
            padded = root / f"padded-{name}.wav"
            run(["ffmpeg", "-v", "error", "-y", "-i", str(audio), "-af", "apad", "-t", f"{duration:.9f}", "-c:a", "pcm_s16le", str(padded)])
            timeline.append({
                "scene": scene_index, "scene_id": scene["id"], "beat": beat_index,
                "start": cursor / fps, "end": (cursor + frames) / fps,
                "frames": frames, "audio_duration": audio_duration,
                "narration": beat["narration"], "focus": beat.get("focus", []),
                "show": beat.get("show"),
                "audio": f"audio/{name}.wav", "frame": f"frames/{name}.png"
            })
            cursor += frames
            print(f"audio {name}: {duration:.2f}s", flush=True)
    concat = root / "audio.txt"
    concat.write_text("\n".join(f"file 'padded-{Path(beat['audio']).name}'" for beat in timeline) + "\n", encoding="utf-8")
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(concat), "-c:a", "pcm_s16le", str(root / "narration.wav")])
    captions = [f"{i + 1}\n{srt_time(beat['start'])} --> {srt_time(beat['end'])}\n{beat['narration']}\n" for i, beat in enumerate(timeline)]
    (root / "captions.srt").write_text("\n".join(captions), encoding="utf-8")
    return timeline, bundled


def render(board, timeline, root, player, width, fps):
    from playwright.sync_api import sync_playwright

    (root / "frames").mkdir()
    height = width * 9 // 16
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        try:
            page = browser.new_page(viewport={"width": width, "height": height}, device_scale_factor=1)
            errors = []
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.route("**/*", lambda route: route.abort())
            page.set_content(player.read_text(encoding="utf-8"))
            page.evaluate("data => (window.motionExplainer || window.animatic).load(data)", {"storyboard": board, "timeline": timeline, "width": width})
            page.evaluate("() => document.fonts.ready")
            for beat in timeline:
                midpoint = (beat["start"] + beat["end"]) / 2
                page.evaluate("t => (window.motionExplainer || window.animatic).seek(t, true)", midpoint)
                issues = page.evaluate("() => (window.motionExplainer || window.animatic).audit()")
                if issues or errors:
                    raise RuntimeError(f"{beat['scene_id']}/{beat['beat']}: {issues + errors}")
                page.screenshot(path=str(root / beat["frame"]))
                for moment in [beat["start"] + min(0.35, (beat["end"] - beat["start"]) / 2), beat["end"] - 1 / fps]:
                    page.evaluate("t => (window.motionExplainer || window.animatic).seek(t, false)", moment)
                    issues = page.evaluate("() => (window.motionExplainer || window.animatic).audit()")
                    if issues or errors:
                        raise RuntimeError(f"{beat['scene_id']}/{beat['beat']} at {moment:.3f}s: {issues + errors}")
            with (root / "encode.log").open("w") as log:
                process = subprocess.Popen([
                    "ffmpeg", "-v", "error", "-y", "-f", "image2pipe", "-vcodec", "png", "-framerate", str(fps), "-i", "pipe:0",
                    "-i", str(root / "narration.wav"), "-i", str(root / "captions.srt"),
                    "-map", "0:v:0", "-map", "1:a:0", "-map", "2:s:0", "-c:v", "libx264", "-preset", "fast", "-crf", "20",
                    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k", "-c:s", "mov_text", "-movflags", "+faststart",
                    "-metadata", f"title={board['title']}", str(root / "video.mp4")
                ], stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=log)
                try:
                    frame_index = 0
                    for beat in timeline:
                        print(f"render {beat['scene_id']}/{beat['beat']}: {beat['frames']} frames", flush=True)
                        for _ in range(beat["frames"]):
                            page.evaluate("t => (window.motionExplainer || window.animatic).seek(t, false)", frame_index / fps)
                            process.stdin.write(page.screenshot(type="png"))
                            frame_index += 1
                        if errors:
                            raise RuntimeError(f"renderer errors: {errors}")
                    process.stdin.close()
                    if process.wait(timeout=300):
                        raise RuntimeError((root / "encode.log").read_text()[-4000:])
                except BaseException:
                    process.kill()
                    process.wait()
                    raise
        finally:
            browser.close()


def verify(root):
    manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    timeline = json.loads((root / "timeline.json").read_text(encoding="utf-8"))
    info = media_info(root / "video.mp4")
    streams = {stream["codec_type"]: stream for stream in info["streams"]}
    if not {"video", "audio", "subtitle"} <= streams.keys():
        raise ValueError("video, audio and subtitle tracks are required")
    video, audio = streams["video"], streams["audio"]
    expected = manifest["duration"]
    tolerance = max(0.1, 2 / manifest["fps"])
    if video["codec_name"] != "h264" or audio["codec_name"] != "aac":
        raise ValueError("expected H.264 / AAC")
    if video["width"] != manifest["width"] or video["height"] != manifest["height"]:
        raise ValueError("video dimensions differ from manifest")
    if int(video["nb_frames"]) != manifest["frames"]:
        raise ValueError(f"encoded frame count: expected {manifest['frames']}, got {video['nb_frames']}")
    for stream in [video, audio, streams["subtitle"]]:
        if abs(float(stream["duration"]) - expected) > tolerance:
            raise ValueError(f"{stream['codec_type']} duration differs from timeline")
    cursor = 0.0
    for beat in timeline:
        if abs(beat["start"] - cursor) > 0.00001 or beat["end"] <= cursor:
            raise ValueError("timeline has a gap or overlap")
        if beat["audio_duration"] > beat["end"] - beat["start"]:
            raise ValueError("narration is truncated")
        for key in ["frame", "audio"]:
            if not (root / beat[key]).is_file():
                raise ValueError(f"missing {beat[key]}")
        cursor = beat["end"]
    if abs(cursor - expected) > 0.00001:
        raise ValueError("timeline duration differs from manifest")
    subtitles = (root / "captions.srt").read_text(encoding="utf-8")
    expected_ranges = [f"{srt_time(beat['start'])} --> {srt_time(beat['end'])}" for beat in timeline]
    if re.findall(r"\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}", subtitles) != expected_ranges:
        raise ValueError("caption timings differ from timeline")
    run(["ffmpeg", "-v", "error", "-xerror", "-i", str(root / "video.mp4"), "-map", "0:v:0", "-map", "0:a:0", "-f", "null", "-"], timeout=300)
    return {"ok": True, "duration": expected, "frames": manifest["frames"], "beats": len(timeline), "video": str(root / "video.mp4")}


def owned_directory(root: Path) -> bool:
    for name, expected in [(".motion-explainer", "motion-explainer-v1\n"), (".animatic", "animatic-v1\n")]:
        marker = root / name
        if marker.is_file() and marker.read_text(encoding="utf-8") == expected:
            return True
    return False


def build(args):
    source = args.storyboard.resolve()
    board = read_storyboard(source)
    for scene in board["scenes"]:
        for beat in scene["beats"]:
            if (beat.get("delivery") and "audio" not in beat) or (beat.get("anchors") and not beat.get("cues")):
                raise ValueError("delivery and anchors require prepared speech; run prepare_speech.py first")
    root = args.out.resolve()
    if root.exists() and any(root.iterdir()) and not owned_directory(root):
        raise ValueError("output directory must be empty or owned by motion-explainer (.motion-explainer marker)")
    root.mkdir(parents=True, exist_ok=True)
    (root / ".motion-explainer").write_text("motion-explainer-v1\n", encoding="utf-8")
    player = (args.player or ASSETS / "player.html").resolve()
    with tempfile.TemporaryDirectory(prefix=".build-", dir=root) as temporary:
        staging = Path(temporary)
        bundle_player(player, staging / "player.html")
        timeline, bundled = make_audio(board, source, staging, args.fps)
        render(board, timeline, staging, staging / "player.html", args.width, args.fps)
        write_json(staging / "storyboard.json", bundled)
        write_json(staging / "timeline.json", timeline)
        shutil.copyfile(staging / timeline[0]["frame"], staging / "poster.png")
        write_json(staging / "manifest.json", {
            "version": 1, "title": board["title"], "width": args.width, "height": args.width * 9 // 16,
            "fps": args.fps, "frames": sum(beat["frames"] for beat in timeline), "duration": timeline[-1]["end"],
            "speech": sorted({"supplied audio" if "audio" in beat else "configured TTS command" if board.get("tts_command") else "macOS say" for scene in board["scenes"] for beat in scene["beats"]}),
            "speech_provider": board.get("speech_provider"),
            "voice": board.get("voice"),
            "language": board.get("language"),
            "renderer": "playwright==1.65.1",
        })
        result = verify(staging)
        for name in ["audio", "frames"]:
            target = root / name
            if target.exists():
                shutil.rmtree(target)
            shutil.move(str(staging / name), str(target))
        for name in ["video.mp4", "storyboard.json", "timeline.json", "player.html", "captions.srt", "manifest.json", "poster.png"]:
            (staging / name).replace(root / name)
        result["video"] = str(root / "video.mp4")
        print(json.dumps(result, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(description="Build editable narrated explainer videos")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("doctor")
    validate = commands.add_parser("validate")
    validate.add_argument("storyboard", type=Path)
    make = commands.add_parser("build")
    make.add_argument("storyboard", type=Path)
    make.add_argument("--out", type=Path, required=True)
    make.add_argument("--player", type=Path)
    make.add_argument("--width", type=int, choices=[1280, 1920], default=1280)
    make.add_argument("--fps", type=int, choices=[12, 24, 30], default=24)
    check = commands.add_parser("verify")
    check.add_argument("out", type=Path)
    args = parser.parse_args()
    try:
        if args.command == "doctor":
            return doctor()
        if args.command == "validate":
            board = read_storyboard(args.storyboard.resolve())
            print(json.dumps({"ok": True, "scenes": len(board["scenes"]), "beats": sum(len(scene["beats"]) for scene in board["scenes"])}))
        elif args.command == "build":
            build(args)
        else:
            print(json.dumps(verify(args.out.resolve()), ensure_ascii=False, indent=2))
        return 0
    except (ValueError, KeyError, OSError, RuntimeError, subprocess.SubprocessError) as exc:
        print(f"motion-explainer: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
