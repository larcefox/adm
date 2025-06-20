# -*- coding: utf-8 -*-
"""pythr.py: Visual arching helper."""

__author__ = "Bac9l Xyer"
__copyright__ = "GPLv3"

import abc
import numpy as np


class ArchManager():

    arch_list = []
    def arch_list_append(self, arch_class, arch_type) -> None:
        if arch_type == 'arch':
            self.arch_list.append(arch_class)
        else:
            print("Error! Wrong arch type!")

    def clear_arch_list(self) -> None:
        for i in self.arch_list: del i
        self.arch_list.clear()

    def get_arch_list(self, arch_type):
        if arch_type == 'arch':
            return self.arch_list
        else:
            return None


class Arch(abc.ABC, ArchManager):
    manager = ArchManager()

    @abc.abstractmethod
    def return_dict(self):
        pass

    def get_name(self, arch_type):
        arch_number = hash(self)
        if arch_type == 'arch':
            return ''.join(('arch', str(arch_number)))
        else:
            return 'NaN'

class Cube(Arch):
    def __init__(
            self,
            name: str = 'Cube',
            color:int = 0x00ff00,
            texture = None,
            vertices_len = 3,
            rotation: dict = {'x': 0, 'y': 0, 'z': 0},
            material_type: str = 'MeshBasicMaterial',
            cast_shadow = True,
            receive_shadow = True,
            wireframe = False, 
            transparent = False, 
            triangls = [],
            opacity = 0.5,
            side_length = 1,
            ) -> None:
        self.side_length = side_length
        self.half_side = self.side_length / 2
        self.geometry_type = 'BufferGeometry'
        self.name = name
        self.vertices_len = vertices_len
        self.rotation = rotation
        self.material = {'texture': texture} if texture else {'color': color, 'wireframe': wireframe, 'transparent': transparent, 'opacity': opacity}
        self.material_type = material_type
        self.cast_shadow = cast_shadow
        self.receive_shadow = receive_shadow
        self.triangls = triangls

    def return_dict(self) -> dict:
        vertices = np.array([
            [-self.half_side, -self.half_side, -self.half_side],  # 0
            [ self.half_side, -self.half_side, -self.half_side],  # 1
            [ self.half_side,  self.half_side, -self.half_side],  # 2
            [-self.half_side,  self.half_side, -self.half_side],  # 3
            [-self.half_side, -self.half_side,  self.half_side],  # 4
            [ self.half_side, -self.half_side,  self.half_side],  # 5
            [ self.half_side,  self.half_side,  self.half_side],  # 6
            [-self.half_side,  self.half_side,  self.half_side]   # 7
        ])
        
        # Define the faces of the cube (each face is defined by four vertices)
        faces = np.array([
            # Bottom face (counterclockwise when viewed from below)
            [0, 2, 1],
            [0, 3, 2],
            # Top face (counterclockwise when viewed from above)
            [4, 5, 6],
            [4, 6, 7],
            # Front face (counterclockwise when viewed from the front)
            [0, 1, 5],
            [0, 5, 4],
            # Back face (counterclockwise when viewed from the back)
            [2, 3, 7],
            [2, 7, 6],
            # Left face (counterclockwise when viewed from the left)
            [0, 4, 7],
            [0, 7, 3],
            # Right face (counterclockwise when viewed from the right)
            [1, 2, 6],
            [1, 6, 5]
        ])
        
        arch_dict = {
                'vertices': vertices.flatten().tolist(),
                'faces' : faces.flatten().tolist(),
                'rotation': self.rotation,
                'castShadow': self.cast_shadow,
                'receiveShadow': self.receive_shadow,
                'material_type': self.material_type,
                'geometry_type': self.geometry_type,
                'material': self.material,
                'triangls': self.triangls
                }
        return arch_dict
    
