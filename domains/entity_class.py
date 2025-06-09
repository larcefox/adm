# -*- coding: utf-8 -*-
"""pythr.py: Visual modeling helper."""

__author__ = "Bac9l Xyer"
__copyright__ = "GPLv3"

import abc


class Entity_manager():
    entity_list = []
    camera_list = []
    light_list = []
    line_list = []
    figure_list = []

    def entity_list_append(self, entity_class, entity_type) -> None:
        if entity_type == 'shape':
            self.entity_list.append(entity_class)
        elif entity_type == 'camera':
            self.camera_list.append(entity_class)
        elif entity_type == 'light':
            self.light_list.append(entity_class)
        elif entity_type == 'line':
            self.line_list.append(entity_class)
        elif entity_type == 'figure':
            self.figure_list.append(entity_class)
        else:
            print("Error! Wrong entity type!")

    def clear_entity_list(self) -> None:
        for lst in [self.entity_list, self.camera_list, self.light_list, self.line_list, self.figure_list]:
            for i in lst:
                del i
            lst.clear()

    def get_entity_list(self, entity_type):
        if entity_type == 'shape':
            return self.entity_list
        elif entity_type == 'camera':
            return self.camera_list
        elif entity_type == 'light':
            return self.light_list
        elif entity_type == 'line':
            return self.line_list
        elif entity_type == 'figure':
            return self.figure_list
        else:
            return self.entity_list


class Entity(abc.ABC, Entity_manager):
    manager = Entity_manager()

    @abc.abstractmethod
    def return_dict(self):
        pass

    def get_name(self, entity_type):
        entity_number = hash(self)
        return f"{entity_type}{entity_number}" if entity_type in ['shape', 'camera', 'light', 'line', 'figure'] else 'NaN'


class Line(Entity):
    def __init__(
            self,
            name: str = 'Line',
            color: int = 0xff0000,
            position1: dict = {'x': 0, 'y': 0, 'z': 0},
            position2: dict = {'x': 0, 'y': 0, 'z': 0},
            material_type: str = 'LineBasicMaterial',
            cast_shadow=True,
            receive_shadow=True
    ) -> None:
        self.geometry_type = 'BufferGeometry'
        self.name = name
        self.position1 = position1
        self.position2 = position2
        self.material = {'color': color}
        self.material_type = material_type
        self.cast_shadow = cast_shadow
        self.receive_shadow = receive_shadow

    def return_dict(self) -> dict:
        return {
            'material_type': self.material_type,
            'geometry_type': self.geometry_type,
            'material': self.material,
            'position1': self.position1,
            'position2': self.position2,
            'castShadow': self.cast_shadow,
            'receiveShadow': self.receive_shadow
        }


class Figure(Entity):
    def __init__(
            self,
            name: str = 'Figure',
            color: int = 0xffffff,
            texture=None,
            vertices: list = [],
            vertices_len=3,
            rotation: dict = {'x': 0, 'y': 0, 'z': 0},
            material_type: str = 'MeshBasicMaterial',
            cast_shadow=True,
            receive_shadow=True,
            wireframe=False,
            transparent=False,
            triangls=[],
            opacity=0.5
    ) -> None:
        self.geometry_type = 'BufferGeometry'
        self.name = name
        self.vertices = vertices
        self.vertices_len = vertices_len
        self.rotation = rotation
        self.material = {'texture': texture} if texture else {
            'color': color, 'wireframe': wireframe, 'transparent': transparent, 'opacity': opacity}
        self.material_type = material_type
        self.cast_shadow = cast_shadow
        self.receive_shadow = receive_shadow
        self.triangls = triangls

    def return_dict(self) -> dict:
        return {
            'material_type': self.material_type,
            'geometry_type': self.geometry_type,
            'material': self.material,
            'vertices': self.vertices,
            'vertices_len': self.vertices_len,
            'rotation': self.rotation,
            'castShadow': self.cast_shadow,
            'receiveShadow': self.receive_shadow,
            'triangls': self.triangls
        }


