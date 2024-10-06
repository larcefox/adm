from datetime import datetime
from src import bcrypt, db
import uuid
import lib.load_env as lib_env
from loguru import logger
from flask_login import UserMixin
from src.accounts.models import User


# Settings
logger.add(
    "logs/log_file.log",
    format="{time} {level} {message}",
    filter="flask_models",
    level="INFO",
)
db_schema = lib_env.env["DB_SCHEMA"]
