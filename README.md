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
    bin/phosphene --mic                   # system input; or --mic 1, --mic "MacBook Air Microphone"
    bin/phosphene --pcm 4000              # s16le mono 22050 Hz from a TCP server on localhost

Needs `lg` (let-go ≥ 1.13), `ffmpeg`, `perl`, and `afplay` (macOS) for playback.
`scripts/mk-test-track.py out.wav` writes a 40 s, 124 BPM test track.

## Music

[`music/sodium-uv/`](music/sodium-uv/) holds *Sodium / UV*, a 124 BPM melodic
techno cue composed for phosphene in [Slab](https://github.com/nooga/slab), a
livecoded macOS DAW by [@nooga](https://github.com/nooga)
([site](https://slab-site-three.vercel.app/#listen)). It comes as a full
89-second track and a 16-bar loop of the drop, both lossless FLAC, along with
the editable Slab project. The music is
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); the code is MIT.

    bin/phosphene music/sodium-uv/sodium_uv_full.flac

To just listen: [phosphene.aibuilds.me/sodium-uv.mp3](https://phosphene.aibuilds.me/sodium-uv.mp3).

## Limitations

- **Playback is macOS only.** It shells out to `afplay`; on Linux the visuals
  run but there's no sound until an `aplay` (or similar) path lands.
- **Terminal only.** There's no browser build yet. let-go can compile to a
  WASM page, but phosphene shells out to ffmpeg, so a browser version needs a
  way to pass audio from JS into lg.
- **Mic input is macOS only** (ffmpeg's avfoundation). macOS grants mic access
  to the terminal app, or under tmux to whichever app started the tmux server;
  if it's denied, ffmpeg delivers silence and the HUD shows "no signal". Live
  input has no lookahead, so beats register as they land.
- **Speed.** On the let-go VM it runs at roughly 10–20 fps at 160×48 cells
  (measured 2026-10-10); the hot loops are written for let-go's AOT
  compiler, which is where smooth frame rates are meant to come from.

See [PLAN.md](PLAN.md) for scope, the runtime direction (VM now, AOT kernels
next), and the backlog.
