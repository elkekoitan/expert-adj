"""Add strategy_presets, backtest_runs, forward_runs

Revision ID: 002_strategy_and_runs
Revises: 001_initial
Create Date: 2025-11-10 11:00:00.000000
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "002_strategy_and_runs"
down_revision = "001_initial"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "strategy_presets",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("owner_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("ea_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("slug", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("symbol", sa.String(length=20), nullable=True),
        sa.Column("timeframe", sa.String(length=10), nullable=True),
        sa.Column("mode", sa.String(length=20), nullable=False, server_default="manual"),
        sa.Column(
            "parameters",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=sa.text("'{}'::jsonb"),
        ),
        sa.Column(
            "dynamic_policies",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=True,
        ),
        sa.Column("tags", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column(
            "status",
            sa.String(length=20),
            nullable=False,
            server_default="draft",
        ),
        sa.Column(
            "metrics_snapshot",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=True,
        ),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["owner_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"]),
        sa.ForeignKeyConstraint(["ea_id"], ["expert_advisors.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_strategy_presets_slug",
        "strategy_presets",
        ["slug"],
        unique=True,
    )

    op.create_table(
        "backtest_runs",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("owner_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("preset_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("ea_version_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("symbol", sa.String(length=20), nullable=False),
        sa.Column("timeframe", sa.String(length=10), nullable=False),
        sa.Column("date_from", sa.String(), nullable=False),
        sa.Column("date_to", sa.String(), nullable=False),
        sa.Column(
            "engine",
            sa.String(length=50),
            nullable=False,
            server_default="mt5_local",
        ),
        sa.Column(
            "parameters",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=sa.text("'{}'::jsonb"),
        ),
        sa.Column(
            "status",
            sa.String(length=20),
            nullable=False,
            server_default="queued",
        ),
        sa.Column(
            "metrics",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=True,
        ),
        sa.Column("report_ref", sa.String(length=500), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["owner_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"]),
        sa.ForeignKeyConstraint(["preset_id"], ["strategy_presets.id"]),
        sa.ForeignKeyConstraint(["ea_version_id"], ["ea_versions.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "forward_runs",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("owner_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("preset_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("account_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "status",
            sa.String(length=20),
            nullable=False,
            server_default="deploying",
        ),
        sa.Column(
            "allocation",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=True,
        ),
        sa.Column(
            "live_metrics",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=True,
        ),
        sa.Column("started_at", sa.String(), nullable=True),
        sa.Column("stopped_at", sa.String(), nullable=True),
        sa.Column("last_heartbeat_at", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["owner_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"]),
        sa.ForeignKeyConstraint(["preset_id"], ["strategy_presets.id"]),
        sa.ForeignKeyConstraint(["account_id"], ["trading_accounts.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("forward_runs")
    op.drop_table("backtest_runs")
    op.drop_index("ix_strategy_presets_slug", table_name="strategy_presets")
    op.drop_table("strategy_presets")