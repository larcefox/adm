from skyfield.api import load
from datetime import datetime
from typing import Dict, Tuple
from cachetools import cached, TTLCache


class PlanetDataFetcher:
    """
    Класс для получения координат и размеров планет с использованием Skyfield.
    """

    PLANET_DATA = {
        'mercury': ('MERCURY BARYCENTER', 2439.7),
        'venus': ('VENUS BARYCENTER', 6051.8),
        'earth': ('EARTH BARYCENTER', 6371.0),
        'mars': ('MARS BARYCENTER', 3389.5),
        'jupiter': ('JUPITER BARYCENTER', 69911),
        'saturn': ('SATURN BARYCENTER', 58232),
        'uranus': ('URANUS BARYCENTER', 25362),
        'neptune': ('NEPTUNE BARYCENTER', 24622),
        'sun': ('SUN', 69634)
    }

    def __init__(self):
        """Инициализация Skyfield и загрузка эфемерид"""
        self.ts = load.timescale()
        self.eph = load('de421.bsp')  # Загрузка эфемерид JPL DE421

    @cached(cache=TTLCache(maxsize=10, ttl=3600))
    def get_planet_data(self, planet: str, date: str = None) -> Dict[str, float]:
        """
        Получает данные планеты: координаты и размер

        :param planet: Название планеты (mercury, venus, earth, mars, etc.)
        :param date: Дата в формате 'YYYY-MM-DD' (None - текущая дата)
        :return: Словарь с данными {
            'x', 'y', 'z': координаты в AU,
            'radius_km': радиус в километрах,
            'diameter_km': диаметр в километрах
        }
        """
        try:
            planet_info = self.PLANET_DATA.get(planet.lower())
            if not planet_info:
                raise ValueError(f"Неизвестная планета: {planet}")

            planet_name, planet_radius = planet_info

            # Создаем объект времени
            if date:
                dt = datetime.strptime(date, '%Y-%m-%d')
                t = self.ts.utc(dt.year, dt.month, dt.day)
            else:
                t = self.ts.now()

            # Получаем положение планеты относительно Солнца
            sun = self.eph['sun']
            planet_obj = self.eph[planet_name]
            astrometric = sun.at(t).observe(planet_obj)

            # Возвращаем координаты и размер
            x, y, z = astrometric.position.au
            return {
                'x': float(x),
                'y': float(y),
                'z': float(z),
                'radius_km': planet_radius,
                'diameter_km': planet_radius * 2
            }

        except Exception as e:
            raise ValueError(f"Ошибка получения данных {planet}: {str(e)}")

    def get_all_planets_data(self, date: str = None) -> Dict[str, Dict[str, float]]:
        """
        Получает данные всех планет на указанную дату
        """
        results = {}
        for planet in self.PLANET_DATA:
            try:
                results[planet] = self.get_planet_data(planet, date)
            except ValueError:
                results[planet] = None
        return results


if __name__ == "__main__":
    # Пример использования
    fetcher = PlanetDataFetcher()

    # Получаем текущие данные всех планет
    print("Текущие данные планет:")
    print("{:<10} {:<10} {:<10} {:<10} {:<10} {:<10}".format(
        "Планета", "X (AU)", "Y (AU)", "Z (AU)", "Радиус (км)", "Диаметр (км)"))

    positions = fetcher.get_all_planets_data()

    for planet, data in positions.items():
        if data:
            print(data)
            print("{:<10} {:<10.3f} {:<10.3f} {:<10.3f} {:<10,.0f} {:<10,.0f}".format(
                planet,
                data['x'],
                data['y'],
                data['z'],
                data['radius_km'],
                data['diameter_km']
            ))
        else:
            print(f"{planet}: Данные недоступны")

    # Получаем данные Марса на конкретную дату
    print("\nДанные Марса 1 января 2025 года:")
    try:
        mars_data = fetcher.get_planet_data('mars', '2025-01-01')
        print(f"Координаты (AU): X={mars_data['x']:.3f}, Y={mars_data['y']:.3f}, Z={mars_data['z']:.3f}")
        print(f"Радиус: {mars_data['radius_km']:,.0f} км")
        print(f"Диаметр: {mars_data['diameter_km']:,.0f} км")
    except ValueError as e:
        print(f"Ошибка: {e}")