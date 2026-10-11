# phosphene — plan

A full-screen terminal music visualizer in let-go. Wav or mp3 in, awe out.
Winamp-plugin lineage; demoscene × linux × agentic coding × desert rave.

## Architecture

- **Decode:** `ffmpeg` → raw mono (and stereo, for XY) PCM in a temp file.
- **Analyze up front:** one pass over the track computes per-frame FFT
  bands, envelopes, beat onsets and loudness, so the render loop does no FFT
  and the effects can react a moment ahead of a kick.
- **Play:** `afplay` in the background; frames follow the wall clock from its
  start. Slab can later replace this by streaming PCM in.
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
- [ ] **MilkDrop-style feedback warp** — each frame zooms/rotates/fades the
      last one, a new waveform drawn on top; per-preset warp params
- [ ] **AVS-style superscope** — presets are small lg fns from
      (i, n, wave sample, bands, t) → point; several built-in presets
- [ ] Preset switching and crossfades between the three engines
- [ ] Post FX that serve 1–3: bloom-ish glow, palette cycling
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

Feed live audio from Slab instead of a file.

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
