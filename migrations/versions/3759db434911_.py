"""empty message

Revision ID: 3759db434911
Revises: 37bb4fa1bee1
Create Date: 2024-08-20 01:14:27.931021

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3759db434911'
down_revision = '37bb4fa1bee1'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("INSERT INTO auth.role VALUES ('69860c71-5262-41dc-9b7c-913d3e6a99f9','guest',false,false,false,true)")
    op.execute("INSERT INTO auth.role VALUES ('69860c71-5262-41dc-9b7c-913d3e6a9910','admin',true,false,false,true)")


def downgrade():
    pass
