"""create User table

Revision ID: 147299881313
Revises: 14d6397bc3ba
Create Date: 2023-10-28 14:30:45.009055

"""
from typing import Sequence, Union

import fastapi_users_db_sqlalchemy
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '147299881313'
down_revision: Union[str, None] = '14d6397bc3ba'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('user',
                    sa.Column('username', sa.String(length=50), nullable=False),
                    sa.Column('first_name', sa.String(length=50), nullable=False),
                    sa.Column('last_name', sa.String(length=50), nullable=False),
                    sa.Column('birth_date', sa.Date(), nullable=True),
                    sa.Column('id', fastapi_users_db_sqlalchemy.generics.GUID(), nullable=False),
                    sa.Column('email', sa.String(length=320), nullable=False),
                    sa.Column('hashed_password', sa.String(length=1024), nullable=False),
                    sa.Column('is_active', sa.Boolean(), nullable=False),
                    sa.Column('is_superuser', sa.Boolean(), nullable=False),
                    sa.Column('is_verified', sa.Boolean(), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('username')
                    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.add_column('todo', sa.Column('user_id', fastapi_users_db_sqlalchemy.generics.GUID(), nullable=False))
    op.alter_column('todo', 'status_id',
                    existing_type=sa.UUID(),
                    nullable=False)
    op.create_foreign_key('todo_user_id_fkey', 'todo', 'user', ['user_id'], ['id'], onupdate='CASCADE',
                          ondelete='CASCADE')


def downgrade() -> None:
    op.drop_constraint('todo_user_id_fkey', 'todo', type_='foreignkey')
    op.alter_column('todo', 'status_id',
                    existing_type=sa.UUID(),
                    nullable=True)
    op.drop_column('todo', 'user_id')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
