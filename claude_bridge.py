#!/usr/bin/env python3
"""
Local Claude CLI bridge for the IHR Well Economics dashboard.

Run this on your own computer (needs the Claude Code CLI installed & logged in):

    python3 claude_bridge.py            # listens on http://localhost:8787

Then open the dashboard and use the "Ask Fable" box — it auto-detects the bridge.
Queries run through YOUR Claude login via `claude -p`; nothing else is exposed.
Press Ctrl+C to stop. Only listens on localhost.
"""
import json, subprocess, sys
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT = 8787
CLAUDE = "claude"  # or full path, e.g. /usr/local/bin/claude

class H(BaseHTTPRequestHandler):
    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Private-Network", "true")

    def do_OPTIONS(self):
        self.send_response(204); self._cors(); self.end_headers()

    def do_POST(self):
        if self.path.rstrip("/") != "/ask":
            self.send_response(404); self._cors(); self.end_headers(); return
        n = int(self.headers.get("Content-Length", 0))
        try:
            body = json.loads(self.rfile.read(n) or b"{}")
            prompt = body.get("prompt", "")
            p = subprocess.run([CLAUDE, "-p", "--output-format", "json"],
                               input=prompt.encode(), capture_output=True, timeout=180)
            out = p.stdout.decode(errors="replace").strip()
            try:
                j = json.loads(out)
                result = j.get("result") or j.get("text") or out
            except Exception:
                result = out or p.stderr.decode(errors="replace")[:500]
            resp = json.dumps({"result": result}).encode()
            self.send_response(200); self._cors()
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(resp)))
            self.end_headers(); self.wfile.write(resp)
        except Exception as e:
            resp = json.dumps({"error": str(e)}).encode()
            self.send_response(500); self._cors()
            self.send_header("Content-Type", "application/json")
            self.end_headers(); self.wfile.write(resp)

    def log_message(self, *a):  # quieter
        sys.stderr.write("bridge: %s\n" % (a[1] if len(a) > 1 else a))

if __name__ == "__main__":
    print(f"Claude bridge listening on http://localhost:{PORT} — leave this running, Ctrl+C to stop.")
    HTTPServer(("127.0.0.1", PORT), H).serve_forever()
