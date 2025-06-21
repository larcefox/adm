#!/usr/bin/python
import json
import math
from domains.entity_class import Entity_fabric as ef
from domains.entity_class import Entity, Light, AmbientLight
from domains.model_class import ModelFabric as mf
from domains.model_class import Model
from domains.planet_postion_class import PlanetDataFetcher
from domains.arch_class import ArchFabric as af
from domains.arch_class import Arch
from lib.pnoise_map import MapGen
from lib.postgres_con import Database
from lib.neur_net import YandexGPTApiService
import asyncio
import random


noise_map = MapGen()
terrain = noise_map.map_gen()

def send_data():

    fetcher = PlanetDataFetcher()
    positions = fetcher.get_all_planets_data()

    for planet, data in positions.items():
        if data:

            ef.create('sphere',
                      radius=data['radius_km']/1000, widthSegments=8, heightSegments=8,
                      position={'x': data['x'] * 100, 'y': data['y'] * 100, 'z': data['z'] * 100},
                      color="#{:06x}".format(random.randint(0, 0xFFFFFF)))

        else:
            print(f"{planet}: Данные недоступны")

    plane = ef.create(
            'plane',
            630,
            630,
            texture='textures/map.svg',
            color=0xffffff,
            position={'x':0, 'y': -200, 'z': 0},
            rotation={'x': 0,'y': 0, 'z': 0}
            )

    lights = {
            light.name:
            light.return_dict() for light in Entity.manager.get_entity_list('light')
            }
    shapes = {
            entity.name:
            entity.return_dict() for entity in Entity.manager.get_entity_list('shape')
            }
    lines = {
            line.name:
            line.return_dict() for line in Entity.manager.get_entity_list('line')
            }
    figures = {
            figure.name:
            figure.return_dict() for figure in Entity.manager.get_entity_list('figure')
            }
    models = {
            model.name:
            model.return_dict() for model in Model.manager.get_model_list('model_obj')
            }
    arch = {
            arch.name:
            arch.return_dict() for arch in Arch.manager.get_arch_list('arch')
            }

    return {
            'light': lights,
            'shape': shapes,
            'line': lines,
            'figure': figures,
            'model': models,
            'arch': arch
            }

async def ai_generate_additions(session_id: str = "world_gen") -> dict:
    """Generate additional world objects via YandexGPT API."""
    service = YandexGPTApiService()
    if not service.api_key or not service.model_uri:
        print("YandexGPT credentials missing. Skipping AI generation.")
        return {
            "shape": {
                "sample_box": {
                    "type": "box",
                    "width": 1,
                    "height": 1,
                    "depth": 1,
                }
            }
        }

    prompt = (
        "Создай JSON с дополнительными объектами мира. "
        "Используй ключи 'light', 'shape', 'line', 'figure', 'model', 'arch'. "
        "Каждый ключ должен содержать словарь объектов."
    )
    try:
        response = await service.get_response(session_id, prompt)
        return json.loads(response)
    except Exception as e:
        print(f"AI generation failed: {e}")
        return {}
    
async def main():
        elements = send_data()
        ai_elements = await ai_generate_additions()
        for key, value in ai_elements.items():
                if key in elements:
                        elements[key].update(value)
                else:
                        elements[key] = value

        # Instantiate the Database class
        db = Database()

        # Connect to the database (optional, as the connection is managed automatically)
        await db.connect()

        # Execute a raw SQL query
        #query = "SELECT * FROM your_table_name WHERE some_column = $1"
        #data = await db.execute_query(query, 'some_value')

        # Print the results
        #print(data)
        
        for element in elements:
                if elements[element]:
                        for pice in elements[element]:
                                pice_json = json.dumps({pice: elements[element][pice]})
                                # нужно указать пользователя
                                query = f"INSERT INTO world.{element} (data, user_id) VALUES ('{pice_json}', '837c5740-a7d6-4aeb-b050-caad708c6607')"
                                print(query)
                                data = await db.execute_query(query)
                                print(data)
      
        # Disconnect from the database
        await db.disconnect()


if __name__ == "__main__":
        asyncio.run(main())

