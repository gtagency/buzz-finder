from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from bot import Bot, PLAYER1, PLAYER2
class Handler(BaseHTTPRequestHandler):
    def _serve_headers(self, status_code = 200, content = 'text/html'):
        self.send_response(status_code)
        self.send_header('Content-type', content)
        self.end_headers()


    def do_GET(self):
        print("get recieved")
        path = self.path.split('/')
        if path[1] == '':
            #serve home
            self._serve_headers()
            with open('index.html', 'rb') as f:
                index = f.read()
            self.wfile.write(index)
        elif path[1] == 'next':
            #serve request
            self._serve_headers(content = 'application/json')

        elif path[1] == 'js' and path[2] == 'game.js':
            self._serve_headers(content = 'application/javascript')
            with open('js/game.js', 'rb') as f:
                game = f.read()
            self.wfile.write(game)

if __name__ == '__main__':
    #init bot
    # bot = Bot(PLAYER1)


    #init server
    httpd = HTTPServer(('', 8000), Handler)
    print("starting server at http://localhost:8000/")
    httpd.serve_forever()
