"""add user table

Revision ID: b07374f70a08
Revises: 627a32fd1976
Create Date: 2024-12-01 21:02:43.215002

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b07374f70a08'
down_revision: Union[str, None] = '627a32fd1976'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('email', sa.String, nullable=False, unique=True),
        sa.Column('password', sa.String, nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()'))
    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
