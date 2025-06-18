"""create shape update trigger

Revision ID: a3e8811fe9cb
Revises: 6dae38d24648
Create Date: 2025-06-17 23:16:27.451946

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'a3e8811fe9cb'
down_revision = '6dae38d24648'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
    CREATE OR REPLACE FUNCTION notify_shape_update()
    RETURNS TRIGGER AS $$
    BEGIN
      PERFORM pg_notify('shape_channel', row_to_json(NEW)::text);
      RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    """)

    op.execute("""
    CREATE TRIGGER shape_update_trigger
    AFTER INSERT OR UPDATE ON world.shape
    FOR EACH ROW EXECUTE FUNCTION notify_shape_update();
    """)


def downgrade():
    op.execute("DROP TRIGGER IF EXISTS shape_update_trigger ON world.shape;")
    op.execute("DROP FUNCTION IF EXISTS notify_shape_update();")