class Box(Entity):
    def __init__(
            self,
            width: float,
            height: float,
            depth: float,
            name: str = 'Box',
            color: int = 0xffffff,
            texture=None,
            position: dict = {'x': 0, 'y': 0, 'z': 0},
            rotation: dict = {'x': 0, 'y': 0, 'z': 0},
            material_type: str = 'MeshBasicMaterial',
            cast_shadow=True,
            receive_shadow=True
    ) -> None:
        self.geometry_type = 'BoxGeometry'
        self.geometry = {'width': width, 'height': height, 'depth': depth}
        self.name = name
        self.position = position
        self.rotation = rotation
        self.material = {'texture': texture} if texture else {'color': color}
        self.material_type = material_type
        self.cast_shadow = cast_shadow
        self.receive_shadow = receive_shadow

    def return_dict(self) -> dict:
        return {
            'material_type': self.material_type,
            'geometry_type': self.geometry_type,
            'geometry': self.geometry,
            'material': self.material,
            'position': self.position,
            'rotation': self.rotation,
            'castShadow': self.cast_shadow,
            'receiveShadow': self.receive_shadow
        }


class Sphere(Box):
    def __init__(
            self,
            radius: float,
            widthSegments: int,
            heightSegments: int,
            **kwargs
    ):
        super().__init__(0, 0, 0, **kwargs)
        self.geometry_type = 'SphereGeometry'
        self.geometry = {
            'radius': radius,
            'widthSegments': widthSegments,
            'heightSegments': heightSegments
        }


class Plane(Box):
    def __init__(
            self,
            width: float,
            height: float,
            **kwargs
    ):
        super().__init__(width, height, 0, **kwargs)
        self.geometry_type = 'PlaneGeometry'
        self.geometry = {'width': width, 'height': height}


class Cylinder(Box):
    def __init__(
            self,
            radiusTop: float,
            radiusBottom: float,
            height: float,
            radialSegments: int = 8,
            heightSegments: int = 1,
            openEnded: bool = False,
            **kwargs
    ):
        super().__init__(0, 0, 0, **kwargs)
        self.geometry_type = 'CylinderGeometry'
        self.geometry = {
            'radiusTop': radiusTop,
            'radiusBottom': radiusBottom,
            'height': height,
            'radialSegments': radialSegments,
            'heightSegments': heightSegments,
            'openEnded': openEnded
        }


class Cone(Box):
    def __init__(
            self,
            radius: float,
            height: float,
            radialSegments: int = 8,
            heightSegments: int = 1,
            openEnded: bool = False,
            **kwargs
    ):
        super().__init__(0, 0, 0, **kwargs)
        self.geometry_type = 'ConeGeometry'
        self.geometry = {
            'radius': radius,
            'height': height,
            'radialSegments': radialSegments,
            'heightSegments': heightSegments,
            'openEnded': openEnded
        }


class Torus(Box):
    def __init__(
            self,
            radius: float,
            tube: float,
            radialSegments: int = 16,
            tubularSegments: int = 100,
            arc: float = 6.283185307179586,
            **kwargs
    ):
        super().__init__(0, 0, 0, **kwargs)
        self.geometry_type = 'TorusGeometry'
        self.geometry = {
            'radius': radius,
            'tube': tube,
            'radialSegments': radialSegments,
            'tubularSegments': tubularSegments,
            'arc': arc
        }


class Camera(Entity):
    def __init__(
            self,
            name: str = 'Camera',
            camera_type: str = 'PerspectiveCamera',
            fild_of_view: int = 75,
            aspect_ratio: str = 'innerWidth / innerHeight',
            clipping_plane_near: float = 0.1,
            clipping_plane_far: float = 10000,
            position: dict = {'x': -240, 'y': 440, 'z': 140}
    ) -> None:
        self.name = name
        self.camera_type = camera_type
        self.fild_of_view = fild_of_view
        self.aspect_ratio = aspect_ratio
        self.clipping_plane_near = clipping_plane_near
        self.clipping_plane_far = clipping_plane_far
        self.position = position

    def return_dict(self) -> dict:
        return self.__dict__


