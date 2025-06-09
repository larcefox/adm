from flask import Blueprint, render_template
from src.world.models import Shape, Light, Line, Figure, Model, Arch


world_bp = Blueprint("world", __name__, template_folder="templates")