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

async def get_objects(obj)->dict:
    db = Database()
    await db.connect()
    # Geting entity data from db
    # SELECT data FROM world.entity WHERE data ?| 'Shape%'
    query = f"""
        SELECT data FROM world.{obj} WHERE data ?| 
            array(SELECT ARRAY (SELECT key FROM  world.{obj}, lateral jsonb_each_text(data) WHERE key LIKE '{obj}%'))
        ;
        """
    db_data = await db.execute_query(query)
    await db.disconnect()
    
    dict_data = {}
    if db_data:
        for row in db_data:
            dict_data.update(json.loads(dict(row)['data']))
    return dict_data

async def get_graphical_obj():
    # Get entity from DB
    graphical_obj = {
        'entity_state': await get_objects('shape'),
        'light_state': await get_objects('light'),
        'line_state': await get_objects('line'),
        'figure_state': await get_objects('figure'),
        'model_state': await get_objects('model'),
        'arch_state': await get_objects('arch')
    }
    return graphical_obj

graphical_obj = asyncio.run(get_graphical_obj())

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
                case 'all_3d_data':
                    print('got_all_3d_request')
                    await websocket.send(json.dumps({data_key: graphical_obj}))
                    print('data sended')

                case _:
                    if data_key in graphical_obj and graphical_obj[data_key]:
                        await websocket.send(json.dumps({data_key: graphical_obj[data_key]}))
                        
                    else:
                        print(data_key, 'Object key not found!')

async def main():
    try:
        logger.info("Trying to use port and host")
        async with websockets.serve(echo_messages, "127.0.0.1", 8765):
            await asyncio.Future()
    except OSError as e:
        logger.info("Websocket error, may be already started", e)

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
