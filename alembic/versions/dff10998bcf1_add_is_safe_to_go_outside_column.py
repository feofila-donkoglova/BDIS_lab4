"""Add is_safe_to_go_outside column

Revision ID: dff10998bcf1
Revises: 5de7b3a7c52f
Create Date: 2026-11-01 15:06:22.056124

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'dff10998bcf1'
down_revision: Union[str, Sequence[str], None] = '5de7b3a7c52f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('wind_records', sa.Column('is_safe_to_go_outside', sa.Boolean(), nullable=True))

    op.execute("""
        UPDATE wind_records 
        SET is_safe_to_go_outside = (wind_kph <= 36.0);
    """)


def downgrade() -> None:
    op.drop_column('wind_records', 'is_safe_to_go_outside')