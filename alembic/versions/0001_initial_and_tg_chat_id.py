"""initial migration + tg_chat_id in users

Revision ID: 0001_initial_and_tg_chat_id
Revises: 
Create Date: 2026-02-10

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0001_initial_and_tg_chat_id'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Таблица regions
    op.create_table(
        'regions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('code', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # Таблица cities
    op.create_table(
        'cities',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('region_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.ForeignKeyConstraint(['region_id'], ['regions.id']),
        sa.PrimaryKeyConstraint('id')
    )

    # Таблица clinics
    op.create_table(
        'clinics',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('city_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('address', sa.String(), nullable=True),
        sa.Column('aliases', sa.String(), nullable=True),
        sa.Column('url', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['city_id'], ['cities.id']),
        sa.PrimaryKeyConstraint('id')
    )

    # Таблица doctors
    op.create_table(
        'doctors',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('clinic_id', sa.Integer(), nullable=False),
        sa.Column('full_name', sa.String(), nullable=False),
        sa.Column('specialty', sa.String(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.ForeignKeyConstraint(['clinic_id'], ['clinics.id']),
        sa.PrimaryKeyConstraint('id')
    )

    # Таблица users
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('tg_user_id', sa.Integer(), nullable=False),
        sa.Column('tg_chat_id', sa.Integer(), nullable=True),  # ← добавляем сразу
        sa.Column('username', sa.String(), nullable=True),
        sa.Column('first_name', sa.String(), nullable=True),
        sa.Column('last_name', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('tg_user_id')
    )

    # Таблица monitoring_tasks
    op.create_table(
        'monitoring_tasks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('tg_chat_id', sa.Integer(), nullable=False),
        sa.Column('region_id', sa.Integer(), nullable=False),
        sa.Column('city_id', sa.Integer(), nullable=False),
        sa.Column('clinic_id', sa.Integer(), nullable=False),
        sa.Column('doctor_id', sa.Integer(), nullable=False),
        sa.Column('mode', sa.String(), nullable=False, server_default='auto'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.ForeignKeyConstraint(['region_id'], ['regions.id']),
        sa.ForeignKeyConstraint(['city_id'], ['cities.id']),
        sa.ForeignKeyConstraint(['clinic_id'], ['clinics.id']),
        sa.ForeignKeyConstraint(['doctor_id'], ['doctors.id']),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('monitoring_tasks')
    op.drop_table('users')
    op.drop_table('doctors')
    op.drop_table('clinics')
    op.drop_table('cities')
    op.drop_table('regions')
