"""create group_listings

Revision ID: e3a1f8b2c940
Revises:
Create Date: 2026-02-20

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "e3a1f8b2c940"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "group_listings",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("player_name", sa.String(12), nullable=False),
        sa.Column("activity", sa.String(50), nullable=False),
        sa.Column("current_size", sa.Integer(), nullable=False),
        sa.Column("max_size", sa.Integer(), nullable=False),
        sa.Column("description", sa.String(200), nullable=False, server_default=""),
        sa.Column("created_at", sa.BigInteger(), nullable=False),
        sa.Column("last_heartbeat", sa.BigInteger(), nullable=False),
    )
    op.create_index("ix_group_listings_activity", "group_listings", ["activity"])
    op.create_index("ix_group_listings_last_heartbeat", "group_listings", ["last_heartbeat"])


def downgrade() -> None:
    op.drop_index("ix_group_listings_last_heartbeat", "group_listings")
    op.drop_index("ix_group_listings_activity", "group_listings")
    op.drop_table("group_listings")
