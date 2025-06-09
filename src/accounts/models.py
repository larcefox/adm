from datetime import datetime
from src import bcrypt, db
import uuid
import lib.load_env as lib_env
from loguru import logger
from flask_login import UserMixin


# Settings
guest_id = "69860c71-5262-41dc-9b7c-913d3e6a99f9"
logger.add(
    "logs/log_file.log",
    format="{time} {level} {message}",
    filter="flask_models",
    level="INFO",
)
db_schema = lib_env.env["DB_SCHEMA"]


class Role(db.Model):
    __tablename__ = "role"
    __table_args__ = {"schema": db_schema}
    id = db.Column(
        db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False
    )
    name = db.Column(db.String(64), index=True)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    is_author = db.Column(db.Boolean, nullable=False, default=False)
    is_customer = db.Column(db.Boolean, nullable=False, default=False)
    is_guest = db.Column(db.Boolean, nullable=False, default=True)

    def __repr__(self) -> str:
        return f"<role {self.name}>"


class User(UserMixin, db.Model):
    __tablename__ = "users"
    __table_args__ = {"schema": db_schema}

    id = db.Column(
        db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False
    )
    name = db.Column(db.String(64), index=True)
    phone = db.Column(db.String(20))
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False)
    last_seen = db.Column(db.DateTime)
    role_id = db.Column(
        db.UUID(as_uuid=True), db.ForeignKey(Role.id), nullable=False, default=guest_id
    )
    role = db.relationship("Role", backref="user_role", lazy=True)

    def __init__(self, email, password, is_admin=False):
        self.email = email
        pwhash = bcrypt.generate_password_hash(password.encode("utf8"))
        self.password = pwhash.decode("utf8")
        self.created_on = datetime.now()

    def __repr__(self):
        return f"<user {self.name}>"
