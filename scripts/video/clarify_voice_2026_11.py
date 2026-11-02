"""Build a reversible consonant-preserving voice experiment, not pronunciation repair.

Run with the direct EU5 Python interpreter. Requires ffmpeg and ffprobe on PATH.
All outputs live in out/voice_clarity_trial; the release render is untouched.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "docs/video/2026-11_update/out"
TRIAL = OUT / "voice_clarity_trial"
SOURCE = ROOT / "assets/1030-movie/音频 1_2.wav"
CURRENT = OUT / "great_projects_1.4_audio.wav"
# Deliberately omit the previous serial denoisers and de-esser: their attenuation
# can remove consonant detail. These filters cannot change s/sh or z/zh phonemes.
FILTERS = ",".join([
    "highpass=f=75:poles=2",
    "afftdn=nf=-50:nr=9:tn=1",
    "equalizer=f=280:t=q:w=0.9:g=-1.5",
    "equalizer=f=2200:t=q:w=0.8:g=1.5",
    "equalizer=f=4200:t=q:w=1.0:g=1.0",
    "acompressor=threshold=-20dB:ratio=1.7:attack=18:release=160:makeup=1",
])


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["ffmpeg", "-hide_banner", "-nostdin", "-nostats", *args],
                          check=True, capture_output=True, text=True, encoding="utf-8",
                          errors="replace")


def measure(path: Path, filters: str = "anull") -> dict:
    result = run("-i", str(path), "-af",
                 f"{filters},loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json",
                 "-f", "null", "-")
    start = result.stderr.rfind("{")
    return json.loads(result.stderr[start:result.stderr.rfind("}") + 1])


def main() -> None:
    TRIAL.mkdir(parents=True, exist_ok=True)
    # Match the current audio's exact sample count so the subtitle timeline stays put.
    probe = subprocess.run([
        "ffprobe", "-v", "error", "-select_streams", "a:0",
        "-show_entries", "stream=duration_ts,time_base", "-of", "json", str(CURRENT),
    ], check=True, capture_output=True, text=True)
    stream = json.loads(probe.stdout)["streams"][0]
    num, den = map(int, stream["time_base"].split("/"))
    samples = round(int(stream["duration_ts"]) * num * 48000 / den)
    measured = measure(SOURCE, FILTERS)
    normalization = (
        "loudnorm=I=-16:TP=-1.5:LRA=11:linear=true:"
        f"measured_I={measured['input_i']}:measured_TP={measured['input_tp']}:"
        f"measured_LRA={measured['input_lra']}:"
        f"measured_thresh={measured['input_thresh']}:offset={measured['target_offset']}"
    )
    chain = f"{FILTERS},{normalization},aresample=48000,atrim=end_sample={samples}"
    voice = TRIAL / "voice_clarity.wav"
    run("-y", "-i", str(SOURCE), "-af", chain, "-ar", "48000", "-ac", "2",
        "-c:a", "pcm_s24le", str(voice))
    # A/B uses the same phrase and matched overall loudness, separated by 0.8s.
    # First A = current release processing; then B = this experiment.
    run("-y", "-i", str(CURRENT), "-i", str(voice), "-filter_complex",
        "[0:a]atrim=start=17:end=38.9,asetpts=PTS-STARTPTS,"
        "volume=-0.18dB,apad=pad_dur=0.8[a];"
        "[1:a]atrim=start=17:end=38.9,asetpts=PTS-STARTPTS[b];"
        "[a][b]concat=n=2:v=0:a=1[out]", "-map", "[out]",
        "-c:a", "libmp3lame", "-b:a", "192k", str(TRIAL / "AB_current_then_clarity.mp3"))
    # Copy the existing burned video stream; no frame rendering or timeline changes.
    run("-y", "-i", str(OUT / "great_projects_1.4_burned.mp4"), "-i", str(voice),
        "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac",
        "-b:a", "192k", "-movflags", "+faststart", str(TRIAL / "preview_clarity.mp4"))
    report = {"purpose": "Consonant-preserving listening trial; not phoneme correction",
              "source": str(SOURCE.relative_to(ROOT)), "filter_chain": chain,
              "samples": samples, "sample_rate": 48000,
              "current": measure(CURRENT), "trial": measure(voice),
              "ab_order": "A: current 17-38.9s; 0.8s silence; B: trial same excerpt",
              "subjective_listening_verified": False}
    (TRIAL / "processing_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
