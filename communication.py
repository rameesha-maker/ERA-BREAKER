import asyncio
import json
import threading
import sys
from queue import Queue

from settings import WEBSOCKET_HOST, WEBSOCKET_PORT


WEB_MODE = sys.platform == "emscripten"


class CommunicationServer:
    def __init__(self):
        self.clients = set()
        self.command_queue = Queue()

        self.loop = None
        self.thread = None
        self.server = None
        self.stop_event = None
        self.running = False

    def start(self):
        # Never start a local websocket server in Pygbag/browser mode.
        if WEB_MODE:
            return

        self.thread = threading.Thread(
            target=self._run_server,
            daemon=True
        )
        self.thread.start()

    def _run_server(self):
        # Import websockets only on desktop.
        import websockets

        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.running = True

        try:
            self.loop.run_until_complete(self._server())
        except Exception as e:
            print("[WEB] Server error:", e)
        finally:
            self.running = False

            pending = asyncio.all_tasks(self.loop)

            for task in pending:
                task.cancel()

            try:
                self.loop.run_until_complete(
                    asyncio.gather(
                        *pending,
                        return_exceptions=True
                    )
                )
            except Exception:
                pass

            self.loop.close()
            self.loop = None

    async def _server(self):
        import websockets

        self.stop_event = asyncio.Event()

        self.server = await websockets.serve(
            self._handle_client,
            WEBSOCKET_HOST,
            WEBSOCKET_PORT
        )

        print(
            f"[WEB] WebSocket server running at "
            f"ws://{WEBSOCKET_HOST}:{WEBSOCKET_PORT}"
        )

        try:
            await self.stop_event.wait()
        finally:
            self.server.close()
            await self.server.wait_closed()
            self.server = None

    async def _handle_client(self, websocket):
        print("[WEB] Dashboard connected!")
        self.clients.add(websocket)

        try:
            async for message in websocket:
                print("[WEB] Received:", message)

                try:
                    command = json.loads(message)
                    print("[WEB] Command:", command)
                    self.command_queue.put(command)
                except json.JSONDecodeError:
                    print("[WEB] Invalid JSON received")

        except Exception as e:
            print("[WEB] Client error:", e)

        finally:
            self.clients.discard(websocket)
            print("[WEB] Dashboard disconnected")

    def get_commands(self):
        commands = []

        while not self.command_queue.empty():
            commands.append(self.command_queue.get())

        return commands

    def broadcast_state(self, state):
        if not self.clients or not self.loop:
            return

        message = json.dumps(state)

        asyncio.run_coroutine_threadsafe(
            self._broadcast(message),
            self.loop
        )

    async def _broadcast(self, message):
        disconnected = set()

        for client in self.clients:
            try:
                await client.send(message)
            except Exception:
                disconnected.add(client)

        for client in disconnected:
            self.clients.discard(client)

    def stop(self):
        if not self.loop or not self.running:
            return

        def request_shutdown():
            if self.stop_event:
                self.stop_event.set()

        try:
            self.loop.call_soon_threadsafe(request_shutdown)
        except RuntimeError:
            return

        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=2)

        self.thread = None