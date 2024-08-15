from typing import Dict, Any
import asyncio
import websockets
from loguru import logger
import json
import hashlib


logger.add('./logs/manage.log', format="{time} {level} {message}", level="INFO", retention="10 days")
users_position = {}


async def echo_messages(websocket, path):
    while True:
        data = await websocket.recv()
        data = json.loads(data)
        
        for data_key in data:
            match data_key:
                
                case 'user_position':
                    users_position.update(data[data_key])
                
                case 'users_pos':
                    for user in data[data_key]:
                        other_users = {i:users_position[i] for i in users_position if i!=user}
                        current_hash = dict_hash(other_users)
                        user_hash = dict_hash(data[data_key][user])
                        if current_hash == user_hash:
                            pass
                        else:
                            await websocket.send(json.dumps({'users_pos': other_users}))
                case _:
                    await websocket.send('Data not recognized: ', json.dumps(data))

async def main():
    try:
        async with websockets.serve(echo_messages, "localhost", 8765):
            await asyncio.Future()
    except OSError as e:
        logger.info("Websocket already started")

def dict_hash(dictionary: Dict[str, Any]) -> str:
    """MD5 hash of a dictionary."""
    dhash = hashlib.md5()
    # We need to sort arguments so {'a': 1, 'b': 2} is
    # the same as {'b': 2, 'a': 1}
    encoded = json.dumps(dictionary, sort_keys=True).encode()
    dhash.update(encoded)
    return dhash.hexdigest()

if __name__ == "__main__":
    asyncio.run(main())