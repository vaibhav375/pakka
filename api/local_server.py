"""The Build It path: python3 api/local_server.py

Wraps the Lambda handler in a stdlib HTTP server so the whole thing runs on a
laptop with no AWS account, no credentials and nothing to install. Scans are
written to a JSON file instead of DynamoDB.
"""
from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from handler import lambda_handler

PORT = 8787


class Handler(BaseHTTPRequestHandler):
    def _run(self, method: str) -> None:
        length = int(self.headers.get("content-length") or 0)
        body = self.rfile.read(length).decode() if length else ""
        result = lambda_handler(
            {"httpMethod": method, "path": self.path, "body": body}
        )
        payload = (result.get("body") or "").encode()
        self.send_response(result["statusCode"])
        for k, v in result.get("headers", {}).items():
            self.send_header(k, v)
        self.send_header("content-length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self): self._run("GET")
    def do_POST(self): self._run("POST")
    def do_OPTIONS(self): self._run("OPTIONS")
    def log_message(self, fmt, *args): print(f"  {self.command} {self.path}")


if __name__ == "__main__":
    print(f"  Pakka API on http://127.0.0.1:{PORT}  (POST /scan)")
    ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
