"""Initial schema with all models

Revision ID: 001_initial
Revises:
Create Date: 2025-11-10 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create organizations table
    op.create_table(
        'organizations',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('slug', sa.String(length=255), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.String(), nullable=True),
        sa.Column('updated_at', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_organizations_slug'), 'organizations', ['slug'], unique=True)

    # Create users table
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('organization_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('username', sa.String(length=100), nullable=True),
        sa.Column('full_name', sa.String(length=255), nullable=True),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('is_superuser', sa.Boolean(), nullable=True),
        sa.Column('is_verified', sa.Boolean(), nullable=True),
        sa.Column('totp_secret', sa.String(length=64), nullable=True),
        sa.Column('totp_enabled', sa.Boolean(), nullable=True),
        sa.Column('last_login', sa.String(), nullable=True),
        sa.Column('created_at', sa.String(), nullable=True),
        sa.Column('updated_at', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)

    # Create expert_advisors table
    op.create_table(
        'expert_advisors',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('organization_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('owner_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('platform', sa.String(length=10), nullable=False),
        sa.Column('tags', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.String(), nullable=True),
        sa.Column('updated_at', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ),
        sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_expert_advisors_name'), 'expert_advisors', ['name'], unique=False)

    # Create instruments table
    op.create_table(
        'instruments',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('symbol', sa.String(length=20), nullable=False),
        sa.Column('broker', sa.String(length=100), nullable=True),
        sa.Column('description', sa.String(length=255), nullable=True),
        sa.Column('instrument_type', sa.String(length=50), nullable=True),
        sa.Column('base_currency', sa.String(length=10), nullable=True),
        sa.Column('quote_currency', sa.String(length=10), nullable=True),
        sa.Column('point_value', sa.Numeric(precision=10, scale=5), nullable=True),
        sa.Column('contract_size', sa.Numeric(precision=15, scale=2), nullable=True),
        sa.Column('min_lot', sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column('max_lot', sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column('lot_step', sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.String(), nullable=True),
        sa.Column('updated_at', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_instruments_symbol'), 'instruments', ['symbol'], unique=True)

    # Create trading_accounts table
    op.create_table(
        'trading_accounts',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('owner_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('platform', sa.String(length=10), nullable=False),
        sa.Column('broker_server', sa.String(length=100), nullable=False),
        sa.Column('account_number', sa.String(length=50), nullable=False),
        sa.Column('account_type', sa.String(length=20), nullable=False),
        sa.Column('label', sa.String(length=255), nullable=True),
        sa.Column('encrypted_password', sa.String(length=500), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('is_connected', sa.Boolean(), nullable=True),
        sa.Column('balance', sa.Numeric(precision=15, scale=2), nullable=True),
        sa.Column('equity', sa.Numeric(precision=15, scale=2), nullable=True),
        sa.Column('margin', sa.Numeric(precision=15, scale=2), nullable=True),
        sa.Column('free_margin', sa.Numeric(precision=15, scale=2), nullable=True),
        sa.Column('leverage', sa.Integer(), nullable=True),
        sa.Column('currency', sa.String(length=10), nullable=True),
        sa.Column('last_heartbeat', sa.String(), nullable=True),
        sa.Column('meta_data', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.String(), nullable=True),
        sa.Column('updated_at', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create ea_versions table
    op.create_table(
        'ea_versions',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('ea_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('version', sa.String(length=50), nullable=False),
        sa.Column('build_hash', sa.String(length=64), nullable=True),
        sa.Column('compiled_file_path', sa.String(length=500), nullable=False),
        sa.Column('source_file_path', sa.String(length=500), nullable=True),
        sa.Column('source_present', sa.Boolean(), nullable=True),
        sa.Column('requires_sdk', sa.Boolean(), nullable=True),
        sa.Column('compiled_at', sa.String(), nullable=True),
        sa.Column('meta_data', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.String(), nullable=True),
        sa.Column('updated_at', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['ea_id'], ['expert_advisors.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ea_versions_build_hash'), 'ea_versions', ['build_hash'], unique=False)

    # Create optimization_sessions table
    op.create_table(
        'optimization_sessions',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('ea_version_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('owner_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=True),
        sa.Column('symbols', postgresql.ARRAY(sa.String()), nullable=False),
        sa.Column('timeframes', postgresql.ARRAY(sa.String()), nullable=False),
        sa.Column('date_from', sa.Date(), nullable=False),
        sa.Column('date_to', sa.Date(), nullable=False),
        sa.Column('optimization_method', sa.String(length=50), nullable=False),
        sa.Column('target_metric', sa.String(length=50), nullable=False),
        sa.Column('walk_forward_enabled', sa.Boolean(), nullable=True),
        sa.Column('wf_config', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('total_iterations', sa.Integer(), nullable=True),
        sa.Column('completed_iterations', sa.Integer(), nullable=True),
        sa.Column('best_parameters', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('best_score', sa.Numeric(precision=15, scale=4), nullable=True),
        sa.Column('started_at', sa.String(), nullable=True),
        sa.Column('completed_at', sa.String(), nullable=True),
        sa.Column('meta_data', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('error_message', sa.String(), nullable=True),
        sa.Column('created_at', sa.String(), nullable=True),
        sa.Column('updated_at', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['ea_version_id'], ['ea_versions.id'], ),
        sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create live_sessions table
    op.create_table(
        'live_sessions',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('account_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('ea_version_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('symbol', sa.String(length=20), nullable=False),
        sa.Column('timeframe', sa.String(length=10), nullable=False),
        sa.Column('parameters', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('initial_balance', sa.Numeric(precision=15, scale=2), nullable=True),
        sa.Column('current_profit', sa.Numeric(precision=15, scale=2), nullable=True),
        sa.Column('peak_profit', sa.Numeric(precision=15, scale=2), nullable=True),
        sa.Column('current_drawdown', sa.Numeric(precision=15, scale=2), nullable=True),
        sa.Column('max_drawdown', sa.Numeric(precision=15, scale=2), nullable=True),
        sa.Column('total_trades', sa.Integer(), nullable=True),
        sa.Column('winning_trades', sa.Integer(), nullable=True),
        sa.Column('losing_trades', sa.Integer(), nullable=True),
        sa.Column('threshold_policy', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('started_at', sa.String(), nullable=True),
        sa.Column('stopped_at', sa.String(), nullable=True),
        sa.Column('meta_data', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.String(), nullable=True),
        sa.Column('updated_at', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['account_id'], ['trading_accounts.id'], ),
        sa.ForeignKeyConstraint(['ea_version_id'], ['ea_versions.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create ea_parameters table
    op.create_table(
        'ea_parameters',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('ea_version_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('parameter_type', sa.String(length=50), nullable=False),
        sa.Column('default_value', sa.String(length=255), nullable=True),
        sa.Column('min_value', sa.String(length=255), nullable=True),
        sa.Column('max_value', sa.String(length=255), nullable=True),
        sa.Column('step_value', sa.String(length=255), nullable=True),
        sa.Column('enum_values', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('is_optimizable', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.String(), nullable=True),
        sa.Column('updated_at', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['ea_version_id'], ['ea_versions.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create dependencies table
    op.create_table(
        'dependencies',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('ea_version_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('dependency_type', sa.String(length=50), nullable=False),
        sa.Column('filename', sa.String(length=255), nullable=False),
        sa.Column('file_path', sa.String(length=500), nullable=False),
        sa.Column('checksum', sa.String(length=64), nullable=True),
        sa.Column('created_at', sa.String(), nullable=True),
        sa.Column('updated_at', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['ea_version_id'], ['ea_versions.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create backtest_results table
    op.create_table(
        'backtest_results',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('optimization_session_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('ea_version_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('symbol', sa.String(length=20), nullable=False),
        sa.Column('timeframe', sa.String(length=10), nullable=False),
        sa.Column('test_from', sa.Date(), nullable=False),
        sa.Column('test_to', sa.Date(), nullable=False),
        sa.Column('parameters', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('is_training', sa.Boolean(), nullable=True),
        sa.Column('is_oos', sa.Boolean(), nullable=True),
        sa.Column('initial_deposit', sa.Numeric(precision=15, scale=2), nullable=True),
        sa.Column('leverage', sa.Integer(), nullable=True),
        sa.Column('modeling_quality', sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column('net_profit', sa.Numeric(precision=15, scale=2), nullable=True),
        sa.Column('gross_profit', sa.Numeric(precision=15, scale=2), nullable=True),
        sa.Column('gross_loss', sa.Numeric(precision=15, scale=2), nullable=True),
        sa.Column('profit_factor', sa.Numeric(precision=10, scale=4), nullable=True),
        sa.Column('expected_payoff', sa.Numeric(precision=15, scale=2), nullable=True),
        sa.Column('total_trades', sa.Integer(), nullable=True),
        sa.Column('winning_trades', sa.Integer(), nullable=True),
        sa.Column('losing_trades', sa.Integer(), nullable=True),
        sa.Column('win_rate', sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column('largest_win', sa.Numeric(precision=15, scale=2), nullable=True),
        sa.Column('largest_loss', sa.Numeric(precision=15, scale=2), nullable=True),
        sa.Column('average_win', sa.Numeric(precision=15, scale=2), nullable=True),
        sa.Column('average_loss', sa.Numeric(precision=15, scale=2), nullable=True),
        sa.Column('max_drawdown', sa.Numeric(precision=15, scale=2), nullable=True),
        sa.Column('max_drawdown_percent', sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column('relative_drawdown', sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column('sharpe_ratio', sa.Numeric(precision=10, scale=4), nullable=True),
        sa.Column('sortino_ratio', sa.Numeric(precision=10, scale=4), nullable=True),
        sa.Column('calmar_ratio', sa.Numeric(precision=10, scale=4), nullable=True),
        sa.Column('recovery_factor', sa.Numeric(precision=10, scale=4), nullable=True),
        sa.Column('composite_score', sa.Numeric(precision=10, scale=4), nullable=True),
        sa.Column('report_html_path', sa.String(length=500), nullable=True),
        sa.Column('report_xml_path', sa.String(length=500), nullable=True),
        sa.Column('trades_csv_path', sa.String(length=500), nullable=True),
        sa.Column('terminal_build', sa.String(length=50), nullable=True),
        sa.Column('data_version', sa.String(length=50), nullable=True),
        sa.Column('meta_data', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.String(), nullable=True),
        sa.Column('updated_at', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['optimization_session_id'], ['optimization_sessions.id'], ),
        sa.ForeignKeyConstraint(['ea_version_id'], ['ea_versions.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create optimization_batches table
    op.create_table(
        'optimization_batches',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('session_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('algorithm', sa.String(length=50), nullable=False),
        sa.Column('parameter_space', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('statistics', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.String(), nullable=True),
        sa.Column('updated_at', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['session_id'], ['optimization_sessions.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create trades table
    op.create_table(
        'trades',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('session_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('ticket', sa.Integer(), nullable=False),
        sa.Column('symbol', sa.String(length=20), nullable=False),
        sa.Column('trade_type', sa.String(length=10), nullable=False),
        sa.Column('volume', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('open_price', sa.Numeric(precision=15, scale=5), nullable=False),
        sa.Column('close_price', sa.Numeric(precision=15, scale=5), nullable=False),
        sa.Column('stop_loss', sa.Numeric(precision=15, scale=5), nullable=True),
        sa.Column('take_profit', sa.Numeric(precision=15, scale=5), nullable=True),
        sa.Column('profit', sa.Numeric(precision=15, scale=2), nullable=False),
        sa.Column('commission', sa.Numeric(precision=15, scale=2), nullable=True),
        sa.Column('swap', sa.Numeric(precision=15, scale=2), nullable=True),
        sa.Column('open_time', sa.String(), nullable=False),
        sa.Column('close_time', sa.String(), nullable=False),
        sa.Column('comment', sa.String(length=255), nullable=True),
        sa.Column('meta_data', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.String(), nullable=True),
        sa.Column('updated_at', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['session_id'], ['live_sessions.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_trades_ticket'), 'trades', ['ticket'], unique=False)

    # Create positions table
    op.create_table(
        'positions',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('session_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('ticket', sa.Integer(), nullable=False),
        sa.Column('symbol', sa.String(length=20), nullable=False),
        sa.Column('position_type', sa.String(length=10), nullable=False),
        sa.Column('volume', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('open_price', sa.Numeric(precision=15, scale=5), nullable=False),
        sa.Column('current_price', sa.Numeric(precision=15, scale=5), nullable=True),
        sa.Column('stop_loss', sa.Numeric(precision=15, scale=5), nullable=True),
        sa.Column('take_profit', sa.Numeric(precision=15, scale=5), nullable=True),
        sa.Column('profit', sa.Numeric(precision=15, scale=2), nullable=True),
        sa.Column('commission', sa.Numeric(precision=15, scale=2), nullable=True),
        sa.Column('swap', sa.Numeric(precision=15, scale=2), nullable=True),
        sa.Column('open_time', sa.String(), nullable=False),
        sa.Column('comment', sa.String(length=255), nullable=True),
        sa.Column('meta_data', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.String(), nullable=True),
        sa.Column('updated_at', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['session_id'], ['live_sessions.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_positions_ticket'), 'positions', ['ticket'], unique=False)


def downgrade() -> None:
    # Drop all tables in reverse order
    op.drop_index(op.f('ix_positions_ticket'), table_name='positions')
    op.drop_table('positions')
    op.drop_index(op.f('ix_trades_ticket'), table_name='trades')
    op.drop_table('trades')
    op.drop_table('optimization_batches')
    op.drop_table('backtest_results')
    op.drop_table('dependencies')
    op.drop_table('ea_parameters')
    op.drop_table('live_sessions')
    op.drop_table('optimization_sessions')
    op.drop_index(op.f('ix_ea_versions_build_hash'), table_name='ea_versions')
    op.drop_table('ea_versions')
    op.drop_table('trading_accounts')
    op.drop_index(op.f('ix_instruments_symbol'), table_name='instruments')
    op.drop_table('instruments')
    op.drop_index(op.f('ix_expert_advisors_name'), table_name='expert_advisors')
    op.drop_table('expert_advisors')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_organizations_slug'), table_name='organizations')
    op.drop_table('organizations')
