import os
import asyncio
import websockets
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

rooms = {}

async def relay(websocket):
    try:
        room_code = await websocket.recv()
        if room_code not in rooms:
            rooms[room_code] = []
        rooms[room_code].append(websocket)
        print(f"{websocket.remote_address} joined room {room_code}")

        while True:
            msg = await websocket.recv()
            for ws in rooms[room_code]:
                if ws != websocket:
                    await ws.send(msg)
    except Exception as e:
        print("Bağlantı koptu:", e)
    finally:
        if room_code in rooms:
            rooms[room_code].remove(websocket)
            if not rooms[room_code]:
                del rooms[room_code]

async def main():
    port = int(os.environ.get("PORT", 8765))  # Render'ın verdiği portu dinle
    print(f"Relay sunucu başlatıldı, port {port}")
    async with websockets.serve(relay, "0.0.0.0", port):
        await asyncio.Future()  # sonsuza kadar bekle

if __name__ == "__main__":
    asyncio.run(main())

