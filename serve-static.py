import http.server
import socketserver
#
# PORT = 8000
#
# Handler = http.server.SimpleHTTPRequestHandler
#
# with socketserver.TCPServer(("", PORT), Handler) as httpd:
#     print("serving at port", PORT)
#     httpd.serve_forever()
#

from http.server import HTTPServer, BaseHTTPRequestHandler, SimpleHTTPRequestHandler
import json
from src.play_maze_world import Playground

playground = Playground()

class HTTPRequestHandler(SimpleHTTPRequestHandler):

    def do_GET(self):
        # self.send_response(200)
        # self.end_headers()
        # self.wfile.write(b'Hello, world!')
        return SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):

        # print('----')
        # print(json.dumps(params))

        if self.path == '/server/reset':
            values = playground.reset()
            self.json_output({ 'values': values.tolist()})
            pass

        elif self.path == '/server/evaluate':
            values = playground.evaluate(render=False)
            self.json_output({ 'values': values.tolist()})

        elif self.path == '/server/sample':
            position = self.get_params()['position']
            values = playground.sample(tuple(position))
            self.json_output({ 'values': values.tolist()})

        else:
            self.json_error({ 'msg': 'There is no such request: ' + self.path}, 404)


    def get_params(self):
        content_length = int(self.headers['Content-Length'])
        params = self.rfile.read(content_length).decode('utf-8')
        return json.loads(params)

    def json_output(self, data, code = 200):
        self.send_response(code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        output = {'success': True, 'result': data }
        self.wfile.write(json.dumps(output).encode('utf-8'))


    def json_error(self, data, code = 404):
        self.send_response(code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        output = {'success': False, 'error': data}
        self.wfile.write(json.dumps(output).encode('utf-8'))


# httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
httpd = HTTPServer(('localhost', 8000), HTTPRequestHandler)
httpd.serve_forever()