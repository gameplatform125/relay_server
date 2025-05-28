import asyncio
import websockets
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

rooms = {}

async def relay(websocket, path):
    try:
        # İlk mesaj: oda kodu
        room_code = await websocket.recv()
        if room_code not in rooms:
            rooms[room_code] = []
        rooms[room_code].append(websocket)
        print(f"{websocket.remote_address} joined room {room_code}")

        while True:
            msg = await websocket.recv()
            # Oda içindeki diğer herkese ilet
            for ws in rooms[room_code]:
                if ws != websocket:
                    await ws.send(msg)
    except Exception as e:
        print("Bağlantı koptu:", e)
    finally:
        # Temizlik
        if room_code in rooms:
            rooms[room_code].remove(websocket)
            if not rooms[room_code]:
                del rooms[room_code]

async def main():
    print("Relay sunucu başlatıldı, port 8765")
    async with websockets.serve(relay, "0.0.0.0", 8765):
        await asyncio.Future()  # sonsuza kadar bekle

def run_http_server():
    class Handler(BaseHTTPRequestHandler):
        def do_HEAD(self):
            self.send_response(200)
            self.end_headers()
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")
    server = HTTPServer(('0.0.0.0', 10000), Handler)
    server.serve_forever()

threading.Thread(target=run_http_server, daemon=True).start()

if __name__ == "__main__":
    asyncio.run(main()) 