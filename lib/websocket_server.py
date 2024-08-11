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
        
        for data_key in data:

            match data_key:
                case 'user_position':
                    for user in data[data_key]:
                            # {'user_position': {'{{ user }}': {'position': this._camera.position, 'rotation': this._camera.rotation}}}
                            position = data[data_key][user]['position']
                            rotation = data[data_key][user]['rotation']
                            
                            # delete current user old coords
                            old_coordinates = users_position.pop(user, None)
                            
                            await websocket.send(json.dumps(users_position))
                            users_position.update(data[data_key])
                case _:
                    await websocket.send('Data not recognized: ', json.dumps(data))

async def main():
    try:
        async with websockets.serve(echo_messages, "localhost", 8765):
            await asyncio.Future()
    except OSError as e:
        logger.info("Websocket already started")

if __name__ == "__main__":
    asyncio.run(main())