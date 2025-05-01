import os
import importlib.util
import sys
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Dict

def run_ssr_server(config: Dict):
    host = config.get("host", "localhost")
    port = config.get("port", 3000)
    # Use "ssr_dir" for dynamic functions and "ssg_dir" for static assets.
    ssr_dir = config.get("ssr_dir", "./server")
    public_dir = config.get("ssg_dir", "./dist")

    class SSRHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            # First, try to serve a static asset if it exists.
            request_path = urllib.parse.unquote(self.path)
            # clean the path and join with public_dir
            static_path = os.path.join(public_dir, request_path.lstrip("/"))
            if os.path.isfile(static_path):
                try:
                    with open(static_path, 'rb') as f:
                        content = f.read()
                    self.send_response(200)
                    self.send_header("Content-Length", str(len(content)))
                    # A simplistic content type; you may enhance this logic as needed.
                    self.send_header("Content-Type", "application/octet-stream")
                    self.end_headers()
                    self.wfile.write(content)
                    return
                except Exception as e:
                    self.send_error(500, f"Static file error: {str(e)}")
                    return

            # Otherwise, try dynamic SSR via handler
            try:
                handler_path = os.path.join(ssr_dir, "handler.py")
                spec = importlib.util.spec_from_file_location("handler", handler_path)
                if not spec or not spec.loader:
                    raise ImportError("Could not load SSR handler module.")
                module = importlib.util.module_from_spec(spec)
                sys.modules["handler"] = module
                spec.loader.exec_module(module)
                if hasattr(module, "handle_request"):
                    module.handle_request(self)
                else:
                    raise Exception("SSR handler missing handle_request(self) function.")
            except Exception as e:
                print("SSR Error:", e)
                self.send_error(500, "Internal Server Error")

    server = HTTPServer((host, port), SSRHandler)
    print(f"SSR server running at http://{host}:{port}")
    server.serve_forever()