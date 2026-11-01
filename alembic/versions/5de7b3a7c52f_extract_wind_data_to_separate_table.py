"""Extract wind data to separate table

Revision ID: 5de7b3a7c52f
Revises: df3b2aea1bdf
Create Date: 2026-11-01 14:51:37.455006

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '5de7b3a7c52f'
down_revision: Union[str, Sequence[str], None] = 'df3b2aea1bdf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_table('wind_records',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('weather_id', sa.Integer(), nullable=False),
        sa.Column('wind_degree', sa.Integer(), nullable=False),
        sa.Column('wind_kph', sa.Float(), nullable=False),
        sa.Column('wind_direction', postgresql.ENUM(name='winddirectionenum', create_type=False), nullable=False),
        sa.Column('wind_mph', sa.Float(), nullable=True),
        sa.Column('wind_gust_mph', sa.Float(), nullable=True),
        sa.Column('wind_gust_kph', sa.Float(), nullable=True),
        sa.ForeignKeyConstraint(['weather_id'], ['weather_records.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('weather_id')
    )

    op.execute("""
        INSERT INTO wind_records (weather_id, wind_degree, wind_kph, wind_direction, wind_mph, wind_gust_kph)
        SELECT id, wind_degree, wind_kph, wind_direction, wind_mph, gust_kph
        FROM weather_records;
    """)

    op.drop_column('weather_records', 'wind_degree')
    op.drop_column('weather_records', 'wind_kph')
    op.drop_column('weather_records', 'wind_direction')
    op.drop_column('weather_records', 'wind_mph')
    op.drop_column('weather_records', 'gust_kph')


def downgrade() -> None:
    # 1. Повертаємо колонки назад у weather_records
    op.add_column('weather_records', sa.Column('wind_degree', sa.Integer(), nullable=True))
    op.add_column('weather_records', sa.Column('wind_kph', sa.Float(), nullable=True))
    op.add_column('weather_records', sa.Column('wind_direction', postgresql.ENUM(name='winddirectionenum', create_type=False), nullable=True))
    op.add_column('weather_records', sa.Column('wind_mph', sa.Float(), nullable=True))
    op.add_column('weather_records', sa.Column('gust_kph', sa.Float(), nullable=True))

    op.execute("""
        UPDATE weather_records w
        SET wind_degree = r.wind_degree,
            wind_kph = r.wind_kph,
            wind_direction = r.wind_direction,
            wind_mph = r.wind_mph,
            gust_kph = r.wind_gust_kph
        FROM wind_records r
        WHERE w.id = r.weather_id;
    """)

    op.drop_table('wind_records')