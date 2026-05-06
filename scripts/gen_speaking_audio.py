#!/usr/bin/env python3
"""Generate TTS audio (questions + answers) for each Speaking topic deck.

Reads TOPICS from gen_speaking_topics.py, strips markup, runs Piper TTS
to a WAV, then ffmpeg to MP3, saving under
  /speaking/topics/{slug}/audio/{q1.mp3,a1.mp3,q2.mp3,a2.mp3,...}

Idempotent: skips files that already exist (delete to regenerate).

Voice: en_US-amy-medium (clear American female).
Swap MODEL path below for British (en_GB-alba-medium etc.) if preferred.
"""

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

# Add scripts/ to path so we can import the topic data
SCRIPTS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS_DIR))

from gen_speaking_topics import TOPICS  # noqa: E402

REPO_ROOT = SCRIPTS_DIR.parent
MODEL = Path.home() / ".cache" / "piper-voices" / "cori-med.onnx"
LENGTH_SCALE = "1.0"  # 1.0 = normal, >1.0 slower (more pedagogical), <1.0 faster
# Voice: Cori (medium) by Bryce Beattie — UK English female, public domain
# Source: https://brycebeattie.com/files/tts/  (LibriVox-trained, 24h dataset)


def strip_markup(text: str) -> str:
    """Remove ~~..~~ and ==..== markers, keep inner text."""
    text = re.sub(r"~~(.*?)~~", r"\1", text)
    text = re.sub(r"==(.*?)==", r"\1", text)
    return text


def piper_to_wav(text: str, wav_path: Path) -> None:
    """Run piper to synthesize WAV."""
    subprocess.run(
        [
            sys.executable, "-m", "piper",
            "-m", str(MODEL),
            "-f", str(wav_path),
            "--length-scale", LENGTH_SCALE,
        ],
        input=text,
        text=True,
        check=True,
        capture_output=True,
    )


def wav_to_mp3(wav_path: Path, mp3_path: Path) -> None:
    """Convert WAV -> MP3 mono 64kbps via ffmpeg."""
    subprocess.run(
        [
            "ffmpeg", "-y", "-loglevel", "error",
            "-i", str(wav_path),
            "-codec:a", "libmp3lame",
            "-b:a", "64k",
            "-ac", "1",
            str(mp3_path),
        ],
        check=True,
    )


def synth(text: str, mp3_path: Path) -> None:
    if mp3_path.exists():
        return
    mp3_path.parent.mkdir(parents=True, exist_ok=True)
    wav_tmp = mp3_path.with_suffix(".wav")
    piper_to_wav(text, wav_tmp)
    wav_to_mp3(wav_tmp, mp3_path)
    wav_tmp.unlink(missing_ok=True)


def main() -> None:
    if not MODEL.exists():
        print(f"ERROR: voice model not found at {MODEL}", file=sys.stderr)
        print("Download with:", file=sys.stderr)
        print("  curl -L -o ~/.cache/piper-voices/en_US-amy-medium.onnx https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/amy/medium/en_US-amy-medium.onnx", file=sys.stderr)
        print("  curl -L -o ~/.cache/piper-voices/en_US-amy-medium.onnx.json https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/amy/medium/en_US-amy-medium.onnx.json", file=sys.stderr)
        sys.exit(1)

    if not shutil.which("ffmpeg"):
        print("ERROR: ffmpeg not found in PATH", file=sys.stderr)
        sys.exit(1)

    total = sum(2 * len(t["questions"]) for t in TOPICS)
    done = 0
    skipped = 0

    for topic in TOPICS:
        audio_dir = REPO_ROOT / "speaking" / "topics" / topic["slug"] / "audio"
        for qi, item in enumerate(topic["questions"], start=1):
            q_path = audio_dir / f"q{qi}.mp3"
            a_path = audio_dir / f"a{qi}.mp3"

            if q_path.exists():
                skipped += 1
            else:
                synth(item["q"], q_path)
                done += 1
                print(f"  [{done}/{total - skipped}]  {q_path.relative_to(REPO_ROOT)}")

            answer_text = strip_markup(item["a"])
            if a_path.exists():
                skipped += 1
            else:
                synth(answer_text, a_path)
                done += 1
                print(f"  [{done}/{total - skipped}]  {a_path.relative_to(REPO_ROOT)}")

    print(f"\nDone. Generated {done} clips, skipped {skipped} existing.")


if __name__ == "__main__":
    main()
