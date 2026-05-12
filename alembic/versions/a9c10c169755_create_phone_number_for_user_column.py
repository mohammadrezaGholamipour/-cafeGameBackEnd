"""Create phone number for user column

Revision ID: a9c10c169755
Revises: 
Create Date: 2026-05-12 16:11:00.279131

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a9c10c169755'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("phoneNumber", sa.String, nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    pass
