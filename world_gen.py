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

        # directional_light = ef.create('light')
        # ambient_light = ef.create('light', light_type='AmbientLight')

        # example entity

        # plane = ef.create(
        #         'plane',
        #         630, 
        #         630,
        #         texture='textures/map.svg',
        #         color=0xffffff,
        #         position={'x':0, 'y': 0, 'z': 0},
        #         rotation={'x': -(math.pi/2),'y': 0, 'z': -(math.pi/2)}
        #         )
    
        model = mf.create('model_obj', path='coffee_shop/scene.glb')
        # box = ef.create('box', 10, 10, 10, position={'x': 0, 'y': 10, 'z': 0}, color='red')
        # map = ef.create('figure', vertices=terrain)
        # cube = af.create('cube', side_length=100)
        # wall = af.create('k_wall')
        # sphere = ef.create('sphere', 5, 15, 15, position={'x': 0, 'y': 23, 'z': 0}, color='green')

        # for i in list(range(1, 2)):
        #         ef.create(
        #                 'box', 
        #                 width=1,
        #                 height=1, 
        #                 depth=1, 
        #                 position={'x': -25 + i, 'y': 10, 'z': 0}, 
        #                 rotation={'x': i/10, 'y': 0, 'z': 0}, 
        #                 color=0xff0000
        #                 )


        # for x in list(range(11, 25)):
        #         for y in list(range(11, 25)):
        #                 ef.create(
        #                         'box', 1, 1, 2, 
        #                         position={
        #                         'x': random.random() + x * 4, 
        #                         'y': random.random() * 4 + 2, 
        #                         'z': random.random() + y * 5
        #                         }, 
        #                         color=0x80807f)

        # # Coordinates test
        # line_test = ef.create(
        #         'line', 
        #         position1 = {'x': 30, 'y': 10, 'z': 10},
        #         position2 = {'x': 0, 'y': 0, 'z': 0},
        #         color='red')


        # TODO rewrite for loop creation
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
                                query = f"INSERT INTO world.{element} (data, user_id) VALUES ('{pice_json}', '34c1d67a-7f54-4a47-a503-84979ba8ac7f')"
                                print(query)
                                data = await db.execute_query(query)
                                print(data)
      
        # Disconnect from the database
        await db.disconnect()


if __name__ == "__main__":
        asyncio.run(main())