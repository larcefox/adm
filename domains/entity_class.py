# -*- coding: utf-8 -*-
"""pythr.py: Visual modeling helper."""

__author__ = "Bac9l Xyer"
__copyright__ = "GPLv3"

import abc
import uuid


class Entity_manager:
    entities = {"shape": [], "camera": [], "light": [], "line": [], "figure": []}

    def entity_list_append(self, entity_class, entity_type) -> None:
        if entity_type in self.entities:
            self.entities[entity_type].append(entity_class)
        else:
            print("Error! Wrong entity type!")

    def clear_entity_list(self) -> None:
        for lst in self.entities.values():
            lst.clear()

    def get_entity_list(self, entity_type):
        return self.entities.get(entity_type, self.entities["shape"])


class Entity(abc.ABC, Entity_manager):
    manager = Entity_manager()

    def __init__(self, scale: dict | None = None, visible: bool = True) -> None:
        self.uuid = str(uuid.uuid4())
        self.scale = scale or {"x": 1, "y": 1, "z": 1}
        self.visible = visible

    @abc.abstractmethod
    def return_dict(self):
        pass

    def get_name(self, entity_type):
        entity_number = hash(self)
        return (
            f"{entity_type}{entity_number}"
            if entity_type in Entity_manager.entities
            else "NaN"
        )


class Line(Entity):
    def __init__(
        self,
        name: str = "Line",
        color: int = 0xFF0000,
        position1: dict | None = None,
        position2: dict | None = None,
        material_type: str = "LineBasicMaterial",
        cast_shadow=True,
        receive_shadow=True,
        scale: dict | None = None,
        visible: bool = True,
    ) -> None:
        super().__init__(scale=scale, visible=visible)
        self.geometry_type = "BufferGeometry"
        self.name = name
        self.position1 = position1 or {"x": 0, "y": 0, "z": 0}
        self.position2 = position2 or {"x": 0, "y": 0, "z": 0}
        self.material = {"color": color}
        self.material_type = material_type
        self.cast_shadow = cast_shadow
        self.receive_shadow = receive_shadow

    def return_dict(self) -> dict:
        return {
            "material_type": self.material_type,
            "geometry_type": self.geometry_type,
            "material": self.material,
            "position1": self.position1,
            "position2": self.position2,
            "scale": self.scale,
            "visible": self.visible,
            "uuid": self.uuid,
            "castShadow": self.cast_shadow,
            "receiveShadow": self.receive_shadow,
        }


class Figure(Entity):
    def __init__(
        self,
        name: str = "Figure",
        color: int = 0xFFFFFF,
        texture=None,
        vertices: list | None = None,
        vertices_len=3,
        rotation: dict | None = None,
        material_type: str = "MeshBasicMaterial",
        cast_shadow=True,
        receive_shadow=True,
        wireframe=False,
        transparent=False,
        triangls: list | None = None,
        opacity=0.5,
        scale: dict | None = None,
        visible: bool = True,
    ) -> None:
        super().__init__(scale=scale, visible=visible)
        self.geometry_type = "BufferGeometry"
        self.name = name
        self.vertices = vertices or []
        self.vertices_len = vertices_len
        self.rotation = rotation or {"x": 0, "y": 0, "z": 0}
        self.material = (
            {"texture": texture}
            if texture
            else {
                "color": color,
                "wireframe": wireframe,
                "transparent": transparent,
                "opacity": opacity,
            }
        )
        self.material_type = material_type
        self.cast_shadow = cast_shadow
        self.receive_shadow = receive_shadow
        self.triangls = triangls or []

    def return_dict(self) -> dict:
        return {
            "material_type": self.material_type,
            "geometry_type": self.geometry_type,
            "material": self.material,
            "vertices": self.vertices,
            "vertices_len": self.vertices_len,
            "rotation": self.rotation,
            "scale": self.scale,
            "visible": self.visible,
            "uuid": self.uuid,
            "castShadow": self.cast_shadow,
            "receiveShadow": self.receive_shadow,
            "triangls": self.triangls,
        }


