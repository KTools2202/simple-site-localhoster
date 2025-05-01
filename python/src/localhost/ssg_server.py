import os
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from contextlib import contextmanager
from typing import Dict

@contextmanager
def change_dir(target):
    prev = os.getcwd()
    os.chdir(target)
    try:
        yield
    finally:
        os.chdir(prev)

def run_ssg_server(config: Dict):
    host = config.get("host", "localhost")
    port = config.get("port", 3000)
    public_dir = config.get("public_dir", "./public")

    with change_dir(public_dir):
        handler = SimpleHTTPRequestHandler
        server = ThreadingHTTPServer((host, port), handler)
        print(f"SSG server running at http://{host}:{port}")
        server.serve_forever()