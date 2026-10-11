"""Sodium / UV — original visualizer cue, 124 BPM, F# minor, 46 bars.

Generate: PYTHONPATH=tools python3 songs/sodium_uv.py
Render:   PYTHONPATH=tools python3 songs/sodium_uv.py --render
Requires numpy (slabkit) and ffmpeg (delivery analysis).
The loop is the eight-bar main drop, tail-wrapped and repeated twice.
"""
import argparse
import json
from pathlib import Path
import subprocess
import wave

import numpy as np
from slabkit import Song, fx
from slabkit.analyze import analyze_wav, read_wav

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "songs/sodium_uv"
song = Song("Sodium / UV", bpm=124, key="F# minor", groove_seed=12446)
intro, groove, build, drop, breakdown, final = [
    song.section(name, bars) for name, bars in
    [("INTRO", 8), ("GROOVE", 8), ("BUILD", 8), ("DROP", 8),
     ("BREAKDOWN", 8), ("FINAL DROP", 6)]
]

kick = song.track("SODIUM KICK", "drum2", "909-punch", volume=0.72,
    params=dict(kick_tune=54, kick_decay=0.24, kick_click=0.68,
                kick_drive=1.8, master_drive=1.0))
clap = song.track("CLAP / ROLL", "drum2", "dry-punch-kit", volume=0.44,
    params=dict(clap_decay=0.13, snare_decay=0.10, snare_sdec=0.06,
                snare_tone=2700, master_drive=1.0))
hats = song.track("CLOSED HATS", "drum2", "crisp-hat-kit", volume=0.65,
    pan=-0.19, params=dict(hat_chdec=0.07, hat_tone=1.04, master_drive=1.0))
openh = song.track("OFFBEAT AIR", "drum2", "thin-hat-kit", volume=0.58,
    pan=0.23, params=dict(hat_ohdec=0.24, hat_tone=1.05, master_drive=1.0))
bass = song.track("WARM ROLLING BASS", "cream", "synthwave-bass", volume=0.62,
    params=dict(range1="8", range2="8", wave1="SAW", wave2="TRI",
        lvl2=0.5, lvl3=0.18, cutoff=700, emphasis=0.14, contour=1.6,
        a_atk=0.003, a_dec=0.22, a_sus=0.5, a_rel=0.045,
        f_dec=0.16, f_sus=0.1, drive=0.32, level=0.65),
    fx=[fx("geq8", "flat", t1="LC12", f1=32),
        fx("comp2", key=kick, thresh=-21, ratio=3, atk=0.003, rel=0.13)])
pad = song.track("DESERT GLASS PAD", "juno2", "lush-pad", volume=0.20,
    params=dict(atk=0.3, rel=0.48, cutoff=1700, sub=0, level=0.62),
    fx=[fx("geq8", "flat", t1="LC12", f1=260, t3="BELL", f3=450, b3=-2),
        fx("chorus2", "wide-slow", mix=0.42, spread=0.7),
        fx("comp2", key=kick, thresh=-23, ratio=3, atk=0.002, rel=0.16)])
arp = song.track("UV ARPEGGIO", "profit5", "pluck-keys", volume=0.62,
    params=dict(cutoff=1500, env=0.30, a_dec=0.19, a_rel=0.08,
                f_dec=0.15, level=0.62, freq_b=0, fine_b=0.045),
    fx=[fx("geq8", "flat", t1="LC12", f1=240),
        fx("delay2", sync="SYNC", div="1/8.", mode="PING", fb=0.24,
           lowcut=550, damp=5200, mix=0.28, width=1.3)])
glass = song.track("GLASS ANSWER", "fm86", "slab/celesta", volume=1.05,
    pan=0.16, fx=[fx("geq8", "flat", t1="LC12", f1=400),
        fx("delay2", sync="SYNC", div="1/4", mode="PING", fb=0.20,
           lowcut=650, damp=6000, mix=0.24), fx("chorus2", "bell-widener", mix=0.3)])
