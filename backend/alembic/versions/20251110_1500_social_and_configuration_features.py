"""Social and configuration features

Revision ID: 002_social_config
Revises: 001_initial
Create Date: 2025-11-10 15:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '002_social_config'
down_revision = '001_initial'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create user_profiles table
    op.create_table(
        'user_profiles',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('bio', sa.Text(), nullable=True),
        sa.Column('website', sa.String(length=500), nullable=True),
        sa.Column('twitter', sa.String(length=100), nullable=True),
        sa.Column('linkedin', sa.String(length=100), nullable=True),
        sa.Column('experience_level', sa.String(length=20), nullable=True),
        sa.Column('preferred_markets', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('risk_tolerance', sa.String(length=20), nullable=True),
        sa.Column('trading_style', sa.String(length=50), nullable=True),
        sa.Column('profile_visibility', sa.String(length=20), nullable=True),
        sa.Column('show_activity', sa.Boolean(), nullable=True),
        sa.Column('show_in_search', sa.Boolean(), nullable=True),
        sa.Column('reputation_score', sa.Integer(), nullable=True),
        sa.Column('followers_count', sa.Integer(), nullable=True),
        sa.Column('following_count', sa.Integer(), nullable=True),
        sa.Column('eas_uploaded', sa.Integer(), nullable=True),
        sa.Column('configs_shared', sa.Integer(), nullable=True),
        sa.Column('is_verified', sa.Boolean(), nullable=True),
        sa.Column('verification_date', sa.String(), nullable=True),
        sa.Column('created_at', sa.String(), nullable=True),
        sa.Column('updated_at', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id')
    )

    # Create user_follows table
    op.create_table(
        'user_follows',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('follower_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('following_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.String(), nullable=True),
        sa.Column('updated_at', sa.String(), nullable=True),
        sa.CheckConstraint('follower_id != following_id', name='check_no_self_follow'),
        sa.ForeignKeyConstraint(['follower_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['following_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('follower_id', 'following_id', name='unique_follow')
    )
    op.create_index(op.f('ix_user_follows_follower'), 'user_follows', ['follower_id'], unique=False)
    op.create_index(op.f('ix_user_follows_following'), 'user_follows', ['following_id'], unique=False)

    # Create ea_configurations table
    op.create_table(
        'ea_configurations',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('ea_version_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('parameters', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('symbol', sa.String(length=20), nullable=True),
        sa.Column('timeframe', sa.String(length=10), nullable=True),
        sa.Column('backtest_from', sa.Date(), nullable=True),
        sa.Column('backtest_to', sa.Date(), nullable=True),
        sa.Column('profit_factor', sa.Numeric(precision=10, scale=4), nullable=True),
        sa.Column('win_rate', sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column('total_trades', sa.Integer(), nullable=True),
        sa.Column('net_profit', sa.Numeric(precision=15, scale=2), nullable=True),
        sa.Column('max_drawdown', sa.Numeric(precision=15, scale=2), nullable=True),
        sa.Column('sharpe_ratio', sa.Numeric(precision=10, scale=4), nullable=True),
        sa.Column('visibility', sa.String(length=20), nullable=True),
        sa.Column('is_featured', sa.Boolean(), nullable=True),
        sa.Column('likes_count', sa.Integer(), nullable=True),
        sa.Column('uses_count', sa.Integer(), nullable=True),
        sa.Column('forks_count', sa.Integer(), nullable=True),
        sa.Column('views_count', sa.Integer(), nullable=True),
        sa.Column('parent_config_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('tags', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.String(), nullable=True),
        sa.Column('updated_at', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['ea_version_id'], ['ea_versions.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['parent_config_id'], ['ea_configurations.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ea_configurations_visibility'), 'ea_configurations', ['visibility'], unique=False)
    op.create_index(op.f('ix_ea_configurations_featured'), 'ea_configurations', ['is_featured'], unique=False)

    # Create comments table
    op.create_table(
        'comments',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('commentable_type', sa.String(length=50), nullable=False),
        sa.Column('commentable_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('parent_comment_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('is_hidden', sa.Boolean(), nullable=True),
        sa.Column('is_deleted', sa.Boolean(), nullable=True),
        sa.Column('deleted_at', sa.String(), nullable=True),
        sa.Column('likes_count', sa.Integer(), nullable=True),
        sa.Column('replies_count', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.String(), nullable=True),
        sa.Column('updated_at', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['parent_comment_id'], ['comments.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_comments_commentable'), 'comments', ['commentable_type', 'commentable_id'], unique=False)

    # Create likes table
    op.create_table(
        'likes',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('likeable_type', sa.String(length=50), nullable=False),
        sa.Column('likeable_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.String(), nullable=True),
        sa.Column('updated_at', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id', 'likeable_type', 'likeable_id', name='unique_like')
    )
    op.create_index(op.f('ix_likes_likeable'), 'likes', ['likeable_type', 'likeable_id'], unique=False)

    # Create notifications table
    op.create_table(
        'notifications',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('type', sa.String(length=50), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('content', sa.Text(), nullable=True),
        sa.Column('data', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('is_read', sa.Boolean(), nullable=True),
        sa.Column('read_at', sa.String(), nullable=True),
        sa.Column('action_url', sa.String(length=500), nullable=True),
        sa.Column('created_at', sa.String(), nullable=True),
        sa.Column('updated_at', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_notifications_user_unread'), 'notifications', ['user_id', 'is_read', 'created_at'], unique=False)

    # Create direct_messages table
    op.create_table(
        'direct_messages',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('sender_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('recipient_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('attachments', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('is_read', sa.Boolean(), nullable=True),
        sa.Column('read_at', sa.String(), nullable=True),
        sa.Column('is_deleted_by_sender', sa.Boolean(), nullable=True),
        sa.Column('is_deleted_by_recipient', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.String(), nullable=True),
        sa.Column('updated_at', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['sender_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['recipient_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_direct_messages_conversation'), 'direct_messages', ['sender_id', 'recipient_id', 'created_at'], unique=False)
    op.create_index(op.f('ix_direct_messages_unread'), 'direct_messages', ['recipient_id', 'is_read'], unique=False)

    # Create workspaces table
    op.create_table(
        'workspaces',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('owner_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('visibility', sa.String(length=20), nullable=True),
        sa.Column('settings', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.String(), nullable=True),
        sa.Column('updated_at', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Create workspace_members table
    op.create_table(
        'workspace_members',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('workspace_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('role', sa.String(length=20), nullable=True),
        sa.Column('joined_at', sa.String(), nullable=True),
        sa.Column('created_at', sa.String(), nullable=True),
        sa.Column('updated_at', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['workspace_id'], ['workspaces.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('workspace_id', 'user_id', name='unique_workspace_member')
    )

    # Create badges table
    op.create_table(
        'badges',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('icon', sa.String(length=100), nullable=True),
        sa.Column('category', sa.String(length=50), nullable=True),
        sa.Column('criteria', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('display_order', sa.Integer(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.String(), nullable=True),
        sa.Column('updated_at', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )

    # Create user_badges table
    op.create_table(
        'user_badges',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('badge_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('earned_at', sa.String(), nullable=True),
        sa.Column('created_at', sa.String(), nullable=True),
        sa.Column('updated_at', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['badge_id'], ['badges.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id', 'badge_id', name='unique_user_badge')
    )

    # Create audit_logs table
    op.create_table(
        'audit_logs',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('action', sa.String(length=100), nullable=False),
        sa.Column('resource_type', sa.String(length=50), nullable=True),
        sa.Column('resource_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('details', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('ip_address', sa.String(length=45), nullable=True),
        sa.Column('user_agent', sa.Text(), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=True),
        sa.Column('created_at', sa.String(), nullable=True),
        sa.Column('updated_at', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_audit_logs_user_action'), 'audit_logs', ['user_id', 'action', 'created_at'], unique=False)
    op.create_index(op.f('ix_audit_logs_resource'), 'audit_logs', ['resource_type', 'resource_id'], unique=False)

    # Create oauth_connections table
    op.create_table(
        'oauth_connections',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('provider', sa.String(length=50), nullable=False),
        sa.Column('provider_user_id', sa.String(length=255), nullable=False),
        sa.Column('access_token', sa.Text(), nullable=True),
        sa.Column('refresh_token', sa.Text(), nullable=True),
        sa.Column('expires_at', sa.String(), nullable=True),
        sa.Column('profile_data', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.String(), nullable=True),
        sa.Column('updated_at', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('provider', 'provider_user_id', name='unique_oauth_provider_user')
    )
    op.create_index(op.f('ix_oauth_connections_user'), 'oauth_connections', ['user_id'], unique=False)


def downgrade() -> None:
    # Drop all tables in reverse order
    op.drop_index(op.f('ix_oauth_connections_user'), table_name='oauth_connections')
    op.drop_table('oauth_connections')
    op.drop_index(op.f('ix_audit_logs_resource'), table_name='audit_logs')
    op.drop_index(op.f('ix_audit_logs_user_action'), table_name='audit_logs')
    op.drop_table('audit_logs')
    op.drop_table('user_badges')
    op.drop_table('badges')
    op.drop_table('workspace_members')
    op.drop_table('workspaces')
    op.drop_index(op.f('ix_direct_messages_unread'), table_name='direct_messages')
    op.drop_index(op.f('ix_direct_messages_conversation'), table_name='direct_messages')
    op.drop_table('direct_messages')
    op.drop_index(op.f('ix_notifications_user_unread'), table_name='notifications')
    op.drop_table('notifications')
    op.drop_index(op.f('ix_likes_likeable'), table_name='likes')
    op.drop_table('likes')
    op.drop_index(op.f('ix_comments_commentable'), table_name='comments')
    op.drop_table('comments')
    op.drop_index(op.f('ix_ea_configurations_featured'), table_name='ea_configurations')
    op.drop_index(op.f('ix_ea_configurations_visibility'), table_name='ea_configurations')
    op.drop_table('ea_configurations')
    op.drop_index(op.f('ix_user_follows_following'), table_name='user_follows')
    op.drop_index(op.f('ix_user_follows_follower'), table_name='user_follows')
    op.drop_table('user_follows')
    op.drop_table('user_profiles')
