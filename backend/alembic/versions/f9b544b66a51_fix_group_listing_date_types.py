"""fix group listing date types

Revision ID: f9b544b66a51
Revises: e3a1f8b2c940
Create Date: 2026-02-21 10:40:57.725274

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "f9b544b66a51"
down_revision: str | Sequence[str] | None = "e3a1f8b2c940"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_index(op.f("ix_group_listings_activity"), table_name="group_listings")
    op.drop_index(op.f("ix_group_listings_last_heartbeat"), table_name="group_listings")
    op.drop_column("group_listings", "created_at")
    op.drop_column("group_listings", "last_heartbeat")
    op.add_column(
        "group_listings",
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.add_column(
        "group_listings",
        sa.Column("last_heartbeat", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("group_listings", "last_heartbeat")
    op.drop_column("group_listings", "created_at")
    op.add_column("group_listings", sa.Column("created_at", sa.BIGINT(), nullable=False, server_default="0"))
    op.add_column("group_listings", sa.Column("last_heartbeat", sa.BIGINT(), nullable=False, server_default="0"))
    op.create_index(op.f("ix_group_listings_last_heartbeat"), "group_listings", ["last_heartbeat"], unique=False)
    op.create_index(op.f("ix_group_listings_activity"), "group_listings", ["activity"], unique=False)
