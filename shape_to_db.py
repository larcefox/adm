import asyncio
import json
from domains.web_to_3d import convert_webpage_to_3d  # библиотека, созданная ранее
from lib.postgres_con import Database

USER_ID = 'c55f8791-65f9-4a29-8f46-bc5e618fd0dd'

def send_data():
    return convert_webpage_to_3d("https://im.systems/news/chto-takoe-integrirovannoe-biznes-planirovanie-i-kakie-biznes-effekty-ono-mo")

async def main():
    elements = send_data()
    db = Database()
    await db.connect()

    for element_type in elements:
        if elements[element_type]:
            for name, content in elements[element_type].items():
                pice_json = json.dumps({name: content})
                # Экранируем одинарные кавычки внутри JSON
                pice_json = pice_json.replace("'", "''")
                query = f"""
                INSERT INTO world.{element_type} (data, user_id)
                VALUES ('{pice_json}', '{USER_ID}')
                """
                print(query)
                result = await db.execute_query(query)
                print(result)

    await db.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
