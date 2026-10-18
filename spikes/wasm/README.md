# WASM frame-rate spike

How fast phosphene's render loop runs in a browser, before any audio bridge
exists. `web.lg` synthesizes a 20 s track in lg, then runs listen → director →
output flat out and reports timings through `js/emit`.

    PHOS_SKIP=1 LETGO_USE_TINYGO=1 LETGO_TINYGO_OPT=2 lg -source-paths src \
      -w .out/page -w-shell spikes/wasm/shell.html spikes/wasm/web.lg
    python3 spikes/wasm/serve.py .out/page 8765        # COOP/COEP headers
    uv run --with playwright python spikes/wasm/measure.py http://127.0.0.1:8765 \
      'out=canvas&w=80&h=48&fx=plasma&frames=60'

Query: `out=canvas|ansi|none`, `w`/`h` (canvas px), `cols`/`rows`/`scale`
(ansi), `fx=plasma|milk|superscope`, `frames`, `post=0`. Natively, the same
keys are read from `PHOS_<KEY>`.

## Results, 2026-10-18

let-go `main` at b8258829 plus nooga/let-go#1076 and #1077, TinyGo 0.42.0,
headless Chromium, M-series laptop under a load average of 3–12 from other
work, so treat these as ±30%. fps is frames produced and drawn, single runs.

At the terminal's resolution (80×48 px, i.e. 160×48 cells at `--scale 2`),
canvas output:

| build                    | plasma | milk | superscope |
|--------------------------|-------:|-----:|-----------:|
| browser, VM, TinyGo      |   10.7 |  7.4 |       11.6 |

At 160×96 px (four times the pixels):

| build                          | plasma | milk | superscope |
|--------------------------------|-------:|-----:|-----------:|
| native, VM                     |   10.4 |  5.6 |       11.3 |
| native, `lg compile`           |   25.0 | 12.4 |       36.2 |
| browser, VM, stock Go          |    1.3 |    — |        1.7 |
| browser, VM, TinyGo            |    2.8 |    — |        3.4 |
| Node, `lg compile`, stock Go   |    2.1 |  1.2 |        6.5 |
| Node, `lg compile`, TinyGo     |    4.7 |  2.7 |       11.0 |

- Stock Go's WASM port runs this code 10–15× slower than native, VM or
  compiled alike; even the plain synth loop takes 13 s against 0.8 s.
  TinyGo halves that.
- Canvas beats the terminal. ANSI encoding cost 75 ms a frame at 80×48
  against 10 ms to pack RGBA (TinyGo, superscope: 7.0 fps through
  xterm.js with WebGL, against 11.6 on canvas).
- `lg compile` is 2–3× the VM natively and about 1.7× in WASM, far short of
  plain Go: most arithmetic in phosphene's kernels still goes through boxed
  `rt.*Value` calls.
- The page is 2.6 MB with TinyGo, 8.5 MB with stock Go. TinyGo's build takes
  ~100 s against ~15 s.

## let-go issues found

- **`lg compile` emits Go that doesn't type-check** for `aget`, `alength`
  and `byte-array` when the result lands in a typed local but the call goes
  through the generic `rt.Core*f` fallback: 37 sites across fft, audio,
  plasma, milk and post. Reproduces on `main` at b8258829; the commit before
  #1057 (d0108ba6) compiles cleanly. The Node numbers above wrap those call
  sites by hand.
- **`lg compile` imports namespaces it skipped.** An input with "no lowerable
  defns" (the `scopes/*` presets) is still imported in `main.go`, so the build
  fails; leaving those files out of the inputs works.
