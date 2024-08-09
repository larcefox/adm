import asyncio
import websockets
from loguru import logger
import json


logger.add('./logs/manage.log', format="{time} {level} {message}", level="INFO", retention="10 days")
users_position = {}


async def echo_messages(websocket, path):
    while True:
        data = await websocket.recv()
        data = json.loads(data)
        data_key = list(data.keys())[0]
        match data_key:
            case 'get_arch':
                await websocket.send('send_arch')
            case 'user_position':
                cur_coordinates = data['user_position'][0]
                user = list(cur_coordinates.keys())[0]
                old_coordinates = users_position.pop(user, None)
                await websocket.send(json.dumps(users_position))
                users_position.update(cur_coordinates)
            case _:
                # await websocket.send(json.dumps(data))
                await websocket.send('last')

async def main():
    try:
        async with websockets.serve(echo_messages, "localhost", 8765):
            await asyncio.Future()
    except OSError as e:
        logger.info("Websocket already started")

if __name__ == "__main__":
    asyncio.run(main())