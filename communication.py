import asyncio
import json
import threading
import websockets
from settings import *
from queue import Queue

class CommunicationServer:
    def __init__(self):
        self.clients = set()
        self.command_queue = Queue()
        self.loop = None
        self.thread = None
        self.running = False
    def start(self):
        self.thread = threading.Thread(target=self._run_server,
                                       daemon = True)
        self.thread.start()


    def _run_server(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.running = True
        self.loop.run_until_complete(self._server())

    async def _server(self):
        async with websockets.serve(self._handle_client,WEBSOCKET_HOST,WEBSOCKET_PORT):
            print(f"[WEB] WebSocket server is running at "
                  f"ws://{WEBSOCKET_HOST}:{WEBSOCKET_PORT}")
            await asyncio.Future()

    async def _handle_client(self,websocket,path=None):
        self.clients.add(websocket)
        print("[WEB] Mission Control Connected")
        try: 
            async for message in websocket:
                try:
                    data= json.loads(message)
                    await self.command_queue.put(data)
                except json.JSONDecodeError:
                    print("[WEB] INVALID json RECIEVED.")    
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            self.clients.discard(websocket)
            print("[WEB] Missin Contro Disconnected")

    def broadcast_state(self,state):
        if not self.loop:
            return
        if not self.clients:
            return
        message = json.dumps(state)
        asyncio.run_coroutine_threadsafe(self._broadcast(message),self.loop)

    async def _broadcast(self,message):
        if not self.clients:
            return
        disconnected = set()
        for client in self.clients:
            try:
                await client.send(message)
            except Exception:
                disconnected.add(client)

        for client in disconnected:
            self.clients.discard(client)

    #recieve commands
    def get_commands(self):
        commands=[]
        if not self.loop:
            return commands
        while not self.command_queue.empty():
            try:
                command=(self.command_queue.get_nowait())
                commands.append(command)
            except asyncio.QueueEmpty:
                break

        return commands
        