class Box(Entity):
    def __init__(
        self,
        width: float,
        height: float,
        depth: float,
        name: str = "Box",
        color: int = 0xFFFFFF,
        texture=None,
        position: dict | None = None,
        rotation: dict | None = None,
        material_type: str = "MeshBasicMaterial",
        cast_shadow=True,
        receive_shadow=True,
        scale: dict | None = None,
        visible: bool = True,
    ) -> None:
        super().__init__(scale=scale, visible=visible)
        self.geometry_type = "BoxGeometry"
        self.geometry = {"width": width, "height": height, "depth": depth}
        self.name = name
        self.position = position or {"x": 0, "y": 0, "z": 0}
        self.rotation = rotation or {"x": 0, "y": 0, "z": 0}
        self.material = {"texture": texture} if texture else {"color": color}
        self.material_type = material_type
        self.cast_shadow = cast_shadow
        self.receive_shadow = receive_shadow

    def return_dict(self) -> dict:
        return {
            "material_type": self.material_type,
            "geometry_type": self.geometry_type,
            "geometry": self.geometry,
            "material": self.material,
            "position": self.position,
            "rotation": self.rotation,
            "scale": self.scale,
            "visible": self.visible,
            "uuid": self.uuid,
            "castShadow": self.cast_shadow,
            "receiveShadow": self.receive_shadow,
        }


class Sphere(Box):
    def __init__(
        self, radius: float, widthSegments: int, heightSegments: int, **kwargs
    ):
        super().__init__(0, 0, 0, **kwargs)
        self.geometry_type = "SphereGeometry"
        self.geometry = {
            "radius": radius,
            "widthSegments": widthSegments,
            "heightSegments": heightSegments,
        }


class Plane(Box):
    def __init__(self, width: float, height: float, **kwargs):
        super().__init__(width, height, 0, **kwargs)
        self.geometry_type = "PlaneGeometry"
        self.geometry = {"width": width, "height": height}


class Cylinder(Box):
    def __init__(
        self,
        radiusTop: float,
        radiusBottom: float,
        height: float,
        radialSegments: int = 8,
        heightSegments: int = 1,
        openEnded: bool = False,
        **kwargs,
    ):
        super().__init__(0, 0, 0, **kwargs)
        self.geometry_type = "CylinderGeometry"
        self.geometry = {
            "radiusTop": radiusTop,
            "radiusBottom": radiusBottom,
            "height": height,
            "radialSegments": radialSegments,
            "heightSegments": heightSegments,
            "openEnded": openEnded,
        }


class Cone(Box):
    def __init__(
        self,
        radius: float,
        height: float,
        radialSegments: int = 8,
        heightSegments: int = 1,
        openEnded: bool = False,
        **kwargs,
    ):
        super().__init__(0, 0, 0, **kwargs)
        self.geometry_type = "ConeGeometry"
        self.geometry = {
            "radius": radius,
            "height": height,
            "radialSegments": radialSegments,
            "heightSegments": heightSegments,
            "openEnded": openEnded,
        }


class Torus(Box):
    def __init__(
        self,
        radius: float,
        tube: float,
        radialSegments: int = 16,
        tubularSegments: int = 100,
        arc: float = 6.283185307179586,
        **kwargs,
    ):
        super().__init__(0, 0, 0, **kwargs)
        self.geometry_type = "TorusGeometry"
        self.geometry = {
            "radius": radius,
            "tube": tube,
            "radialSegments": radialSegments,
            "tubularSegments": tubularSegments,
            "arc": arc,
        }


class Circle(Box):
    def __init__(
        self,
        radius: float,
        segments: int = 32,
        thetaStart: float = 0.0,
        thetaLength: float = 6.283185307179586,
        **kwargs,
    ):
        super().__init__(0, 0, 0, **kwargs)
        self.geometry_type = "CircleGeometry"
        self.geometry = {
            "radius": radius,
            "segments": segments,
            "thetaStart": thetaStart,
            "thetaLength": thetaLength,
        }


class Ring(Box):
    def __init__(
        self,
        innerRadius: float,
        outerRadius: float,
        thetaSegments: int = 32,
        phiSegments: int = 1,
        thetaStart: float = 0.0,
        thetaLength: float = 6.283185307179586,
        **kwargs,
    ):
        super().__init__(0, 0, 0, **kwargs)
        self.geometry_type = "RingGeometry"
        self.geometry = {
            "innerRadius": innerRadius,
            "outerRadius": outerRadius,
            "thetaSegments": thetaSegments,
            "phiSegments": phiSegments,
            "thetaStart": thetaStart,
            "thetaLength": thetaLength,
        }


