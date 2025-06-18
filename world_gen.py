#!/usr/bin/python
import json
import math
from domains.entity_class import Entity_fabric as ef
from domains.entity_class import Entity, Light, AmbientLight
from domains.model_class import ModelFabric as mf
from domains.model_class import Model
from domains.arch_class import ArchFabric as af
from domains.arch_class import Arch
from lib.pnoise_map import MapGen
from lib.postgres_con import Database
import asyncio
import random


noise_map = MapGen()
terrain = noise_map.map_gen()

def send_data():
    # Пример 3D модели
    model = mf.create('model_obj', path='coffee_shop/scene.glb', position={'x':50, 'y': 0, 'z': 0}, scale={'x':10, 'y': 10, 'z': 10})

    # Пример 3D модели
    model = mf.create('model_obj', path='doom_guy/doom_guy.glb', position={'x':0, 'y': 0, 'z': 0}, scale={'x':10, 'y': 10, 'z': 10})

    directional_light = ef.create('light')
    ambient_light = ef.create('light', light_type='AmbientLight')

    spacing = 80
    y_position = 25

    plane = ef.create(
            'plane',
            630,
            630,
            texture='textures/map.svg',
            color=0xffffff,
            position={'x':0, 'y': 0, 'z': 0},
            rotation={'x': 0,'y': 0, 'z': 0}
            )

    box = ef.create('box',
              width=30, height=40, depth=50,
              position={'x': 0 * spacing, 'y': y_position, 'z': 0},
              color=0xff0000,
              )

    ef.create('sphere',
              radius=20, widthSegments=32, heightSegments=32,
              position={'x': 1 * spacing, 'y': y_position, 'z': 0},
              color=0x00ff00)

    ef.create('plane',
              width=60, height=60,
              position={'x': 2 * spacing, 'y': y_position, 'z': 0},
              color=0x0000ff)

    ef.create('cylinder',
              radiusTop=15, radiusBottom=15, height=60,
              radialSegments=16, heightSegments=4,
              position={'x': 3 * spacing, 'y': y_position, 'z': 0},
              color=0xffff00)

    ef.create('cone',
              radius=15, height=150,
              radialSegments=16, heightSegments=4,
              position={'x': 4 * spacing, 'y': y_position, 'z': 0},
              color=0xff00ff)

    ef.create('torus',
              radius=20, tube=6,
              radialSegments=16, tubularSegments=150,
              position={'x': 5 * spacing, 'y': y_position, 'z': 0},
              color=0x00ffff)

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
    
async def main():
        elements = send_data()
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