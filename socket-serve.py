import json
import asyncio
import websockets
from src.evaluate_grid_world import Playground


class SocketServer():

    def __init__(self):
        self.connected = set()
        self.playground = Playground()

    def serve(self, host = 'localhost', port = 8080):
        sockets = websockets.serve(self.on_connected, host, port)
        print(f'Socket server listen on ws://{host}:{port}')
        loop = asyncio.get_event_loop()
        loop.run_until_complete(sockets)
        loop.run_forever()

    async def on_connected(self, websocket, path):
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
            values, policy, state = self.playground.reset()
            return { 'values': values.tolist(), 'policy': policy.tolist(), 'state': state.tolist() }
            pass

        elif message == 'evaluate':
            values, policy = self.playground.evaluate(render=False)
            return { 'values': values.tolist(), 'policy': policy.tolist() }

        elif message == 'sample':
            position = params['position']
            values, policy = self.playground.sample(tuple(position))
            return { 'values': values.tolist(), 'policy': policy.tolist() }

        else:
            return { 'error': 'There is no such request: ' + message}



# async def serve_static():
#     from http.server import HTTPServer, SimpleHTTPRequestHandler
#     httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
#     print('HTTP server on http://localhost:8000')
#     httpd.serve_forever()
# asyncio.get_event_loop().create_task(serve_static())

SocketServer().serve()