class Text3D(Entity):
    def __init__(
        self,
        text: str,
        size: float = 10,
        height: float = 2,
        curveSegments: int = 12,
        bevelEnabled: bool = False,
        bevelThickness: float = 1,
        bevelSize: float = 0.5,
        bevelOffset: float = 0,
        bevelSegments: int = 3,
        font: str = "helvetiker",
        name: str = "Text3D",
        color: int = 0xFFFFFF,
        position: dict = {"x": 0, "y": 0, "z": 0},
        rotation: dict = {"x": 0, "y": 0, "z": 0},
        material_type: str = "MeshBasicMaterial",
        cast_shadow: bool = True,
        receive_shadow: bool = True,
    ):
        self.geometry_type = "TextGeometry"
        self.geometry = {
            "text": text,
            "size": size,
            "height": height,
            "curveSegments": curveSegments,
            "bevelEnabled": bevelEnabled,
            "bevelThickness": bevelThickness,
            "bevelSize": bevelSize,
            "bevelOffset": bevelOffset,
            "bevelSegments": bevelSegments,
            "font": font,
        }
        self.name = name
        self.position = position
        self.rotation = rotation
        self.material = {"color": color}
        self.material_type = material_type
        self.cast_shadow = cast_shadow
        self.receive_shadow = receive_shadow

    def return_dict(self) -> dict:
        return {
            "geometry_type": self.geometry_type,
            "geometry": self.geometry,
            "material": self.material,
            "material_type": self.material_type,
            "position": self.position,
            "rotation": self.rotation,
            "castShadow": self.cast_shadow,
            "receiveShadow": self.receive_shadow,
        }


class Camera(Entity):
    def __init__(
        self,
        name: str = "Camera",
        camera_type: str = "PerspectiveCamera",
        fild_of_view: int = 75,
        aspect_ratio: str = "innerWidth / innerHeight",
        clipping_plane_near: float = 0.1,
        clipping_plane_far: float = 10000,
        position: dict | None = None,
        scale: dict | None = None,
        visible: bool = True,
    ) -> None:
        super().__init__(scale=scale, visible=visible)
        self.name = name
        self.camera_type = camera_type
        self.fild_of_view = fild_of_view
        self.aspect_ratio = aspect_ratio
        self.clipping_plane_near = clipping_plane_near
        self.clipping_plane_far = clipping_plane_far
        self.position = position or {"x": -240, "y": 440, "z": 140}

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
        name: str = "OrthographicCamera",
        position: dict | None = None,
        scale: dict | None = None,
        visible: bool = True,
    ) -> None:
        super().__init__(scale=scale, visible=visible)
        self.name = name
        self.camera_type = "OrthographicCamera"
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom
        self.near = near
        self.far = far
        self.position = position or {"x": 0, "y": 0, "z": 100}

    def return_dict(self) -> dict:
        return self.__dict__


class Light(Entity):
    def __init__(
        self,
        name: str = "Light",
        light_type: str = "DirectionalLight",
        color: int = 0xFFFFFF,
        intensity: float = 1.0,
        shadow: dict = None,
        target_position: dict | None = None,
        position: dict | None = None,
        cast_shadow=True,
        scale: dict | None = None,
        visible: bool = True,
    ) -> None:
        super().__init__(scale=scale, visible=visible)
        self.name = name
        self.color = color
        self.intensity = intensity
        self.light_type = light_type
        self.shadow = shadow or {
            "bias": -0.001,
            "mapSize": {"width": 2048, "height": 2048},
            "camera": {
                "near": 0.5,
                "far": 500,
                "left": 100,
                "right": -100,
                "top": 100,
                "bottom": -100,
            },
        }
        self.target_position = target_position or {"x": 20, "y": 100, "z": 10}
        self.position = position or {"x": 20, "y": 100, "z": 10}
        self.cast_shadow = cast_shadow

    def return_dict(self) -> dict:
        return self.__dict__


