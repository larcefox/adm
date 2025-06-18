import asyncio
import websockets
import asyncpg
import hashlib
import json
from typing import Dict, Any
from loguru import logger
from lib.postgres_con import Database

logger.add('./logs/manage.log', format="{time} {level} {message}", level="INFO", retention="10 days")
users_position = {}
connected_clients = set()
db = Database()

async def notify_listener():
    await db.connect()

    async def callback(connection, pid, channel, payload):
        print(f"[DB NOTIFY] {channel} -> {payload}")
        for ws in connected_clients.copy():
            try:
                await ws.send(payload)
            except Exception as e:
                print(f"Error sending to client: {e}")
                connected_clients.remove(ws)

    await db.connection.add_listener("shape_channel", callback)
    await db.connection.add_listener("model_channel", callback)
    await db.connection.add_listener("arch_channel", callback)

    print("Listening to DB channels...")
    while True:
        await asyncio.sleep(1)  # Keep the task alive


async def get_objects(obj) -> dict:
    await db.connect()
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
    graphical_obj = {
        'entity_state': await get_objects('shape'),
        'light_state': await get_objects('light'),
        'line_state': await get_objects('line'),
        'figure_state': await get_objects('figure'),
        'model_state': await get_objects('model'),
        'arch_state': await get_objects('arch')
    }
    return graphical_obj

async def broadcast_audio(data, sender, user):
    if connected_clients:
        disconnected_clients = []
        for client in connected_clients:
            if client != sender:
                try:
                    await client.send(json.dumps({'voice': {user: data}}))
                except websockets.ConnectionClosedOK:
                    print(f"Client {client.remote_address} disconnected.")
                    disconnected_clients.append(client)
                except Exception as e:
                    print(f"Error sending audio data: {e}")
                    disconnected_clients.append(client)

        for client in disconnected_clients:
            connected_clients.remove(client)


async def echo_messages(websocket, path):
    connected_clients.add(websocket)
    print(f"Client connected: {websocket.remote_address}")

    try:
        while True:
            try:
                data = await websocket.recv()
                data = json.loads(data)
            except websockets.ConnectionClosedOK:
                print(f"Client {websocket.remote_address} disconnected.")
                break
            except Exception as e:
                print(f"Error processing message from client: {e}")
                continue

            for data_key in data:
                match data_key:
                    case 'user_position':
                        users_position.update(data[data_key])
                    case 'users_pos':
                        for user in data[data_key]:
                            other_users = {i: users_position[i] for i in users_position if i != user}
                            current_hash = dict_hash(other_users)
                            user_hash = dict_hash(data[data_key][user])
                            if current_hash != user_hash:
                                await websocket.send(json.dumps({'users_pos': other_users}))

                    case 'voice':
                        for user in data[data_key]:
                            encoded_data = data[data_key][user]
                            await broadcast_audio(encoded_data, websocket, user)

                    case 'all_3d_data':
                        print('got_all_3d_request')
                        graphical_obj = await get_graphical_obj()
                        await websocket.send(json.dumps({data_key: graphical_obj}))

                        print(f'data sended')

                    case _:
                        if data_key in graphical_obj and graphical_obj[data_key]:
                            await websocket.send(json.dumps({data_key: graphical_obj[data_key]}))
                        else:
                            print(data_key, 'Object key not found!')

    finally:
        connected_clients.remove(websocket)


async def main():
    try:
        logger.info("Starting WebSocket server and DB listener")
        server = websockets.serve(echo_messages, "127.0.0.1", 8765)
        await asyncio.gather(
            server,
            notify_listener()
        )
    except OSError as e:
        logger.error(f"WebSocket error, may be already started: {e}")


def dict_hash(dictionary: Dict[str, Any]) -> str:
    """MD5 hash of a dictionary."""
    dhash = hashlib.md5()
    encoded = json.dumps(dictionary, sort_keys=True).encode()
    dhash.update(encoded)
    return dhash.hexdigest()


def run_websocket():
    logger.info("Starting thread")
    asyncio.run(main())


if __name__ == "__main__":
    run_websocket()
