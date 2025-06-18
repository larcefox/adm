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

class Shape(db.Model):
    __tablename__ = "shape"
    __table_args__ = {"schema": db_schema}
    id = db.Column(
        db.UUID(as_uuid=True), primary_key=True,
        server_default=db.text("gen_random_uuid()"), nullable=False
    )
    data = db.Column(db.dialects.postgresql.JSONB, nullable=False, default=dict)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, server_default=db.text("now()"))
    user_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey(User.id), nullable=False)

    def __repr__(self) -> str:
        return f"<Shape {self.id}>"

class Light(db.Model):
    __tablename__ = "light"
    __table_args__ = {"schema": db_schema}
    id = db.Column(
        db.UUID(as_uuid=True), primary_key=True,
        server_default=db.text("gen_random_uuid()"), nullable=False
    )
    data = db.Column(db.dialects.postgresql.JSONB, nullable=False, default=dict)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, server_default=db.text("now()"))
    user_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey(User.id), nullable=False)

    def __repr__(self) -> str:
        return f"<Light {self.id}>"

class Line(db.Model):
    __tablename__ = "line"
    __table_args__ = {"schema": db_schema}
    id = db.Column(
        db.UUID(as_uuid=True), primary_key=True,
        server_default=db.text("gen_random_uuid()"), nullable=False
    )
    data = db.Column(db.dialects.postgresql.JSONB, nullable=False, default=dict)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, server_default=db.text("now()"))
    user_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey(User.id), nullable=False)

    def __repr__(self) -> str:
        return f"<Line {self.id}>"

class Figure(db.Model):
    __tablename__ = "figure"
    __table_args__ = {"schema": db_schema}
    id = db.Column(
        db.UUID(as_uuid=True), primary_key=True,
        server_default=db.text("gen_random_uuid()"), nullable=False
    )
    data = db.Column(db.dialects.postgresql.JSONB, nullable=False, default=dict)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, server_default=db.text("now()"))
    user_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey(User.id), nullable=False)

    def __repr__(self) -> str:
        return f"<Figure {self.id}>"

class Model(db.Model):
    __tablename__ = "model"
    __table_args__ = {"schema": db_schema}
    id = db.Column(
        db.UUID(as_uuid=True), primary_key=True,
        server_default=db.text("gen_random_uuid()"), nullable=False
    )
    data = db.Column(db.dialects.postgresql.JSONB, nullable=False, default=dict)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, server_default=db.text("now()"))
    user_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey(User.id), nullable=False)

    def __repr__(self) -> str:
        return f"<Model {self.id}>"

class Arch(db.Model):
    __tablename__ = "arch"
    __table_args__ = {"schema": db_schema}
    id = db.Column(
        db.UUID(as_uuid=True), primary_key=True,
        server_default=db.text("gen_random_uuid()"), nullable=False
    )
    data = db.Column(db.dialects.postgresql.JSONB, nullable=False, default=dict)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, server_default=db.text("now()"))
    user_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey(User.id), nullable=False)

    def __repr__(self) -> str:
        return f"<Arch {self.id}>"
