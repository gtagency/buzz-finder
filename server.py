from http.server import HTTPServer, BaseHTTPRequestHandler
from collections import namedtuple
import json
from bot import Bot, PLAYER1, PLAYER2, Game

Config = namedtuple('Config', ['game'])
config = Config(Game(Bot(PLAYER1), Bot(PLAYER2)))

class Handler(BaseHTTPRequestHandler):
    def _serve_headers(self, status_code = 200, content = 'text/html'):
        self.send_response(status_code)
        self.send_header('Content-type', content)
        self.end_headers()

    def serve_json(self, data):
        self._serve_headers(content = 'application/json')
        self.wfile.write(bytes(json.dumps(data), 'UTF-8'))

    def do_GET(self):
        print(self.path)
        path = self.path.split('/')
        if path[1] == '':
            #reset game
            config.game.reset()
            self._serve_headers()
            with open('index.html', 'rb') as f:
                index = f.read()
            self.wfile.write(index)
        elif path[1] == 'next':
            self.serve_json(config.game.move())
        elif path[1] == 'state':
            self.serve_json(config.game.get_state())
        elif path[1] == 'js' and path[2] == 'game.js':
            self._serve_headers(content = 'application/javascript')
            with open('js/game.js', 'rb') as f:
                game = f.read()
            self.wfile.write(game)

if __name__ == '__main__':
    #init server
    httpd = HTTPServer(('', 8000), Handler)
    print("starting server at http://localhost:8000/")
    httpd.serve_forever()