class AmbientLight(Entity):
    def __init__(
        self,
        color: int = 0xFFFFFF,
        intensity: float = 1.0,
        name: str = "AmbientLight",
        position: dict | None = None,
        scale: dict | None = None,
        visible: bool = True,
    ) -> None:
        super().__init__(scale=scale, visible=visible)
        self.name = name
        self.light_type = "AmbientLight"
        self.color = color
        self.intensity = intensity
        self.position = position or {"x": 0, "y": 0, "z": 0}

    def return_dict(self) -> dict:
        return self.__dict__


class HemisphereLight(Entity):
    def __init__(
        self,
        sky_color: int = 0xFFFFFF,
        ground_color: int = 0x444444,
        intensity: float = 1.0,
        name: str = "HemisphereLight",
        position: dict | None = None,
        scale: dict | None = None,
        visible: bool = True,
    ) -> None:
        super().__init__(scale=scale, visible=visible)
        self.name = name
        self.light_type = "HemisphereLight"
        self.sky_color = sky_color
        self.ground_color = ground_color
        self.intensity = intensity
        self.position = position or {"x": 0, "y": 0, "z": 0}

    def return_dict(self) -> dict:
        return self.__dict__


class PointLight(Entity):
    def __init__(
        self,
        name: str = "PointLight",
        color: int = 0xFFFFFF,
        intensity: float = 1.0,
        distance: float = 0.0,
        decay: float = 2.0,
        shadow: dict | None = None,
        position: dict | None = None,
        cast_shadow=True,
        scale: dict | None = None,
        visible: bool = True,
    ) -> None:
        super().__init__(scale=scale, visible=visible)
        self.name = name
        self.light_type = "PointLight"
        self.color = color
        self.intensity = intensity
        self.distance = distance
        self.decay = decay
        self.shadow = shadow or {
            "bias": -0.001,
            "mapSize": {"width": 1024, "height": 1024},
            "camera": {"near": 0.5, "far": 500},
        }
        self.position = position or {"x": 0, "y": 0, "z": 0}
        self.cast_shadow = cast_shadow

    def return_dict(self) -> dict:
        return self.__dict__


class SpotLight(Entity):
    def __init__(
        self,
        name: str = "SpotLight",
        color: int = 0xFFFFFF,
        intensity: float = 1.0,
        distance: float = 0.0,
        angle: float = 1.047198,
        penumbra: float = 0.0,
        decay: float = 2.0,
        shadow: dict | None = None,
        target_position: dict | None = None,
        position: dict | None = None,
        cast_shadow=True,
        scale: dict | None = None,
        visible: bool = True,
    ) -> None:
        super().__init__(scale=scale, visible=visible)
        self.name = name
        self.light_type = "SpotLight"
        self.color = color
        self.intensity = intensity
        self.distance = distance
        self.angle = angle
        self.penumbra = penumbra
        self.decay = decay
        self.shadow = shadow or {
            "bias": -0.001,
            "mapSize": {"width": 1024, "height": 1024},
            "camera": {"near": 0.5, "far": 500, "fov": 30},
        }
        self.target_position = target_position or {"x": 0, "y": 0, "z": 0}
        self.position = position or {"x": 0, "y": 0, "z": 0}
        self.cast_shadow = cast_shadow

    def return_dict(self) -> dict:
        return self.__dict__


class Entity_fabric:
    @staticmethod
    def create(entity_type, *args, **kwargs):
        mapping = {
            "box": (Box, "shape"),
            "sphere": (Sphere, "shape"),
            "plane": (Plane, "shape"),
            "cylinder": (Cylinder, "shape"),
            "cone": (Cone, "shape"),
            "torus": (Torus, "shape"),
            "circle": (Circle, "shape"),
            "ring": (Ring, "shape"),
            "text3d": (Text3D, "shape"),
            "camera": (Camera, "camera"),
            "ortho_camera": (OrthographicCamera, "camera"),
            "light": (Light, "light"),
            "point_light": (PointLight, "light"),
            "spot_light": (SpotLight, "light"),
            "ambient": (AmbientLight, "light"),
            "hemisphere": (HemisphereLight, "light"),
            "line": (Line, "line"),
            "figure": (Figure, "figure"),
        }

        entity_cls, ent_type = mapping.get(entity_type, (Box, "shape"))
        entity = entity_cls(*args, **kwargs)
        entity.entity_list_append(entity, ent_type)
        entity.name = entity.get_name(ent_type)
        return entity
