"""delete username field from user table

Revision ID: fb54881cd457
Revises: 2c307d52a17a
Create Date: 2023-10-29 13:53:32.560677

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'fb54881cd457'
down_revision: Union[str, None] = '2c307d52a17a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('user', 'birth_date',
                    existing_type=sa.DATE(),
                    type_=sa.DateTime(),
                    existing_nullable=True)
    op.drop_constraint('user_username_key', 'user', type_='unique')
    op.drop_column('user', 'username')


def downgrade() -> None:
    op.add_column('user', sa.Column('username', sa.VARCHAR(length=50), autoincrement=False, nullable=True))
    op.create_unique_constraint('user_username_key', 'user', ['username'])
    op.alter_column('user', 'birth_date',
                    existing_type=sa.DateTime(),
                    type_=sa.DATE(),
                    existing_nullable=True)
