from http.server import HTTPServer, SimpleHTTPRequestHandler
httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
print('HTTP static server listen on http://localhost:8000')
httpd.serve_forever()