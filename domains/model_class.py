# -*- coding: utf-8 -*-
"""pythr.py: Visual modeling helper."""

__author__ = "Bac9l Xyer"
__copyright__ = "GPLv3"

import abc


class ModelManager():

    model_list = []
    def model_list_append(self, model_class, model_type) -> None:
        if model_type == 'model':
            self.model_list.append(model_class)
        else:
            print("Error! Wrong model type!")

    def clear_model_list(self) -> None:
        for i in self.model_list: del i
        self.model_list.clear()

    def get_model_list(self, model_type):
        if model_type == 'model_obj':
            return self.model_list
        else:
            return self.model_list


class Model(abc.ABC, ModelManager):
    manager = ModelManager()

    @abc.abstractmethod
    def return_dict(self):
        pass

    def get_name(self, model_type):
        model_number = self.manager.get_model_list(model_type).index(self)
        if model_type == 'model':
            return ''.join(('Model', str(model_number)))
        else:
            return 'NaN'

class ModelOBJ(Model):
    def __init__(
            self,
            name: str = 'Model',
            static_path: str = './static/3d_models/',
            path: str = None,
            position: dict = {'x': 0, 'y': 0, 'z': 0},
            rotation: dict = {'x': 0, 'y': 0, 'z': 0},
            cast_shadow = True,
            receive_shadow = True
            ) -> None:
        self.name = name
        self.path = static_path + path
        self.position = position
        self.rotation = rotation
        self.cast_shadow = cast_shadow
        self.receive_shadow = receive_shadow

    def return_dict(self) -> dict:
        model_dict = {
                'path': self.path,
                'position': self.position,
                'rotation': self.rotation,
                'castShadow': self.cast_shadow,
                'receiveShadow': self.receive_shadow
                }
        return model_dict

class ModelFabric:
    @staticmethod
    def create(model_type, *args, **kwargs):
        model_dict = {'model_obj': ModelOBJ}
        if model_type in model_dict:
            model = model_dict[model_type](*args, **kwargs)
            model.model_list_append(model, 'model') 
            model.name = model.get_name('model')
            return model

        else:
            print('Error! Model type not found!', model_type)