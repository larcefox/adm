"""update permission for notify

Revision ID: 1be405cba9c2
Revises: d88e8d6792e7
Create Date: 2025-06-18 20:56:16.556234

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import dotenv
import os


# revision identifiers, used by Alembic.
revision = '1be405cba9c2'
down_revision = 'd88e8d6792e7'
branch_labels = None
depends_on = None
database_user = os.getenv('DATABASE_USER')

def upgrade():
    op.execute(f"GRANT EXECUTE ON FUNCTION pg_notify(text, text) TO {database_user};")

def downgrade():
    op.execute("REVOKE EXECUTE ON FUNCTION pg_notify(text, text) FROM {database_user};")
