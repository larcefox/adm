#!/usr/bin/python
import json
from domains.entity_class import Entity_fabric as ef
from domains.entity_class import Entity
from lib.postgres_con import Database
import asyncio


def send_data():
    """Create sample objects for all entity types."""

    # Shapes
    ef.create('box', 10, 10, 10, color=0xff0000)
    ef.create('sphere', radius=5, widthSegments=8, heightSegments=8, position={'x': 15, 'y': 0, 'z': 0})
    ef.create('plane', 20, 20, position={'x': 0, 'y': -5, 'z': 0})
    ef.create('cylinder', radiusTop=3, radiusBottom=3, height=6, position={'x': -15, 'y': 0, 'z': 0})
    ef.create('cone', radius=3, height=6, position={'x': 30, 'y': 0, 'z': 0})
    ef.create('torus', radius=4, tube=1, position={'x': 45, 'y': 0, 'z': 0})
    ef.create('circle', radius=5, position={'x': 60, 'y': 0, 'z': 0})
    ef.create('ring', innerRadius=2, outerRadius=5, position={'x': 75, 'y': 0, 'z': 0})
    ef.create('text3d', 'Hello 3D', size=5, height=1, position={'x': 90, 'y': 0, 'z': 0})

    # Line and Figure
    ef.create('line', position1={'x': 0, 'y': 0, 'z': 0}, position2={'x': 10, 'y': 10, 'z': 0})
    ef.create('figure', vertices=[0, 0, 0, 5, 0, 0, 0, 5, 0], triangls=[0, 1, 2])

    # Cameras
    ef.create('camera')
    ef.create('ortho_camera', left=-5, right=5, top=5, bottom=-5)

    # Lights
    ef.create('light')
    ef.create('point_light')
    ef.create('spot_light')
    ef.create('ambient')
    ef.create('hemisphere')

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
    models = {}
    arch = {}

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
                                query = f"INSERT INTO world.{element} (data, user_id) VALUES ('{pice_json}', 'a6eab050-41ba-481c-badf-4e955665c543')"
                                print(query)
                                data = await db.execute_query(query)
                                print(data)
      
        # Disconnect from the database
        await db.disconnect()


if __name__ == "__main__":
        asyncio.run(main())

