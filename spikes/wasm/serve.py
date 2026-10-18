"""Static server with the cross-origin isolation headers lg -w's worker mode needs."""
import http.server
import sys


class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cross-Origin-Opener-Policy", "same-origin")
        # credentialless rather than require-corp, so the xterm CDN scripts load.
        self.send_header("Cross-Origin-Embedder-Policy", "credentialless")
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 8765
    handler = lambda *a, **k: Handler(*a, directory=sys.argv[1], **k)
    http.server.ThreadingHTTPServer(("127.0.0.1", port), handler).serve_forever()