class MedievalWall(Arch):
    def __init__(
            self,
            name: str = 'm_wall',
            color:int = 0xA000FF,
            texture = None,
            vertices_len = 3,
            position: dict = {'x': 0, 'y': 0, 'z': 0},
            rotation: dict = {'x': 0, 'y': 0, 'z': 0},
            material_type: str = 'MeshBasicMaterial',
            cast_shadow = True,
            receive_shadow = True,
            wireframe = False, 
            transparent = False, 
            triangls = [],
            opacity = 0.5,
            length = 200,
            height = 100,
            thickness = 20,
            crenellation_height = 20,
            crenellation_width = 40,
            crenellation_thickness = 20,
            crenellation_spacing = 20,
            ) -> None:
        self.height = height
        self.thickness = thickness
        self.crenellation_height = crenellation_height
        self.crenellation_width = crenellation_width
        self.crenellation_thickness = crenellation_thickness
        self.crenellation_spacing = crenellation_spacing
        self.length = length
        self.geometry_type = 'BufferGeometry'
        self.name = name
        self.vertices_len = vertices_len
        self.rotation = rotation
        self.position = position
        self.material = {'texture': texture} if texture else {'color': color, 'wireframe': wireframe, 'transparent': transparent, 'opacity': opacity}
        self.material_type = material_type
        self.cast_shadow = cast_shadow
        self.receive_shadow = receive_shadow
        self.triangls = triangls

    def return_dict(self) -> dict:
        base_wall_vertices = np.array([
            [0, 0, 0],                          # 0 - bottom front left
            [self.length, 0, 0],                     # 1 - bottom front right
            [self.length, self.height - self.crenellation_height, 0],  # 2 - top front right before crenellations
            [0, self.height - self.crenellation_height, 0],       # 3 - top front left before crenellations
            [0, 0, self.thickness],                  # 4 - bottom back left
            [self.length, 0, self.thickness],             # 5 - bottom back right
            [self.length, self.height - self.crenellation_height, self.thickness],  # 6 - top back right before crenellations
            [0, self.height - self.crenellation_height, self.thickness]        # 7 - top back left before crenellations
        ])
        
        # Define the crenellation vertices (assuming they start from the top left and move right)
        crenellation_vertices = []
        current_x = 0

        while current_x < self.length:
            crenellation_vertices.extend([
                [current_x, self.height - self.crenellation_height, 0],          # Bottom front of crenellation
                [current_x + self.crenellation_width, self.height - self.crenellation_height, 0],  # Bottom front right of crenellation
                [current_x + self.crenellation_width, self.height, 0],           # Top front right of crenellation
                [current_x, self.height, 0],                                # Top front left of crenellation
                [current_x, self.height - self.crenellation_height, self.thickness],  # Bottom back left of crenellation
                [current_x + self.crenellation_width, self.height - self.crenellation_height, self.thickness],  # Bottom back right of crenellation
                [current_x + self.crenellation_width, self.height, self.thickness],   # Top back right of crenellation
                [current_x, self.height, self.thickness]                         # Top back left of crenellation
            ])
            current_x += self.crenellation_width + self.crenellation_spacing

        crenellation_vertices = np.array(crenellation_vertices)

        # Combine base wall vertices and crenellation vertices
        vertices = np.vstack((base_wall_vertices, crenellation_vertices))
        
        # Define faces of the base wall (without crenellations)
        faces = [
            # Front face (counterclockwise when viewed from front)
            [0, 2, 1],
            [0, 3, 2],
            # Back face (counterclockwise when viewed from back)
            [4, 5, 6],
            [4, 6, 7],
            # Bottom face (counterclockwise when viewed from below)
            [0, 1, 5],
            [0, 5, 4],
            # Top face (below crenellations, counterclockwise when viewed from above)
            [2, 3, 7],
            [2, 7, 6],
            # Left face (counterclockwise when viewed from the left)
            [0, 4, 7],
            [0, 7, 3],
            # Right face (counterclockwise when viewed from the right)
            [1, 2, 6],
            [1, 6, 5]
        ]

        # Define faces for each crenellation
        num_crenellations = len(crenellation_vertices) // 8
        for i in range(num_crenellations):
            base_index = 8 + i * 8
            faces.extend([
                # Front face (counterclockwise when viewed from front)
                [base_index + 0, base_index + 2, base_index + 1],
                [base_index + 0, base_index + 3, base_index + 2],
                # Back face (counterclockwise when viewed from back)
                [base_index + 4, base_index + 5, base_index + 6],
                [base_index + 4, base_index + 6, base_index + 7],
                # Bottom face (counterclockwise when viewed from below)
                [base_index + 0, base_index + 1, base_index + 5],
                [base_index + 0, base_index + 5, base_index + 4],
                # Top face (counterclockwise when viewed from above)
                [base_index + 2, base_index + 3, base_index + 7],
                [base_index + 2, base_index + 7, base_index + 6],
                # Left face (counterclockwise when viewed from the left)
                [base_index + 0, base_index + 4, base_index + 7],
                [base_index + 0, base_index + 7, base_index + 3],
                # Right face (counterclockwise when viewed from the right)
                [base_index + 1, base_index + 2, base_index + 6],
                [base_index + 1, base_index + 6, base_index + 5]
            ])

        faces = np.array(faces)
        
        arch_dict = {
                'vertices': vertices.flatten().tolist(),
                'faces' : faces.flatten().tolist(),
                'rotation': self.rotation,
                'castShadow': self.cast_shadow,
                'receiveShadow': self.receive_shadow,
                'material_type': self.material_type,
                'geometry_type': self.geometry_type,
                'material': self.material,
                'triangls': self.triangls
                }
        return arch_dict
    
