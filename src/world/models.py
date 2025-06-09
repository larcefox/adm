import uuid
import lib.load_env as lib_env
from loguru import logger
from src.accounts.models import User
from src import db
from datetime import datetime


# Settings
logger.add(
    "logs/world.log",
    format="{time} {level} {message}",
    level="INFO",
)

db_schema = lib_env.env["WORLD_DB_SCHEMA"]


class Entity(db.Model):
    __tablename__ = "entity"
    __table_args__ = {"schema": db_schema}
    id = db.Column(
        db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4(), nullable=False
    )
    data = db.Column(db.dialects.postgresql.JSONB, nullable=False, default=False)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.now())
    user_id = db.Column(
        db.UUID(as_uuid=True), db.ForeignKey(User.id), nullable=False
    )
    # author = db.relationship(User, backref="author", lazy=True)

    def __repr__(self) -> str:
        return f"<entity {self.name}>"