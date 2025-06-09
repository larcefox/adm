#!/usr/bin/python
import json
import math
from domains.entity_class import Entity_fabric as ef
from domains.entity_class import Entity
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

        model = mf.create('model_obj', path='coffee_shop/scene.glb')

        # Основание башни
        base = ef.create('cylinder',
                         radiusTop=5, radiusBottom=10, height=10,
                         position={'x': 0, 'y': 5, 'z': 0},
                         color=0x888888)

        # Средняя секция
        middle = ef.create('cylinder',
                           radiusTop=3, radiusBottom=5, height=30,
                           position={'x': 0, 'y': 25, 'z': 0},
                           color=0x999999)

        # Верхняя секция
        top = ef.create('cylinder',
                        radiusTop=1, radiusBottom=3, height=20,
                        position={'x': 0, 'y': 50, 'z': 0},
                        color=0xaaaaaa)

        # Антенна
        antenna = ef.create('cone',
                            radius=1, height=10,
                            position={'x': 0, 'y': 65, 'z': 0},
                            color=0xff0000)

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
                                query = f"INSERT INTO world.{element} (data, user_id) VALUES ('{pice_json}', 'c55f8791-65f9-4a29-8f46-bc5e618fd0dd')"
                                print(query)
                                data = await db.execute_query(query)
                                print(data)
      
        # Disconnect from the database
        await db.disconnect()


if __name__ == "__main__":
        asyncio.run(main())