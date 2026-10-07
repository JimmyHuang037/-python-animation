#!/usr/bin/env python3
"""为 list-ops 各课旁白生成豆包 Tina2.0 配音（seed-tts-2.0 单向流式 HTTP）。

凭据只从环境变量 VOLC_TTS_API_KEY 或 --key-file 指定的本机文件读取，
不写入日志、配置或仓库。相同文本+音色命中缓存即跳过请求。
"""
import argparse
import array
import base64
import hashlib
import json
import os
import pathlib
import subprocess
import sys
import uuid
import wave

VOICE = "zh_female_yingyujiaoxue_uranus_bigtts"
RESOURCE = "seed-tts-2.0"
URL = "https://openspeech.bytedance.com/api/v3/tts/unidirectional"
SAMPLE_RATE = 48000
CACHE = pathlib.Path(__file__).resolve().parent / "voice-cache"


def read_key(key_file):
    if key_file:
        return pathlib.Path(key_file).read_text(encoding="utf-8").strip()
    value = os.environ.get("VOLC_TTS_API_KEY", "").strip()
    if not value:
        sys.exit("缺少凭据：设置 VOLC_TTS_API_KEY 或用 --key-file 指定文件")
    return value


def synth(key, text):
    digest = hashlib.sha256(f"{RESOURCE}|{VOICE}|{text}".encode("utf-8")).hexdigest()
    cached = CACHE / f"{digest}.wav"
    if cached.exists():
        return cached
    payload = json.dumps({
        "user": {"uid": "python-animation-lesson"},
        "req_params": {
            "text": text,
            "speaker": VOICE,
            "audio_params": {"format": "wav", "sample_rate": SAMPLE_RATE},
        },
    }, ensure_ascii=False).encode("utf-8")
    proc = subprocess.run(
        ["curl", "-sS", "--max-time", "180", "-X", "POST", URL,
         "-H", "Content-Type: application/json",
         "-H", f"X-Api-Key: {key}",
         "-H", f"X-Api-Resource-Id: {RESOURCE}",
         "-H", f"X-Api-Request-Id: {uuid.uuid4()}",
         "--data-binary", "@-"],
        input=payload, capture_output=True, check=True)
    chunks = []
    for line in proc.stdout.decode("utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line or line == "[DONE]":
            continue
        body = json.loads(line)
        code = body.get("code")
        if code not in (None, 0, 20000000):
            sys.exit(f"TTS 返回错误 code={code}: {str(body.get('message'))[:300]}")
        if body.get("data"):
            chunks.append(base64.b64decode(body["data"]))
    if not chunks:
        sys.exit(f"TTS 未返回音频: {proc.stdout[:300]!r}")
    CACHE.mkdir(parents=True, exist_ok=True)
    cached.write_bytes(b"".join(chunks))
    return cached


def to_48k_mono(src, dst):
    with wave.open(str(src)) as w:
        rate, channels, width = w.getframerate(), w.getnchannels(), w.getsampwidth()
        frames = w.readframes(w.getnframes())
    assert width == 2, f"期望 16-bit PCM, 实际 sampwidth={width}"
    assert rate == SAMPLE_RATE, f"期望 {SAMPLE_RATE}Hz, 实际 {rate}Hz"
    samples = array.array("h")
    samples.frombytes(frames)
    if channels == 2:
        samples = samples[0::2]
    with wave.open(str(dst), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SAMPLE_RATE)
        w.writeframes(samples.tobytes())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lessons", nargs="+", required=True)
    ap.add_argument("--key-file")
    args = ap.parse_args()
    key = read_key(args.key_file)
    for lesson_path in args.lessons:
        lesson_path = pathlib.Path(lesson_path)
        lesson = json.loads(lesson_path.read_text(encoding="utf-8"))
        root = lesson_path.parent
        for i, stage in enumerate(lesson["stages"], 1):
            dst = root / stage["audio"]
            dst.parent.mkdir(parents=True, exist_ok=True)
            to_48k_mono(synth(key, stage["narration"]), dst)
            with wave.open(str(dst)) as w:
                secs = w.getnframes() / w.getframerate()
            print(f"{root.name} stage{i}: {secs:.2f}s -> {dst}", flush=True)


if __name__ == "__main__":
    main()
