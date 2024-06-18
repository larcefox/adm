import asyncio
import websockets

async def echo_messages(websocket, path):
    while True:
        data = await websocket.recv()
        await websocket.send(data + "1тевирП")

async def main():
    async with websockets.serve(echo_messages, "localhost", 8765):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())