from flask import Blueprint, render_template
from src.world.models import Entity


world_bp = Blueprint("world", __name__, template_folder="templates")