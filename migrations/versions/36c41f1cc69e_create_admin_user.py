"""create admin user

Revision ID: 36c41f1cc69e
Revises: 1be405cba9c2
Create Date: 2025-08-05 19:09:13.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '36c41f1cc69e'
down_revision = '1be405cba9c2'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
        INSERT INTO auth.users (id, email, password, created_on, role_id)
        VALUES ('d71de913-2b25-4746-9cee-11a6827e6a00', 'larcefox@yandex.ru',
                '$2b$12$K/E7wPBO1QdbKyimVpWBaOpcL/WGpSPqJvjLBevOTuYf1c.3iypMe', NOW(),
                (SELECT id FROM auth.role WHERE is_admin = TRUE LIMIT 1))
        ON CONFLICT (email) DO NOTHING;
    """)


def downgrade():
    op.execute("DELETE FROM auth.users WHERE email='larcefox@yandex.ru';")
