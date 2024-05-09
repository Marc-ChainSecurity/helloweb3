from http.server import *
import web3
import json
import os.path
import posixpath


class HTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("Content-Length"))
        message = json.loads(self.rfile.read(length))
        method, params = message["method"], message.get("params")
        token = posixpath.normpath(self.path).lstrip("/")
        ipc_path = os.path.join("/tmp/anvils", token)

        provider = web3.IPCProvider(ipc_path)
        response = json.dumps(provider.make_request(method, params))

        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(response.encode())


ThreadingHTTPServer(("", 8545), HTTPRequestHandler).serve_forever()
