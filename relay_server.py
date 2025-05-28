import asyncio
import websockets

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

start_server = websockets.serve(relay, "0.0.0.0", 8765)
print("Relay sunucu başlatıldı, port 8765")
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever() 