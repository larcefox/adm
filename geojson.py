import json
from domains.entity_class import Entity_fabric, Line, Figure
from lib.postgres_con import Database
import asyncio


def geojson_to_entities(geojson_path, height=10, color=0x00ff00):
    """
    Преобразует GeoJSON-файл в список 3D-сущностей (Line или Figure).

    :param geojson_path: путь к .geojson файлу
    :param height: высота объектов (для Polygon)
    :param color: цвет линий или полигонов
    :return: список Entity объектов
    """
    with open(geojson_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    features = data.get('features', [])
    entities = []

    for feature in features:
        geometry = feature.get('geometry', {})
        geom_type = geometry.get('type')
        coords = geometry.get('coordinates', [])

        # Убираем вложенность, если она есть
        if geom_type in ['Polygon', 'MultiLineString']:
            coords = coords[0]

        if geom_type in ['LineString', 'MultiLineString']:
            for i in range(len(coords) - 1):
                p1 = {'x': coords[i][0], 'y': 0, 'z': coords[i][1]}
                p2 = {'x': coords[i + 1][0], 'y': 0, 'z': coords[i + 1][1]}
                line = Line(position1=p1, position2=p2, color=color)
                entities.append(line)

        elif geom_type in ['Polygon', 'MultiPolygon']:
            vertices = []
            triangls = []
            for i, coord in enumerate(coords):
                vertices.append([coord[0], 0, coord[1]])
                if i >= 2:
                    triangls.append([0, i - 1, i])
            vertices_flat = [v for sublist in vertices for v in sublist]
            triangls_flat = [i for tri in triangls for i in tri]
            fig = Figure(vertices=vertices_flat, triangls=triangls_flat, color=color)
            entities.append(fig)

        elif geom_type == 'Point':
            x, z = coords
            box = Entity_fabric.create(
                'box',
                width=1,
                height=height,
                depth=1,
                position={'x': x, 'y': height / 2, 'z': z},
                color=color
            )
            entities.append(box)

        else:
            print(f"Тип геометрии не поддерживается: {geom_type}")

    return entities


async def insert_entities_to_db(entities, user_id='c55f8791-65f9-4a29-8f46-bc5e618fd0dd'):
    db = Database()
    await db.connect()

    for entity in entities:
        # entity_type = entity.__class__.__name__.lower()  # e.g., 'line', 'figure', 'box'
        if hasattr(entity, 'return_dict'):
            payload = json.dumps({entity.name: entity.return_dict()})
            query = f"INSERT INTO world.shape (data, user_id) VALUES ('{payload}', '{user_id}')"
            await db.execute_query(query)

    await db.disconnect()


if __name__ == '__main__':
    import sys
    geojson_file = sys.argv[1] if len(sys.argv) > 1 else 'data.geojson'

    all_entities = geojson_to_entities(geojson_file)
    asyncio.run(insert_entities_to_db(all_entities))
