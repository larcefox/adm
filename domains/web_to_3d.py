import requests
from bs4 import BeautifulSoup
from domains.entity_class import Entity_fabric as ef
from domains.entity_class import Entity
from domains.model_class import Model
from domains.arch_class import Arch
import json
import random
import re


def fetch_html(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text


TAG_MAP = {
    "h1": {"color": 0x0033CC},
    "h2": {"color": 0x3366CC},
    "h3": {"color": 0x6699FF},
    "p": {"color": 0x00AA88},
    "div": {"color": 0x888888},
    "a": {"color": 0xFF5500},
    "span": {"color": 0x55FFAA},
    "button": {"color": 0xCC4444},
    "input": {"color": 0xAAAAAA},
    "img": {"color": 0xFFFFFF},
}


def extract_size_from_style(style: str):
    """Парсинг width/height из inline-стиля"""
    width, height = 10, 2  # Значения по умолчанию
    if style:
        w_match = re.search(r"width:\s*(\d+)px", style)
        h_match = re.search(r"height:\s*(\d+)px", style)
        if w_match:
            width = max(1, int(w_match.group(1)) / 10)  # нормализация
        if h_match:
            height = max(1, int(h_match.group(1)) / 10)
    return width, height


def parse_and_create_3d_elements(html):

    soup = BeautifulSoup(html, "html.parser")
    grid_x = 0
    grid_y = 0
    spacing = 5

    elements = soup.find_all(TAG_MAP.keys())

    for i, tag in enumerate(elements):
        tag_name = tag.name
        style = tag.get("style", "")
        depth, height = extract_size_from_style(style)

        # Если не было inline-стиля — используем значение по умолчанию
        if depth == 10 and height == 2 and tag_name in TAG_MAP:
            # Можно задать "размерность" по длине текста:
            text_len = len(tag.get_text(strip=True))
            depth = min(30, max(5, text_len * 0.5))
            height = 2

        width = 30  # можно сделать глубину фиксированной

        position = {
            "x": (grid_x % 5) * (width + spacing),
            "y": -(grid_y // 5) * (height + spacing),
            "z": 0,
        }

        color = TAG_MAP.get(tag_name, {}).get(
            "color", random.randint(0x111111, 0xFFFFFF)
        )

        text_value = tag.get_text(strip=True)
        if text_value:
            ef.create(
                "text3d",
                text=text_value,
                size=3,
                height=1,
                position=position,
                color=color,
            )

        ef.create(
            "box",
            width=width,
            height=height,
            depth=depth,
            position=position,
            color=color,
        )

        grid_x += 1
        grid_y += 1

    # Debug: показать сколько сущностей создано
    shapes = Entity.manager.get_entity_list("shape")
    print(f"[DEBUG] Total 3D shapes generated: {len(shapes)}")


def export_to_dict():
    return {
        "light": {
            light.name: light.return_dict()
            for light in Entity.manager.get_entity_list("light")
        },
        "shape": {
            entity.name: entity.return_dict()
            for entity in Entity.manager.get_entity_list("shape")
        },
        "model": {
            model.name: model.return_dict()
            for model in Model.manager.get_model_list("model_obj")
        },
        "arch": {
            arch.name: arch.return_dict() for arch in Arch.manager.get_arch_list("arch")
        },
    }


def convert_webpage_to_3d(url="https://www.google.ru"):
    html = fetch_html(url)
    parse_and_create_3d_elements(html)
    return export_to_dict()


if __name__ == "__main__":
    scene_data = convert_webpage_to_3d()
    print(json.dumps(scene_data, indent=2))
