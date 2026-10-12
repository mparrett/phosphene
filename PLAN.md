# phosphene — plan

A full-screen terminal music visualizer in let-go. Wav or mp3 in, awe out.
Winamp-plugin lineage; demoscene × linux × agentic coding × desert rave.

## Architecture

- **Decode:** `ffmpeg` → raw mono (and stereo, for XY) PCM in a temp file.
- **Analyze up front:** one pass over the track computes per-frame FFT
  bands, envelopes, beat onsets and loudness, so the render loop does no FFT
  and the effects can react a moment ahead of a kick.
- **Play:** `afplay` in the background; frames follow the wall clock from its
  start. Live input (`--mic`, or `--pcm` for Slab) skips decode and
  pre-pass: samples stream into a ring and onsets are found per hop.
- **Render:** half-block `▀` cells (fg/bg truecolor = 2 px per cell) into a
  framebuffer, written as one string per frame; braille for fine line work.
- **Keys:** `←/→` switch effect, `space` pause, `q` quit.

## Runtime direction

The full vision runs on AOT-lowered kernels; the bytecode VM, with live
editing, is a phase on the way. Don't over-tune for the VM.

- Hot loops live in kernel fns written to lower: flat `double-array`s with
  `^doubles` / `^double` / `^long` hints, `aget`/`aset`, no maps, closures or
  seqs inside the loop. nooga/let-go#1057 lowers these to native accessors
  (~230× the VM on a 1M-element sum).
- Loop bodies use `(if test (do … (recur …)) …)`, not `(when test … (recur …))`
  — the `when` spelling fails in AOT legalize (noted in #1057).
- On the VM, render at a reduced internal resolution (`--scale`) to stay
  watchable. As of 2026-10-10 the VM costs ~150 ns per primitive op and
  futures don't run in parallel.
- Deferred: shipping an AOT build that still supports eval (see #1008), which
  would bring live editing to the fast path.

## Sprint 1 — scope (tagged by the user)

Work top to bottom. Tick each box when it runs end to end on a real track.

- [x] Core: decode, analysis pass, playback sync, framebuffer + half-block
      renderer, key loop, clean terminal restore on exit/crash
- [x] **Geiss-style plasma flow** — smooth color fields pushed through a
      displacement map; bass drives flow speed
- [x] **MilkDrop-style feedback warp** — each frame zooms/rotates/fades the
      last one, a new waveform drawn on top; per-preset warp params
- [x] **AVS-style superscope** — presets are small lg fns from
      (i, n, wave sample, bands, t) → point; several built-in presets
- [x] Preset switching and crossfades between the three engines
- [x] Post FX that serve 1–3: bloom-ish glow, palette cycling
- [ ] Stretch: **live preset editor** — a legmacs-style mini editor pane where
      you edit the actual lg of a superscope/warp preset and it hot-reloads

## Backlog — demoscene sprint (later)

Tunnel · rotozoomer · plasma + copper bars · metaballs · fire (aafire) ·
voxel landscape over the scrolling spectrogram · starfield / warp jump ·
vector balls / dot sphere morphs.

## Backlog — other ideas from the original menu

G-Force/Magnetosphere particles · cava-style spectrum bars · XY Lissajous
scope · WMP kaleidoscope symmetry · laser fans over dunes · token rain ·
wavefunction interference · raymarched SDF · strange attractor · spectrogram
waterfall · CRT/chromatic-aberration post chain · beat-synced director ·
agent-style HUD strip.

## Later phase

Browser build. As of 2026-10-12, let-go's WASM build takes only key presses
from JS (`os/sh` and `net` are unavailable), so it needs an upstream sample channel:
an AudioWorklet writing into a SharedArrayBuffer ring, the same shape as
the key ring. `live.lg` already polls a ring per frame, so only its feed
changes; files would play and decode in the browser and go through that
same path. Measure the VM's frame rate under WASM first. Hosting needs
COOP/COEP headers for SharedArrayBuffer.

## Log

Each loop iteration appends one line: date, what landed, what's next.

- 2026-10-10 — core landed: ffmpeg→perl→lg decode, onset pre-pass, per-frame
  FFT features (MilkDrop-style bass/mid/treb), float RGB half-block fb with
  `--scale`, afplay sync with pause via SIGSTOP, HUD, `--dump`/`--bench`, and
  a diagnostic `scope` effect. VM: ~12–16 fps live at 160×48 cells, scale 2.
  Next: Geiss plasma.
- 2026-10-10 — plasma landed: LUT sum-of-sines kernel, domain-warped by
  bass, cosine palettes with dark troughs (ribbons on black), rotating every
  16 beats; frame blend for flow. Headless dumps now seed clock/beats from
  track time. VM: ~8–10 fps live at scale 2 (draw ~30 ms, ansi ~58 ms).
  Next: MilkDrop feedback warp.
- 2026-10-10 — milk landed: 32×18 warp mesh with per-frame and per-vertex
  preset fns (zoom/rot/dx/dy/warp/decay), bilinear resample kernel, waves
  (circle, line, pseudo-XY) alpha-blended so feedback can't run away. Four
  presets: event horizon, lightspeed, desert wind, quantum foam; rotates every
  32 beats. VM: ~10 fps at scale 2. Next: AVS superscope.
- 2026-10-10 — superscope landed: AVS-style presets as one namespace each
  under phosphene.scopes (:init/:frame/:beat/:point, :lines or :dots,
  optional MilkDrop movement under the trails), a 3D kit (rot3, proj, hue).
  Five presets: double helix, torus knot, rose bloom, orb, aurora. `--preset
  N` pins one. eval/load-string work on the VM, so the stretch editor is
  feasible. VM: ~19–21 fps live at scale 2. Next: preset switching + fades.
- 2026-10-10 — director landed: every effect×preset is a scene; auto mode
  interleaves engines and switches every 32 beats (30 s fallback); a new scene
  is seeded with the frame on screen and crossfaded over 1.5 s, so feedback
  effects morph out of the old picture. Keys ←/→, a. Next: post FX.
- 2026-10-10 — post landed: half-res bright-pass + separable box-blur bloom,
  hue-rotation matrix wobbling with treble and kicking on beats, vignette,
  beat exposure lift; runs on the displayed frame only and scenes seed from
  the pre-post frame. Keys b / c, `--no-post`. Sprint 1 done except the
  stretch editor. VM, as of today: ~15–20 fps at 160×48 cells, scale 2,
  noisy under machine load.
- 2026-10-11 — live input landed: `--mic` runs ffmpeg as a localhost PCM
  server and `--pcm PORT` attaches to any other (Slab's way in); a future
  reads `net/read!` byte-arrays into a 4 s ring, onsets run hop by hop with
  the pre-pass rule, auto-gain tracks a slow peak. A socket because lg can't
  yet read a running child's stdout. VM: 10–17 fps at 160×49 cells, scale 2,
  fed a streamed track. Next: a real mic run.
- 2026-10-12 — real mic run works; review fixes: denied-mic silence shows
  "no signal", connect waits out the macOS permission prompt, ffmpeg exits
  on its own if phosphene dies. Next: tune live input (hiss under the gain
  cap, onset thresholds).