class KremlinWall(Arch):
    def __init__(
            self,
            name: str = 'k_wall',
            color:int = 0xA000FF,
            texture = None,
            vertices_len = 3,
            position: dict = {'x': 0, 'y': 0, 'z': 0},
            rotation: dict = {'x': 0, 'y': 0, 'z': 0},
            material_type: str = 'MeshBasicMaterial',
            cast_shadow = True,
            receive_shadow = True,
            wireframe = False, 
            transparent = False, 
            triangls = [],
            opacity = 0.5,
            length = 200,
            height = 100,
            thickness = 20,
            crenellation_height = 20,
            crenellation_width = 40,
            crenellation_thickness = 20,
            crenellation_spacing = 20,
            ) -> None:
        self.height = height
        self.thickness = thickness
        self.crenellation_height = crenellation_height
        self.crenellation_width = crenellation_width
        self.crenellation_thickness = crenellation_thickness
        self.crenellation_spacing = crenellation_spacing
        self.length = length
        self.geometry_type = 'BufferGeometry'
        self.name = name
        self.vertices_len = vertices_len
        self.position = position
        self.rotation = rotation
        self.material = {'texture': texture} if texture else {'color': color, 'wireframe': wireframe, 'transparent': transparent, 'opacity': opacity}
        self.material_type = material_type
        self.cast_shadow = cast_shadow
        self.receive_shadow = receive_shadow
        self.triangls = triangls

    def return_dict(self) -> dict:
        # Define the base wall vertices (without crenellations)
        base_wall_vertices = np.array([
            [0, 0, 0],                          # 0 - bottom front left
            [self.length, 0, 0],                     # 1 - bottom front right
            [self.length, self.height - self.crenellation_height, 0],  # 2 - top front right before crenellations
            [0, self.height - self.crenellation_height, 0],       # 3 - top front left before crenellations
            [0, 0, self.thickness],                  # 4 - bottom back left
            [self.length, 0, self.thickness],             # 5 - bottom back right
            [self.length, self.height - self.crenellation_height, self.thickness],  # 6 - top back right before crenellations
            [0, self.height - self.crenellation_height, self.thickness]        # 7 - top back left before crenellations
        ])

        # Define the crenellation vertices (assuming they start from the top left and move right)
        crenellation_vertices = []
        current_x = 0

        while current_x < self.length:
            crenellation_vertices.extend([
                [current_x, self.height - self.crenellation_height, 0],          # Bottom front of crenellation
                [min(current_x + self.crenellation_width, self.length), self.height - self.crenellation_height, 0],  # Bottom front right of crenellation
                [min(current_x + self.crenellation_width, self.length), self.height, 0],           # Top front right of crenellation
                [current_x, self.height, 0],                                # Top front left of crenellation
                [current_x, self.height - self.crenellation_height, self.thickness],  # Bottom back left of crenellation
                [min(current_x + self.crenellation_width, self.length), self.height - self.crenellation_height, self.thickness],  # Bottom back right of crenellation
                [min(current_x + self.crenellation_width, self.length), self.height, self.thickness],   # Top back right of crenellation
                [current_x, self.height, self.thickness]                         # Top back left of crenellation
            ])
            current_x += self.crenellation_width + self.crenellation_spacing

        crenellation_vertices = np.array(crenellation_vertices)

        # Combine base wall vertices and crenellation vertices
        vertices = np.vstack((base_wall_vertices, crenellation_vertices))

        # Define faces of the base wall (without crenellations)
        faces = [
            # Front face (counterclockwise when viewed from front)
            [0, 2, 1],
            [0, 3, 2],
            # Back face (counterclockwise when viewed from back)
            [4, 5, 6],
            [4, 6, 7],
            # Bottom face (counterclockwise when viewed from below)
            [0, 1, 5],
            [0, 5, 4],
            # Top face (below crenellations, counterclockwise when viewed from above)
            [2, 3, 7],
            [2, 7, 6],
            # Left face (counterclockwise when viewed from the left)
            [0, 4, 7],
            [0, 7, 3],
            # Right face (counterclockwise when viewed from the right)
            [1, 2, 6],
            [1, 6, 5]
        ]

        # Define faces for each crenellation
        num_crenellations = len(crenellation_vertices) // 8
        for i in range(num_crenellations):
            base_index = 8 + i * 8
            faces.extend([
                # Front face (counterclockwise when viewed from front)
                [base_index + 0, base_index + 2, base_index + 1],
                [base_index + 0, base_index + 3, base_index + 2],
                # Back face (counterclockwise when viewed from back)
                [base_index + 4, base_index + 5, base_index + 6],
                [base_index + 4, base_index + 6, base_index + 7],
                # Bottom face (counterclockwise when viewed from below)
                [base_index + 0, base_index + 1, base_index + 5],
                [base_index + 0, base_index + 5, base_index + 4],
                # Top face (counterclockwise when viewed from above)
                [base_index + 2, base_index + 3, base_index + 7],
                [base_index + 2, base_index + 7, base_index + 6],
                # Left face (counterclockwise when viewed from the left)
                [base_index + 0, base_index + 4, base_index + 7],
                [base_index + 0, base_index + 7, base_index + 3],
                # Right face (counterclockwise when viewed from the right)
                [base_index + 1, base_index + 2, base_index + 6],
                [base_index + 1, base_index + 6, base_index + 5]
            ])

        faces = np.array(faces)
        
        arch_dict = {
                'vertices': vertices.flatten().tolist(),
                'faces' : faces.flatten().tolist(),
                'rotation': self.rotation,
                'castShadow': self.cast_shadow,
                'receiveShadow': self.receive_shadow,
                'material_type': self.material_type,
                'geometry_type': self.geometry_type,
                'material': self.material,
                'triangls': self.triangls
                }
        return arch_dict

class ArchFabric:
    @staticmethod
    def create(arch_type, *args, **kwargs):
        arch_dict = {'cube': Cube, 'm_wall': MedievalWall, 'k_wall': KremlinWall}
        if arch_type in arch_dict:
            arch = arch_dict[arch_type](*args, **kwargs)
            arch.arch_list_append(arch, "arch") 
            arch.name = arch.get_name('arch')
            return arch

        else:
            print('Error! Arch type not found!', arch_type)