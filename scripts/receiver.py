"""Local-only receiver (approved by the user 2026-10-17): page JS in the signed-in browser POSTs collected data here,
and it is written under benchmark-data/_incoming/<path>. Binds 127.0.0.1 only; refuses paths outside _incoming."""
import http.server, os, sys

ROOT = os.path.realpath(os.path.expanduser('~/Desktop/benchmark/benchmark-data/_incoming'))
RELAY = b'''<!doctype html><title>benchmark relay</title><body>relay ready<script>
window.addEventListener('message', async (e) => {
  const d = e.data || {};
  if (!d.path) return;
  try { const r = await fetch('/' + d.path, {method: 'POST', body: d.body}); e.source.postMessage({ack: d.id, ok: r.ok}, '*'); }
  catch (err) { e.source.postMessage({ack: d.id, ok: false, err: String(err)}, '*'); }
});
if (window.opener) window.opener.postMessage({relayReady: true}, '*');
</script></body>'''


class H(http.server.BaseHTTPRequestHandler):
    def _cors(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS, GET')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.send_header('Access-Control-Allow-Private-Network', 'true')

    def do_OPTIONS(self):
        self.send_response(204); self._cors(); self.end_headers()

    def do_GET(self):
        # /relay.html: for sites whose CSP blocks connect-src to localhost, the page opens this as a popup and hands it
        # data via postMessage; the relay POSTs it to its own origin (this receiver) and acks back.
        self.send_response(200); self._cors()
        if self.path.startswith('/relay.html'):
            self.send_header('Content-Type', 'text/html'); self.end_headers(); self.wfile.write(RELAY); return
        self.end_headers(); self.wfile.write(b'ok')

    def do_POST(self):
        from urllib.parse import unquote
        p = os.path.realpath(os.path.join(ROOT, unquote(self.path.split('?')[0]).lstrip('/')))
        if not p.startswith(ROOT + os.sep):
            self.send_response(400); self._cors(); self.end_headers(); return
        data = self.rfile.read(int(self.headers.get('Content-Length', 0)))
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, 'wb') as f:
            f.write(data)
        self.send_response(200); self._cors(); self.end_headers(); self.wfile.write(str(len(data)).encode())

    def log_message(self, *a):
        pass


os.makedirs(ROOT, exist_ok=True)
http.server.ThreadingHTTPServer(('127.0.0.1', int(sys.argv[1]) if len(sys.argv) > 1 else 8765), H).serve_forever()
