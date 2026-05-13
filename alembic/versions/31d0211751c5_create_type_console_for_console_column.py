"""create type console for console column

Revision ID: 31d0211751c5
Revises: a9c10c169755
Create Date: 2026-05-12 16:20:01.379473

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '31d0211751c5'
down_revision: Union[str, Sequence[str], None] = 'a9c10c169755'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('consoles', sa.Column('type', sa.String(), nullable=True))
    pass


def downgrade() -> None:
    op.drop_column('consoles', 'type')
