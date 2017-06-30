"""empty message

Revision ID: 6b1903b3c6a6
Revises: 
Create Date: 2017-06-30 13:30:13.805896

"""

# revision identifiers, used by Alembic.

import sqlalchemy as sa
from alembic import op

revision = '6b1903b3c6a6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('url',
                    sa.Column('id', sa.BigInteger(), nullable=False),
                    sa.Column('created_on', sa.DateTime(), nullable=True),
                    sa.Column('modified_on', sa.DateTime(), nullable=True),
                    sa.Column('url', sa.String(), nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('url')
                    )


def downgrade():
    op.drop_table('url')
