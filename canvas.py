#!/usr/bin/python
import json
import math
from domains.entity_class import Entity_fabric as ef
from domains.entity_class import Entity
from domains.model_class import ModelFabric as mf
from domains.model_class import Model
from lib.pnoise_map import MapGen


noise_map = MapGen()
terrain = noise_map.map_gen()

def send_data():

    directional_light = ef.create('light')
    ambient_light = ef.create('light', light_type='AmbientLight')

    # example entity

#     plane = ef.create(
#             'plane',
#             630, 
#             630,
#             texture='textures/map.svg',
#             color=0xffffff,
#             position={'x':0, 'y': 0, 'z': 0},
#             rotation={'x': -(math.pi/2),'y': 0, 'z': -(math.pi/2)}
#             )

    # box = ef.create('box', 10, 10, 10, position={'x': 0, 'y': 10, 'z': 0}, color='red')
    map = ef.create('figure', vertices=terrain)

# sphere = Entity_fabric.create('sphere', 5, 15, 15, position={'x': 0, 'y': 23, 'z': 0}, color='green')

#     for i in list(range(1, 2)):
#         ef.create(
#                 'box', 
#                 width=1,
#                 height=1, 
#                 depth=1, 
#                 position={'x': -25 + i, 'y': 10, 'z': 0}, 
#                 rotation={'x': i/10, 'y': 0, 'z': 0}, 
#                 color=0xff0000
#                 )


#     for x in list(range(-9, 10)):
#         for y in list(range(-9, 10)):
#                 ef.create(
#                         'box', 1, 1, 2, 
#                         position={
#                         'x': random.random() + x * 4, 
#                         'y': random.random() * 4 + 2, 
#                         'z': random.random() + y * 5
#                         }, 
#                         color=0x80807f)

    # Coordinates test
    # line_test = ef.create(
            # 'line', 
            # position1 = {'x': 10, 'y': 10, 'z': 10},
            # position2 = {'x': 0, 'y': 0, 'z': 0},
            # color='red')


    # TODO rewrite for loop creation
    camera = ef.create('camera')
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

    return {
            'camera': camera.return_dict(), 
            'lights': json.dumps(lights),
            'shape': json.dumps(shapes),
            'line': json.dumps(lines),
            'figure': json.dumps(figures),
            'model': json.dumps(models)
            }
