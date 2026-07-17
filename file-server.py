import http.server
import mimetypes
import os
import urllib.parse

ROOT = "/data"
BOT_API_DATA_DIR = "var/lib/telegram-bot-api/"
DELETE_AFTER_SERVE = os.environ.get("DELETE_AFTER_SERVE", "0") == "1"

MAGIC_SIGNATURES = [
    (b"\xff\xd8\xff", "image/jpeg"),
    (b"\x89PNG\r\n\x1a\n", "image/png"),
    (b"GIF87a", "image/gif"),
    (b"GIF89a", "image/gif"),
    (b"%PDF", "application/pdf"),
    (b"OggS", "application/ogg"),
    (b"ID3", "audio/mpeg"),
    (b"PK\x03\x04", "application/zip"),
]


def guess_content_type(path):
    ext_type = mimetypes.guess_type(path)[0]
    if ext_type:
        return ext_type

    with open(path, "rb") as f:
        head = f.read(16)

    if len(head) >= 8 and head[4:8] == b"ftyp":
        return "video/mp4"
    if head[:4] == b"RIFF" and head[8:12] == b"WEBP":
        return "image/webp"
    for sig, mime in MAGIC_SIGNATURES:
        if head.startswith(sig):
            return mime

    return "application/octet-stream"


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        rel_path = urllib.parse.unquote(self.path.lstrip("/"))
        if rel_path.startswith(BOT_API_DATA_DIR):
            rel_path = rel_path[len(BOT_API_DATA_DIR):]
        full_path = os.path.realpath(os.path.join(ROOT, rel_path))

        if not full_path.startswith(os.path.realpath(ROOT) + os.sep):
            self.send_error(403)
            return
        if not os.path.isfile(full_path):
            self.send_error(404)
            return

        size = os.path.getsize(full_path)
        content_type = guess_content_type(full_path)

        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(size))
        self.end_headers()

        with open(full_path, "rb") as f:
            while chunk := f.read(65536):
                self.wfile.write(chunk)

        if DELETE_AFTER_SERVE:
            os.remove(full_path)

    def log_message(self, format, *args):
        pass


if __name__ == "__main__":
    http.server.ThreadingHTTPServer(("0.0.0.0", 80), Handler).serve_forever()
