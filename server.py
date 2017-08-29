from http.server import HTTPServer, BaseHTTPRequestHandler
from collections import namedtuple
import json
from bot import Game

game = Game()

class Handler(BaseHTTPRequestHandler):
    def _serve_headers(self, status_code = 200, content = 'text/html'):
        self.send_response(status_code)
        self.send_header('Content-type', content)
        self.end_headers()

    def serve_json(self, data):
        self._serve_headers(content = 'application/json')
        self.wfile.write(bytes(json.dumps(data), 'UTF-8'))

    def do_GET(self):
        path = self.path.split('/')
        if path[1] == '':
            #reset game
            game.reset()
            self._serve_headers()
            with open('index.html', 'rb') as f:
                index = f.read()
            self.wfile.write(index)
        elif path[1] == 'js' and path[2] == 'game.js':
            self._serve_headers(content = 'application/javascript')
            with open('js/game.js', 'rb') as f:
                js = f.read()
            self.wfile.write(js)
        elif path[1] == 'js' and path[2].endswith('.png'):
            self._serve_headers(content = 'image/png')
            with open('js/' + path[2], 'rb') as f:
                png = f.read()
            self.wfile.write(png)
        elif path[1] == 'solve':
            self.serve_json(game.solve());

    def log_message(self, format, *args):
        return 

if __name__ == '__main__':
    #init server
    httpd = HTTPServer(('', 8000), Handler)
    print("starting server at http://localhost:8000/")
    httpd.serve_forever()
