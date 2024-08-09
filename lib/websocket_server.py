import asyncio
import websockets
from loguru import logger


logger.add('./logs/manage.log', format="{time} {level} {message}", level="INFO", retention="10 days")

async def echo_messages(websocket, path):
    while True:
        data = await websocket.recv()
        match data:
            case 'get_arch':
                await websocket.send('send_arch')
            case _:
                await websocket.send(data)

async def main():
    try:
        async with websockets.serve(echo_messages, "localhost", 8765):
            await asyncio.Future()
    except OSError as e:
        logger.info("Websocket already started")

if __name__ == "__main__":
    asyncio.run(main())