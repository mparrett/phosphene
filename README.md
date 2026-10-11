# phosphene

A full-screen terminal music visualizer written in [let-go](https://github.com/nooga/let-go).
Winamp-plugin lineage: Geiss plasma, MilkDrop feedback warp, AVS superscopes.

![phosphene: a plasma scene handing off to MilkDrop feedback, then three superscope and warp presets](docs/tour.gif)

Rendered headless from the repo at 192×54 cells. The [dev log](https://phosphene.aibuilds.me) walks through how each engine works.

    bin/phosphene track.mp3               # live; scenes change every 32 beats
                                          # ←/→ scene, a auto, b bloom, c colour cycle,
                                          # space pause, q quit
    bin/phosphene track.mp3 --fx milk --preset 2   # pin one scene
    bin/phosphene track.mp3 --scale 1     # full half-block resolution (slower on the VM)
    bin/phosphene track.mp3 --dump 12.5 frame.ppm --size 160x48
    bin/phosphene track.mp3 --bench 60

Needs `lg` (let-go ≥ 1.13), `ffmpeg`, `perl`, and `afplay` (macOS) for playback.
`scripts/mk-test-track.py out.wav` writes a 40 s, 124 BPM test track.

## Limitations

- **Playback is macOS only.** It shells out to `afplay`; on Linux the visuals
  run but there's no sound until an `aplay` (or similar) path lands.
- **Terminal only, file input only.** There's no browser build yet. let-go can
  compile to a WASM page, but phosphene shells out to ffmpeg and analyses the
  whole track up front, so a browser or microphone version needs live,
  frame-by-frame analysis and a way to pass audio from JS into lg.
- **Speed.** On the let-go VM it runs at roughly 10–20 fps at 160×48 cells
  (measured 2026-10-10); the hot loops are written for let-go's AOT
  compiler, which is where smooth frame rates are meant to come from.

See [PLAN.md](PLAN.md) for scope, the runtime direction (VM now, AOT kernels
next), and the backlog.
