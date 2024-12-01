"""add content column to post table

Revision ID: 627a32fd1976
Revises: f977952a6911
Create Date: 2024-12-01 20:58:39.641413

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '627a32fd1976'
down_revision: Union[str, None] = 'f977952a6911'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
