from flask import Blueprint, render_template
from flask_login import login_required
from src.accounts.models import User, Role
from flask_login import current_user
from lib.reload_canvas import Worker


core_bp = Blueprint("core", __name__)

reloader = Worker()
entity_dict = reloader.run_reload()

@core_bp.route("/")
@login_required
def home():
    is_admin = (
        Role.query.join(User).where(User.id == current_user.get_id()).first().is_admin
    )
    return render_template("core/index.html", 
                            is_admin=is_admin,
                            title='EIM 3d prototipe',
                            body='body',
                            light=entity_dict['lights'], 
                            camera=entity_dict['camera'], 
                            entity=entity_dict['shape'],
                            line=entity_dict['line'],
                            figure=entity_dict['figure']
                            )

@core_bp.route('/entitys', methods=['GET'])
def get_entitys():
    return entity_dict['shape']