stabs = song.track("AMBER STABS", "juno2", "warm-chord-plucks", volume=0.20,
    pan=-0.16, params=dict(atk=0.004, dec=0.20, sus=0.05, rel=0.10, cutoff=2300),
    fx=[fx("geq8", "flat", t1="LC12", f1=320)])
space = song.bus("NIGHT SPACE", volume=0.7,
    fx=[fx("verb2", "plate", mix=1, decay=1.3, lowcut=600,
           damp=5200, predelay=0.028, width=1.3)])
pad.send(space, -13)
arp.send(space, -19)
glass.send(space, -17)

# F#m9 / Dmaj9 / Aadd9 / E6. Upper voicings share common tones.
roots = [42, 38, 45, 40]
chords = [[57, 61, 64, 68], [57, 61, 64, 66],
          [57, 61, 64, 71], [56, 61, 64, 66]]
order = [0, 2, 1, 3, 2, 1, 0, 2, 1, 3, 2, 0, 3, 1, 2, 1]

def arrange(sec, kind):
    kc, hc, oc, cc = [t.clip(sec) for t in (kick, hats, openh, clap)]
    bc, pc, ac, gc, sc = [t.clip(sec) for t in (bass, pad, arp, glass, stabs)]
    for bar in range(sec.bars):
        at = bar * 4
        closing = kind == "final" and bar == sec.bars - 1
        root, chord = roots[(bar // 2) % 4], chords[(bar // 2) % 4]
        if kind == "final" and bar >= 4:
            root, chord = roots[0], chords[0]
        if kind != "break":
            for beat in range(1 if closing else 4):
                kc.note(36, at + beat, 0.12,
                        110 if kind in ("drop", "final") else 94 if kind == "intro" else 103)
        if kind != "break" and (kind != "intro" or bar >= 4) and not closing:
            for step in range(8):
                hc.note(42, at + step * 0.5, 0.06, 62 if step % 2 == 0 else 83)
            if kind != "intro":
                for beat in range(4):
                    oc.note(46, at + beat + 0.5, 0.10, 80 if kind in ("drop", "final") else 66)
                for beat in (1, 3):
                    cc.note(39, at + beat, 0.10, 92)
            if kind in ("drop", "final"):
                for step in (3, 11, 15):
                    hc.note(42, at + step * 0.25, 0.05, 48)
        if kind not in ("intro", "break"):
            if closing:
                bc.note(root, at, 0.35, 105)
            else:
                for step in (2, 3, 6, 8, 10, 11, 14):
                    pitch = root + (12 if step == 11 else 7 if step == 14 and bar % 2 else 0)
                    bc.note(pitch, at + step * 0.25, 0.18 if step in (3, 11) else 0.26,
                            102 if step in (2, 6, 10) else 85)
        if bar % 2 == 0 or closing:
            pc.chord(chord, at, 0.45 if closing else min(7.5, sec.length - at - 0.4),
                     69 if kind == "intro" else 83)
        if kind != "intro" or bar >= 4:
            steps = 1 if closing else 16
            for step in range(steps):
                if kind == "groove" and step % 2 or kind == "intro" and step % 4:
                    continue
                pitch = chord[order[step]] + 12
                if kind == "build" and bar >= 6 and step in (7, 15):
                    pitch += 12
                ac.note(pitch, at + step * 0.25, 0.12,
                        95 if step in (0, 3, 6, 10) else 71)
        if kind in ("drop", "final") and not closing:
            # A recognizable two-bar reply above the running arp.
            for offset, idx in [(0.75, 3), (1.5, 2), (2.75, 1), (3.5, 2)]:
                if bar % 2 == 0 or offset >= 2:
                    gc.note(chord[idx] + 12, at + offset, 0.23, 90)
            for offset in (1.75, 3.25):
                sc.chord(chord[:3], at + offset, 0.17, 87)
    if kind == "build":
        for i in range(16):
            cc.note(38, 24 + i * 0.25, 0.055, 47 + i * 2)
        for i in range(32):
            cc.note(38, 28 + i * 0.125, 0.045, 71 + round(i * 1.5))
        ac.ramp("cutoff", 0, 32, 1000, 6200, tension=-0.35)
        pc.ramp("cutoff", 0, 32, 1000, 3600)
    else:
        ac.ramp("cutoff", 0, sec.length, *{
            "intro": (650, 900), "groove": (1100, 1700),
            "drop": (3800, 4200), "break": (650, 2900),
            "final": (4200, 2800)}[kind])
        pc.ramp("cutoff", 0, sec.length,
                650 if kind in ("intro", "break") else 1800,
                2500 if kind in ("drop", "final") else 2000)
    # Only the full drops use maximum pad spread.
    pc.ramp("fx1:spread", 0, sec.length,
            1 if kind in ("drop", "final") else 0.5,
            1 if kind in ("drop", "final") else 0.7)

for sec, kind in zip(song.sections, ["intro", "groove", "build", "drop", "break", "final"]):
    arrange(sec, kind)
song.master(subsonic=True, fx=[fx("limiter2", gain=6, ceil=-1.8, look=2, rel=0.12)])
# The closing chord and kick strike on bar 46; silence follows on the
# next downbeat. A brief tail fade prevents truncating the room abruptly.
song.ramp = False
project = song.save(ROOT / "songs/sodium_uv.slab")

def write_pcm24(path, x, sr):
    q = np.clip(np.rint(x * 8388608), -8388608, 8388607).astype(np.int32).ravel()
    b = np.column_stack((q & 255, (q >> 8) & 255, (q >> 16) & 255)).astype(np.uint8)
    with wave.open(str(path), "wb") as w:
        w.setparams((2, 3, sr, len(x), "NONE", "not compressed"))
        w.writeframes(b.tobytes())

def render():
    OUT.mkdir(exist_ok=True)
    slab = ROOT / "zig-out/bin/slab"
    full = OUT / "sodium_uv_full.wav"
    wrapped = OUT / "drop_8_wrapped.wav"
    for target, options in [(full, ["--tail", "0", "--normalize", "peak:-1.3"]),
                            (wrapped, ["--range", "96:128", "--loop-wrap", "--tail", "auto",
                                       "--normalize", "peak:-1.8"])]:
        subprocess.run([str(slab), project, "--render", str(target), "--rate", "44100",
                        "--bits", "24", *options], cwd=ROOT, check=True)
    x, sr = read_wav(str(full))
    expected = round(46 * 4 * 60 / 124 * sr)
    x = x[:expected]
    fade = round(0.28 * sr)
    x[-fade:] *= np.linspace(1, 0, fade)[:, None]
    write_pcm24(full, x, sr)
    loop, sr = read_wav(str(wrapped))
    # Circularly smooth the final 16 samples, leaving the next kick attack intact.
    n = 16
    loop[-n:] += np.linspace(0, 1, n)[:, None] * (loop[0] - loop[-1])
    loop_path = OUT / "sodium_uv_drop_16bar.wav"
    write_pcm24(loop_path, np.tile(loop, (2, 1)), sr)
    wrapped.unlink()
    secs = [(s.name, s.start * 60 / 124, (s.start + s.length) * 60 / 124)
            for s in song.sections]
    report = {"full": analyze_wav(str(full), secs), "loop": analyze_wav(str(loop_path))}
    import re
    for name, path in [("full", full), ("loop", loop_path)]:
        audio, rate = read_wav(str(path))
        meter = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(path), "-af",
            "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True, check=True)
        report[name]["true_peak_db_ffmpeg"] = float(re.findall(r"Peak:\s+([-\d.]+) dBFS", meter.stderr)[-1])
        with wave.open(str(path)) as w:
            report[name]["file"] = dict(rate=w.getframerate(), bits=w.getsampwidth() * 8,
                channels=w.getnchannels(), frames=w.getnframes(), duration=w.getnframes()/rate)
    (OUT / "mix_report.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--render", action="store_true")
    if parser.parse_args().render:
        render()
