# Sodium / UV

Original melodic techno / progressive house cue for a music visualizer,
composed for phosphene in [Slab](https://github.com/nooga/slab).
124 BPM, 4/4, F-sharp minor. Warm rolling analog bass, a glassy arp and
celesta reply, broad pads, short chord stabs, and a dry four-on-the-floor kick.

Slab delivered stereo PCM WAV, 44.1 kHz, 24-bit. They're stored here as FLAC,
which is lossless: the decoded samples are identical to the WAVs.

- `sodium_uv_full.flac`: 46 bars, 89.032 seconds.
- `sodium_uv_drop_16bar.flac`: 16 bars, 30.968 seconds. The requested main
  drop spans eight bars, so this repeats bars 25–32 twice. Delay and room
  tails are wrapped into its opening; no fade-in or fade-out. Repeat the
  entire file to loop it. Timing is within one sample of 16 bars at 124 BPM.
- `sodium_uv_full.mp3`: the full track as a 320 kbps MP3 for easy sharing,
  also at <https://phosphene.aibuilds.me/sodium-uv.mp3>.

| Bars | Time | Section |
| --- | --- | --- |
| 1–8 | 0.000–15.484 | Intro; kick from bar 1, hats from bar 5 |
| 9–16 | 15.484–30.968 | Groove; bass and offbeat hats |
| 17–24 | 30.968–46.452 | Build; opening filter, snare roll in bars 23–24 |
| 25–32 | 46.452–61.935 | Main drop; full instrumentation and pad width |
| 33–40 | 61.935–77.419 | Breakdown; pads and arp, slow filter sweep |
| 41–46 | 77.419–89.032 | Final drop; resolving hit on bar 46's downbeat |

All section entries land on eight-bar boundaries. The six-bar final phrase
preserves the requested 46-bar length. The final hit is at 87.097 seconds;
its decay fills the remaining bar, with a 280 ms tail fade to silence at
the following downbeat.

Kick and bass have no reverb. Kick-keyed compressors duck bass and pads.
Space is high-passed, and kick/bass stay centered. Master limiting and final
peak normalization preserve substantial transient headroom. See
`mix_report.json` for final loudness, peak, spectrum and stereo measurements.
The audio was checked numerically; it has not been auditioned by the agent.

Editable project: `sodium_uv.slab/`. Generator: `sodium_uv.py`, which builds
on Slab's `slabkit` and writes into a Slab checkout. To regenerate, copy both
into that checkout's `songs/` folder, then from its root, with numpy and
ffmpeg installed:

```sh
PYTHONPATH=tools python3 songs/sodium_uv.py --render
zig-out/bin/slab songs/sodium_uv.slab
```

All instruments are native Slab synths; the project needs no external
sample library.

Play it through phosphene from this repo's root:

```sh
bin/phosphene music/sodium-uv/sodium_uv_full.flac
```

## Licence

*Sodium / UV* (the audio, the Slab project and its generator) by Matt Parrett,
composed with Slab, is licensed under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). The rest of this
repository is MIT.
