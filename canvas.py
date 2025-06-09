#!/usr/bin/python
import json
import math
import random
from domains.entity_class import Entity_fabric as ef
from domains.entity_class import Entity
from domains.model_class import ModelFabric as mf
from domains.model_class import Model
from domains.arch_class import ArchFabric as af
from domains.arch_class import Arch
from lib.pnoise_map import MapGen


noise_map = MapGen()
terrain = noise_map.map_gen()

def send_data():

    directional_light = ef.create('light')
    ambient_light = ef.create('light', light_type='AmbientLight')

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

    # TODO rewrite for loop creation
    camera = ef.create('camera')
    light = {
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
            'camera': camera.return_dict(), 
            'light': json.dumps(light),
            'shape': json.dumps(shapes),
            'line': json.dumps(lines),
            'figure': json.dumps(figures),
            'model': json.dumps(models),
            'arch': json.dumps(arch)
            }
