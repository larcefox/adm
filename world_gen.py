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

        # Создание основания парка (зелёная плоскость)
        park_ground = ef.create('plane', 1000, 1000, position={'x': 0, 'y': 0, 'z': 0}, color='green')

        # Создание дорожек (светло-серые)
        for i in range(-500, 501, 100):
                ef.create('plane', 1000, 10, position={'x': 0, 'y': 0.01, 'z': i}, color='lightgrey')
                ef.create('plane', 10, 1000, position={'x': i, 'y': 0.01, 'z': 0}, color='lightgrey')

        # Создание деревьев
        for _ in range(200):
                x_pos = random.uniform(-500, 500)
                z_pos = random.uniform(-500, 500)
                tree_trunk = ef.create('cylinder', radiusTop=0.5, radiusBottom=0.5, height=5,
                                       position={'x': x_pos, 'y': 2.5, 'z': z_pos}, color='brown')
                tree_foliage = ef.create('sphere', radius=2, widthSegments=8, heightSegments=8,
                                         position={'x': x_pos, 'y': 7, 'z': z_pos}, color='darkgreen')

        # Создание кустов
        for _ in range(300):
                x_pos = random.uniform(-500, 500)
                z_pos = random.uniform(-500, 500)
                bush = ef.create('sphere', radius=1.2, widthSegments=6, heightSegments=6,
                                 position={'x': x_pos, 'y': 1.2, 'z': z_pos}, color='forestgreen')

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
                                query = f"INSERT INTO world.{element} (data, user_id) VALUES ('{pice_json}', 'b51d9b79-9d12-4dd8-9acc-98db5a481953')"
                                print(query)
                                data = await db.execute_query(query)
                                print(data)
      
        # Disconnect from the database
        await db.disconnect()


if __name__ == "__main__":
        asyncio.run(main())