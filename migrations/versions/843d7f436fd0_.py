"""empty message

Revision ID: 843d7f436fd0
Revises: a3e8811fe9cb
Create Date: 2025-06-18 12:55:28.938840

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '843d7f436fd0'
down_revision = 'a3e8811fe9cb'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
        CREATE OR REPLACE FUNCTION world.notify_shape_update()
        RETURNS TRIGGER AS $$
        BEGIN
          PERFORM pg_notify('shape_channel', row_to_json(NEW)::text);
          RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
               """)

    op.execute("""
                CREATE OR REPLACE TRIGGER shape_update_trigger
                AFTER INSERT OR UPDATE ON world.shape
                FOR EACH ROW EXECUTE FUNCTION world.notify_shape_update();
               """)

def downgrade():
    op.execute("DROP TRIGGER IF EXISTS shape_update_trigger ON world.shape;")
    op.execute("DROP FUNCTION IF EXISTS notify_shape_update();")
