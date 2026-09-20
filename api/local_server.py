"""The Build It path: python3 api/local_server.py

Wraps the Lambda handler in a stdlib HTTP server so the whole thing runs on a
laptop with no AWS account, no credentials and nothing to install. Scans are
written to a JSON file instead of DynamoDB.
"""
from __future__ import annotations

import json
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from handler import lambda_handler

PORT = 8787


class Handler(BaseHTTPRequestHandler):
    def _run(self, method: str) -> None:
        length = int(self.headers.get("content-length") or 0)
        body = self.rfile.read(length).decode() if length else ""
        # A Function URL hands the handler the path and the query separately.
        # Passing self.path whole would keep the "?..." on the end of the path,
        # so a route would match in production and miss here, which is the one
        # thing this file exists to prevent.
        parsed = urllib.parse.urlsplit(self.path)
        result = lambda_handler({
            "httpMethod": method,
            "path": parsed.path,
            "rawQueryString": parsed.query,
            "queryStringParameters": {
                k: v[-1] for k, v in urllib.parse.parse_qs(parsed.query, keep_blank_values=True).items()
            },
            "headers": {k.lower(): v for k, v in self.headers.items()},
            "body": body,
        })
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
