"""update User table

Revision ID: 2c307d52a17a
Revises: 147299881313
Create Date: 2023-10-28 18:41:24.813207

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '2c307d52a17a'
down_revision: Union[str, None] = '147299881313'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('user', sa.Column('date_joined', sa.DateTime(), nullable=False))
    op.add_column('user', sa.Column('last_login', sa.DateTime(), nullable=True))


def downgrade() -> None:
    op.drop_column('user', 'last_login')
    op.drop_column('user', 'date_joined')
