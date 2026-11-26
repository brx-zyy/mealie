from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.server.server_port == 8080:
            body = b"""<!doctype html><title>challenge</title>
<script>window.location.href='http://internal-proof:8081/proof';</script>"""
            self.send_response(503)
            self.send_header("Content-Type", "text/html")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            print("PRIVATE_PROOF_REQUEST_RECEIVED path=" + self.path, flush=True)
            body = b"""<!doctype html>
<html><head><title>Private proof</title>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Recipe",
  "name": "INTERNAL_ONLY_PROOF_MARKER_7f31c9",
  "description": "Recipe content fetched from an unallowlisted private service.",
  "recipeYield": "1 serving",
  "recipeIngredient": ["1 cup proof ingredient"],
  "recipeInstructions": [{"@type": "HowToStep", "text": "Private response was parsed."}]
}
</script></head><body>private service response</body></html>"""
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

    def log_message(self, fmt, *args):
        print(fmt % args, flush=True)


def serve(port):
    ThreadingHTTPServer(("0.0.0.0", port), Handler).serve_forever()


Thread(target=serve, args=(8080,), daemon=True).start()
serve(8081)
