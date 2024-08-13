from flask import Blueprint, render_template
from flask_login import login_required
from src.accounts.models import User, Role
from flask_login import current_user
from lib.reload_canvas import Worker
import asyncio
from lib.websocket_cli import websocket_client


core_bp = Blueprint("core", __name__)

reloader = Worker()
objects_dict = reloader.run_reload()

@core_bp.route("/")
@login_required
def home():
    is_admin = (
        Role.query.join(User).where(User.id == current_user.get_id()).first().is_admin
    )
    # asyncio.run(websocket_client({"god_sign": [{current_user.get_id(), "God hear!"}]}))
    return render_template("core/index.html", 
                            user=current_user.get_id(),
                            is_admin=is_admin,
                            title='QurE',
                            body='body',
                            light=objects_dict['lights'], 
                            camera=objects_dict['camera'], 
                            entity=objects_dict['shape'],
                            line=objects_dict['line'],
                            figure=objects_dict['figure'],
                            model=objects_dict['model'],
                            arch=objects_dict['arch']
                            )
# depricated after websocket apire
# @core_bp.route('/entitys', methods=['GET'])
# def get_entitys():
#     return objects_dict['shape']

core_bp.route("/ws")
@login_required
def ws():
    return render_template("core/websocket.js")