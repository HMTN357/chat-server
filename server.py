import aiohttp
from aiohttp import web
import asyncio

clients = set()

async def handle_ws(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    clients.add(ws)
    print("New client connected")

    try:
        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                print(f"Message: {msg.data}")
                for client in clients:
                    if client != ws:
                        await client.send_str(msg.data)
    except Exception as e:
        print("Error:", e)
    finally:
        clients.remove(ws)
        print("Client disconnected")

    return ws

app = web.Application()
app.router.add_get('/ws', handle_ws)

if __name__ == '__main__':
    web.run_app(app, port=8080)
