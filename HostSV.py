import http.server
import socketserver

PORT = 8000

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="./Site", **kwargs)

with socketserver.TCPServer(("", 8080), Handler) as httpd:
    httpd.serve_forever()
