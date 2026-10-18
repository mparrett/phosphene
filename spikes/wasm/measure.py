"""Loads the spike page in headless Chromium once per query string and prints
worker- and page-side frame rates. Usage: measure.py BASE_URL QUERY..."""
import json
import sys

from playwright.sync_api import sync_playwright

base, queries = sys.argv[1], sys.argv[2:]
with sync_playwright() as p:
    browser = p.chromium.launch(args=["--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"])
    for q in queries:
        page = browser.new_page(viewport={"width": 1280, "height": 800})
        errors = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.on("console", lambda m: m.type == "error" and errors.append(m.text))
        page.goto(f"{base}/?{q}")
        try:
            page.wait_for_function("window.__phos && window.__phos.done", timeout=240_000)
            # Let queued terminal writes drain before reading the page counters.
            page.wait_for_timeout(1500)
        except Exception as e:
            errors.append(f"timeout: {e}")
        st = page.evaluate("window.__phos")
        span = (st["lastDraw"] - st["firstDraw"]) / 1000 if st.get("firstDraw") else 0
        page_fps = (st["drawn"] - 1) / span if span > 0 else 0
        d = st.get("done") or {}
        print(json.dumps({
            "q": q, "mode": st.get("mode"), "gl": st.get("gl"),
            "label": d.get("label"),
            "load_s": round((st.get("bootAt") or 0) / 1000, 1),
            "worker_fps": round(d.get("fps", 0), 1),
            "sim_ms": round(d.get("sim-ms", 0), 1), "out_ms": round(d.get("out-ms", 0), 1),
            "drawn": st["drawn"], "page_fps": round(page_fps, 1),
            "errors": errors[:3],
        }), flush=True)
        if "shot" in q:
            page.screenshot(path=f"shot-{q.replace('&', '_').replace('=', '-')}.png")
        page.close()
    browser.close()