class OrthographicCamera(Entity):
    def __init__(
            self,
            left: float,
            right: float,
            top: float,
            bottom: float,
            near: float = 0.1,
            far: float = 2000,
            name: str = 'OrthographicCamera',
            position: dict = {'x': 0, 'y': 0, 'z': 100}
    ) -> None:
        self.name = name
        self.camera_type = 'OrthographicCamera'
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom
        self.near = near
        self.far = far
        self.position = position

    def return_dict(self) -> dict:
        return self.__dict__


class Light(Entity):
    def __init__(
            self,
            name: str = 'Light',
            light_type: str = 'DirectionalLight',
            color: int = 0xffffff,
            intensity: float = 1.0,
            shadow: dict = None,
            target_position: dict = {'x': 20, 'y': 100, 'z': 10},
            position: dict = {'x': 20, 'y': 100, 'z': 10},
            cast_shadow=True
    ) -> None:
        self.name = name
        self.color = color
        self.intensity = intensity
        self.light_type = light_type
        self.shadow = shadow or {
            'bias': -0.001,
            'mapSize': {'width': 2048, 'height': 2048},
            'camera': {'near': 0.5, 'far': 500, 'left': 100, 'right': -100, 'top': 100, 'bottom': -100}
        }
        self.target_position = target_position
        self.position = position
        self.cast_shadow = cast_shadow

    def return_dict(self) -> dict:
        return self.__dict__


class AmbientLight(Entity):
    def __init__(self, color: int = 0xffffff, intensity: float = 1.0, name: str = 'AmbientLight',
                 position: dict = {'x': 0, 'y': 0, 'z': 0}) -> None:
        self.name = name
        self.light_type = 'AmbientLight'
        self.color = color
        self.intensity = intensity
        self.position = position

    def return_dict(self) -> dict:
        return self.__dict__


class HemisphereLight(Entity):
    def __init__(self, sky_color: int = 0xffffff, ground_color: int = 0x444444,
                 intensity: float = 1.0, name: str = 'HemisphereLight',
                 position: dict = {'x': 0, 'y': 0, 'z': 0}) -> None:
        self.name = name
        self.light_type = 'HemisphereLight'
        self.sky_color = sky_color
        self.ground_color = ground_color
        self.intensity = intensity
        self.position = position

    def return_dict(self) -> dict:
        return self.__dict__


class Entity_fabric:
    @staticmethod
    def create(entity_type, *args, **kwargs):
        shape_dict = {
            'box': Box, 'sphere': Sphere, 'plane': Plane,
            'cylinder': Cylinder, 'cone': Cone, 'torus': Torus
        }
        camera_dict = {
            'camera': Camera, 'ortho_camera': OrthographicCamera
        }
        light_dict = {
            'light': Light, 'ambient': AmbientLight, 'hemisphere': HemisphereLight
        }

        if entity_type in shape_dict:
            entity = shape_dict[entity_type](*args, **kwargs)
            entity.entity_list_append(entity, 'shape')
            entity.name = entity.get_name('shape')
        elif entity_type in camera_dict:
            entity = camera_dict[entity_type](*args, **kwargs)
            entity.entity_list_append(entity, 'camera')
            entity.name = entity.get_name('camera')
        elif entity_type in light_dict:
            entity = light_dict[entity_type](*args, **kwargs)
            entity.entity_list_append(entity, 'light')
            entity.name = entity.get_name('light')
        elif entity_type == 'line':
            entity = Line(*args, **kwargs)
            entity.entity_list_append(entity, 'line')
            entity.name = entity.get_name('line')
        elif entity_type == 'figure':
            entity = Figure(*args, **kwargs)
            entity.entity_list_append(entity, 'figure')
            entity.name = entity.get_name('figure')
        else:
            entity = Box(*args, **kwargs)
            entity.entity_list_append(entity, 'shape')
            entity.name = entity.get_name('shape')

        return entity
