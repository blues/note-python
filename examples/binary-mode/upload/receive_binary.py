#!/usr/bin/env python3
"""Minimal HTTP server that receives binary files routed from Notehub.

Receives binary files via a General HTTP/HTTPS route and saves them to
the current directory.

Usage:
    python3 receive_binary.py [port]

    Default port: 8080

Setup:
    1. Run this script (optionally with ngrok to expose it publicly):
           python3 receive_binary.py
           ngrok http 8080

    2. In Notehub, create a General HTTP/HTTPS route pointing to this
       server's URL (or your ngrok URL).

    3. Send a binary file from your Notecard:
           {"req": "web.post", "route": "<your-route>", "binary": true, ...}

    Files are saved to the current directory with a name derived from the
    Notecard's "label" field, or falling back to a timestamped filename
    with an extension inferred from the file's magic bytes.
"""

import os
import sys
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

# Magic bytes used to infer file extensions
MAGIC_SIGNATURES = [
    (b"\x89PNG", "png"),
    (b"\xff\xd8\xff", "jpg"),
    (b"%PDF", "pdf"),
    (b"GIF8", "gif"),
    (b"PK\x03\x04", "zip"),
    (b"\x1f\x8b", "gz"),
]

DEFAULT_PORT = 8080


def decode_chunked(data: bytes) -> bytes:
    """Decode HTTP chunked transfer encoding."""
    output = b""
    pos = 0
    while pos < len(data):
        end = data.find(b"\r\n", pos)
        if end == -1:
            break
        size_str = data[pos:end].decode(errors="ignore").strip()
        if not size_str:
            break
        try:
            size = int(size_str, 16)
        except ValueError:
            break
        if size == 0:
            break
        pos = end + 2
        output += data[pos:pos + size]
        pos += size + 2
    return output


def infer_extension(data: bytes) -> str:
    """Infer file extension from magic bytes."""
    for magic, ext in MAGIC_SIGNATURES:
        if data[: len(magic)] == magic:
            return ext
    return "bin"


def make_filename(label: str, data: bytes) -> str:
    """Return the label if provided, or a timestamped filename."""
    if label:
        return label
    ext = infer_extension(data)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    return f"received_{timestamp}.{ext}"


class BinaryReceiveHandler(BaseHTTPRequestHandler):
    """Handle incoming binary POST requests from Notehub."""

    def do_POST(self):
        """Receive a binary file and save it to disk."""
        # Read body, handling both Content-Length and chunked encoding
        content_length = self.headers.get("Content-Length")
        transfer_encoding = self.headers.get("Transfer-Encoding", "")

        if content_length:
            raw = self.rfile.read(int(content_length))
        else:
            raw = self.rfile.read()

        if "chunked" in transfer_encoding.lower():
            body = decode_chunked(raw)
        else:
            body = raw

        if not body:
            self._respond(400, "Empty body")
            return

        # Notehub sets X-Notecard-Label to the note's label field
        label = self.headers.get("X-Notecard-Label", "").strip()
        filename = make_filename(label, body)

        filepath = os.path.join(os.getcwd(), filename)
        with open(filepath, "wb") as f:
            f.write(body)

        print(f"[{time.strftime('%H:%M:%S')}] Received {len(body):,} bytes -> {filename}")
        self._respond(200, "OK")

    def _respond(self, code: int, message: str):
        self.send_response(code)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(message.encode())

    def log_message(self, format, *args):
        """Suppress default request logging."""
        pass


def main():
    """Start the binary receive server."""
    port = int(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PORT
    server = HTTPServer(("", port), BinaryReceiveHandler)
    print(f"Listening on port {port}. Saving files to: {os.getcwd()}")
    print("Press Ctrl+C to stop.\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
