#!/usr/bin/env python3
import json
import os
import sys
import argparse
from http.server import BaseHTTPRequestHandler
import socketserver
import threading
import time

try:
    import psutil
except ImportError:
    print(
        "Missing dependency: psutil\nInstall with:  pip3 install psutil",
        file=sys.stderr,
    )
    sys.exit(1)


class ThreadingTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    # Allow immediate reuse after a crash/restart to avoid Errno 48
    allow_reuse_address = True
    daemon_threads = True


def get_stats():
    """Gathers CPU and RAM statistics."""
    # Fast sample; avoids blocking the server for long periods
    cpu = psutil.cpu_percent(interval=0.2)
    ram = psutil.virtual_memory().percent
    return {"cpu_load": round(cpu, 1), "ram_load": round(ram, 1), "ok": True}


class SystemStatsHandler(BaseHTTPRequestHandler):
    """A request handler for serving system statistics."""

    server_version = "SystemStats/1.0"

    def _set_cors(self):
        """Set CORS headers for cross-origin requests."""
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def do_OPTIONS(self):
        """Handle CORS preflight requests."""
        self.send_response(204)
        self._set_cors()
        self.end_headers()

    def do_GET(self):
        """Handle GET requests for different endpoints."""
        try:
            status_code = 200
            content_type = "application/json; charset=utf-8"
            body = b""

            if self.path == "/stats":
                payload = get_stats()
                body = json.dumps(payload).encode("utf-8")
            elif self.path == "/health":
                content_type = "text/plain; charset=utf-8"
                body = b"ok"
            elif self.path == "/":
                info = {
                    "endpoints": {
                        "/stats": "JSON with cpu_load and ram_load",
                        "/health": "Plain-text health check",
                    }
                }
                body = json.dumps(info, indent=2).encode("utf-8")
            else:
                status_code = 404
                content_type = "text/plain; charset=utf-8"
                body = b"Not Found"

            self.send_response(status_code)
            if status_code == 200:
                self._set_cors()
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        except BrokenPipeError:
            # This happens when the client disconnects before the response is sent.
            # It's a common occurrence and not a server error, so we can ignore it.
            pass

    def log_message(self, fmt, *args):
        """Silence the default noisy logging."""
        return


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Simple CPU/RAM monitoring HTTP server"
    )
    parser.add_argument(
        "--host",
        default=os.environ.get("HOST", "0.0.0.0"),
        help="Host/IP to bind (default: 0.0.0.0 or $HOST)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=int(os.environ.get("PORT", "8000")),
        help="Port to listen on (default: 8000 or $PORT)",
    )
    return parser.parse_args()


def main():
    """Start the monitoring server."""
    args = parse_args()
    address = (args.host, args.port)

    try:
        with ThreadingTCPServer(address, SystemStatsHandler) as httpd:
            print(f"Monitoring server started on http://{args.host}:{args.port}")
            print("Endpoints: / (info), /stats, /health")
            print("Press Ctrl+C to stop.")
            httpd.serve_forever()
    except OSError as e:
        # Commonly: [Errno 48] Address already in use
        print(f"OSError: {e}", file=sys.stderr)
        print(
            "Tip: another process is using this port. Either kill it or run on a different port, e.g.:",
            file=sys.stderr,
        )
        print("  PORT=8010 python3 monitor.py", file=sys.stderr)
        print("  or: python3 monitor.py --port 8010", file=sys.stderr)
        sys.exit(2)
    except KeyboardInterrupt:
        print("\nStopping server...")
        # Give threads a moment to settle
        time.sleep(0.1)


if __name__ == "__main__":
    main()
