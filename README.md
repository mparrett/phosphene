# phosphene

A full-screen terminal music visualizer written in [let-go](https://github.com/nooga/let-go).
Winamp-plugin lineage: Geiss plasma, MilkDrop feedback warp, AVS superscopes.

    bin/phosphene track.mp3               # live; ←/→ effect, space pause, q quit
    bin/phosphene track.mp3 --scale 1     # full half-block resolution (slower on the VM)
    bin/phosphene track.mp3 --dump 12.5 frame.ppm --size 160x48
    bin/phosphene track.mp3 --bench 60

Needs `lg` (let-go ≥ 1.13), `ffmpeg`, `perl`, and `afplay` (macOS) for playback.
`scripts/mk-test-track.py out.wav` writes a 40 s, 124 BPM test track.

See [PLAN.md](PLAN.md) for scope, the runtime direction (VM now, AOT kernels
next), and the backlog.
