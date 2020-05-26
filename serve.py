import json
import asyncio
import websockets
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
from src.play_maze_world import Playground, Config

class SocketServer:

    def __init__(self):
        self.connected = set()
        self.playground = Playground()

    async def serve(self, host = 'localhost', port = 8080):
        async with websockets.serve(self.on_connected, host, port):
            print(f'Socket server listen on ws://{host}:{port}')
            await asyncio.Future()

    async def on_connected(self, websocket, path=None):
        print(websocket, path)
        self.connected.add(websocket)

        async for message in websocket:
            print('->', message)
            command, params = json.loads(message)
            output = json.dumps(self.on_message(command, params))
            print('<-', output)
            await websocket.send(output)

    def on_message(self, message, params):
        if message == 'reset':
            values, policy, world = self.playground.reset()
            return { 'values': values.tolist(), 'policy': policy.tolist(), 'world': world.tolist() }
            pass

        elif message == 'policy_evaluate':
            values = self.playground.policy_evaluate()
            return { 'values': values.tolist() }

        elif message == 'policy_update':
            policy = self.playground.policy_update()
            return { 'policy': policy.tolist() }

        elif message == 'policy_iteration':
            values, policy = self.playground.policy_iteration()
            return { 'values': values.tolist(), 'policy': policy.tolist() }

        elif message == 'value_iteration':
            values = self.playground.value_iteration()
            return { 'values': values.tolist() }

        elif message == 'config':
            cfg = Config(**params)
            self.playground.config(cfg)
            return { 'values': self.playground.values.tolist(), 'policy': self.playground.policy_probs.tolist() }

        else:
            return { 'error': 'There is no such request: ' + message}

def serve_static():
    httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
    print('HTTP server on http://localhost:8000/www/')
    httpd.serve_forever()

if __name__ == "__main__":
    # Serve static files on a separate thread
    http_thread = threading.Thread(target=serve_static)
    http_thread.daemon = True
    http_thread.start()

    # Serve python
    server = SocketServer()
    asyncio.run(server.serve())

