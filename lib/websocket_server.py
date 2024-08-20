from typing import Dict, Any
import asyncio
import websockets
from loguru import logger
import json
import hashlib
import asyncio
from lib.postgres_con import Database


logger.add('./logs/manage.log', format="{time} {level} {message}", level="INFO", retention="10 days")
users_position = {}
entity_state = {}
db = Database()


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
                case 'entity_state':
                    
                    # Geting entity data from db
                    # SELECT data FROM world.entity WHERE data ?| 'Shape%'
                    query = """
                        SELECT data FROM world.entity WHERE data ?| 
                            array(SELECT ARRAY (SELECT key FROM  world.entity, lateral jsonb_each_text(data) WHERE key LIKE 'Shape%'))
                        ;
                        """
                    entity_db_data = await db.execute_query(query)
                    if entity_db_data:
                        for row in entity_db_data:
                            print(dict(row)['data'])
                            entity_state.update(json.loads(dict(row)['data']))

                        for user in data[data_key]:
                            current_hash = dict_hash(entity_state)
                            user_hash = dict_hash(data[data_key][user])
                            print(current_hash, entity_state)
                            print(user_hash, data[data_key][user])
                            if current_hash == user_hash:
                                print('equial')
                                pass
                            else:
                                print('not equial')
                                await websocket.send(json.dumps({'entity_state': entity_state}))
                case _:
                    await websocket.send('Data not recognized: ', json.dumps(data))

async def main():
    await db.connect()
    try:
        logger.info("Trying to use port and host")
        async with websockets.serve(echo_messages, "localhost", 8765):
            await asyncio.Future()
    except OSError as e:
        logger.info("Websocket error, may be already started")
    await db.disconnect()

def dict_hash(dictionary: Dict[str, Any]) -> str:
    """MD5 hash of a dictionary."""
    dhash = hashlib.md5()
    # We need to sort arguments so {'a': 1, 'b': 2} is
    # the same as {'b': 2, 'a': 1}
    encoded = json.dumps(dictionary, sort_keys=True).encode()
    dhash.update(encoded)
    return dhash.hexdigest()

def run_websocket():
    logger.info("Starting thread")
    asyncio.run(main())

if __name__ == "__main__":
    run_websocket()