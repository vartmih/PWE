"""create table Todo and Status

Revision ID: 14d6397bc3ba
Revises: 
Create Date: 2023-10-16 23:00:55.764539

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '14d6397bc3ba'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('status',
                    sa.Column('id', sa.Uuid(), nullable=False, server_default=sa.text('gen_random_uuid()')),
                    sa.Column('status_name', sa.String(), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('todo',
                    sa.Column('id', sa.Uuid(), nullable=False),
                    sa.Column('todo', sa.String(length=150), nullable=False),
                    sa.Column('modified_date', sa.DateTime(), nullable=True),
                    sa.Column('status_id', sa.Uuid(), nullable=True),
                    sa.Column('created_date', sa.DateTime(), nullable=False),
                    sa.ForeignKeyConstraint(['status_id'], ['status.id'], onupdate='CASCADE', ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.execute(
        """INSERT INTO status (status_name) VALUES ('Запланировано'), ('Выполнено'),
        ('В ожидании'), ('Отменено'), ('В работе');"""
    )


def downgrade() -> None:
    op.drop_table('todo')
    op.drop_table('status')
