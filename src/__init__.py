from decouple import config
from flask import Flask, flash, redirect, url_for, request
from flask_login import LoginManager # Add this line
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from loguru import logger
import sys, subprocess, pathlib
from sqlalchemy import create_engine, inspect
from sqlalchemy.schema import CreateSchema


# Schema creation
schema = config('DB_SCHEMA')
world_schema = config('WORLD_DB_SCHEMA')
conn = create_engine(config('DATABASE_URL'))

# Creating schemas

with conn.connect() as connection:
    if not inspect(connection).has_schema(schema):
        connection.execute(CreateSchema(schema))
        connection.commit()
    
    if not inspect(connection).has_schema(world_schema):
        connection.execute(CreateSchema(world_schema))
        connection.commit()
    

# Settings
app = Flask(__name__)
app.config.from_object(config("APP_SETTINGS"))

login_manager = LoginManager() # Add this line
login_manager.init_app(app) # Add this line
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# logger
logger.add(sys.stderr, format="{time} {level} {message}", filter="admin", level="INFO")

# Registering blueprints
from src.accounts.views import accounts_bp
from src.core.views import core_bp
from src.world.views import world_bp

app.register_blueprint(accounts_bp)
app.register_blueprint(core_bp)
app.register_blueprint(world_bp)


# user_loader callback
from src.accounts.models import Role, User
@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == user_id).first()

# customize the default login process
login_manager.login_view = "accounts.login"

# customize the message category
login_manager.login_message_category = "danger"

# Flask Admin
from flask_admin import Admin, expose, AdminIndexView, menu
from flask_admin.contrib.sqla import ModelView
from sqlalchemy import inspect
from flask_login import current_user
from src.dinamo import base_model
from src.dinamo.models import module_factory


class_names = module_factory()
class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for('accounts.login'))
        return super(MyAdminIndexView, self).index()

admin = Admin(app, name='Dinamo', template_mode='bootstrap4', index_view=MyAdminIndexView())

class AuthModel(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated:
            is_admin = Role.query.join(User).where(User.id == current_user.get_id()).first().is_admin
        else:
            is_admin = False
        return current_user.is_authenticated and is_admin
    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('accounts.login', next=request.url))
    
admin.add_view(AuthModel(Role, db.session, 'Роли'))

class UsersView(AuthModel):
    column_display_pk = True
    column_hide_backrefs = False
    column_list = [c_attr.key for c_attr in inspect(User).mapper.column_attrs]

admin.add_view(UsersView(User, db.session, 'Пользователи'))

admin.add_link(menu.MenuLink(name='На сайт', category='', url='/'))

# Base model import to admin panel

class DinamoView(ModelView):
    column_display_pk = True
    column_hide_backrefs = False
    
    def __init__(self, model, session, **kwargs):
        columns = [c_attr.key for c_attr in inspect(model).mapper.column_attrs]
        super(DinamoView, self).__init__(model ,session,**kwargs)

def class_repr(class_name):
    return class_name

for class_name in class_names:
    model_class = eval(f"base_model.{class_name}")
    model_class.__class__.__repr__ = class_repr(class_name)
    print(model_class.__repr__(class_name))
    admin.add_view(DinamoView(eval(f"base_model.{class_name}"), db.session))
