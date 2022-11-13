"""Added core tables for app

Revision ID: 58b9dc6b9d2e
Revises: 57b460a916d4
Create Date: 2022-11-13 15:52:50.220883

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '58b9dc6b9d2e'
down_revision = '57b460a916d4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_category_id'), 'category', ['id'], unique=False)
    op.create_index(op.f('ix_category_name'), 'category', ['name'], unique=False)
    op.create_table('game',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('image_url', sa.String(), nullable=True),
    sa.Column('release_timestamp', sa.DateTime(timezone=True), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_game_id'), 'game', ['id'], unique=False)
    op.create_index(op.f('ix_game_name'), 'game', ['name'], unique=False)
    op.create_table('source',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('url', sa.String(), nullable=True),
    sa.Column('user_reviews_url', sa.String(), nullable=True),
    sa.Column('critic_reviews_url', sa.String(), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('critic_reviews_url'),
    sa.UniqueConstraint('user_reviews_url')
    )
    op.create_index(op.f('ix_source_id'), 'source', ['id'], unique=False)
    op.create_index(op.f('ix_source_url'), 'source', ['url'], unique=True)
    op.create_table('gamecategory',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('game_id', sa.Integer(), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['category.id'], ),
    sa.ForeignKeyConstraint(['game_id'], ['game.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_gamecategory_id'), 'gamecategory', ['id'], unique=False)
    op.create_table('gamesource',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('game_id', sa.Integer(), nullable=True),
    sa.Column('source_id', sa.Integer(), nullable=True),
    sa.Column('app_id', sa.String(), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['game_id'], ['game.id'], ),
    sa.ForeignKeyConstraint(['source_id'], ['source.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_gamesource_app_id'), 'gamesource', ['app_id'], unique=True)
    op.create_index(op.f('ix_gamesource_id'), 'gamesource', ['id'], unique=False)
    op.create_table('reviewer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('source_id', sa.Integer(), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('num_reviews', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['source_id'], ['source.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_reviewer_id'), 'reviewer', ['id'], unique=False)
    op.create_table('review',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('source_review_id', sa.Integer(), nullable=True),
    sa.Column('game_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('source_id', sa.Integer(), nullable=True),
    sa.Column('language', sa.String(), nullable=True),
    sa.Column('text', sa.TEXT(), nullable=True),
    sa.Column('summary', sa.TEXT(), nullable=True),
    sa.Column('score', sa.String(), nullable=True),
    sa.Column('helpful_score', sa.String(), nullable=True),
    sa.Column('good', sa.TEXT(), nullable=True),
    sa.Column('bad', sa.TEXT(), nullable=True),
    sa.Column('voted_up', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('processed_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('apect_sum_polarity', sa.String(), nullable=True),
    sa.Column('playtime_forever', sa.Integer(), nullable=True),
    sa.Column('playtime_last_two_weeks', sa.Integer(), nullable=True),
    sa.Column('playtime_at_review', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['game_id'], ['game.id'], ),
    sa.ForeignKeyConstraint(['source_id'], ['source.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['reviewer.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_review_id'), 'review', ['id'], unique=False)
    op.create_table('aspect',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('review_id', sa.Integer(), nullable=True),
    sa.Column('term', sa.String(), nullable=True),
    sa.Column('category', sa.String(), nullable=True),
    sa.Column('polarity', sa.String(), nullable=True),
    sa.Column('confidence', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['review_id'], ['review.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_aspect_id'), 'aspect', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_aspect_id'), table_name='aspect')
    op.drop_table('aspect')
    op.drop_index(op.f('ix_review_id'), table_name='review')
    op.drop_table('review')
    op.drop_index(op.f('ix_reviewer_id'), table_name='reviewer')
    op.drop_table('reviewer')
    op.drop_index(op.f('ix_gamesource_id'), table_name='gamesource')
    op.drop_index(op.f('ix_gamesource_app_id'), table_name='gamesource')
    op.drop_table('gamesource')
    op.drop_index(op.f('ix_gamecategory_id'), table_name='gamecategory')
    op.drop_table('gamecategory')
    op.drop_index(op.f('ix_source_url'), table_name='source')
    op.drop_index(op.f('ix_source_id'), table_name='source')
    op.drop_table('source')
    op.drop_index(op.f('ix_game_name'), table_name='game')
    op.drop_index(op.f('ix_game_id'), table_name='game')
    op.drop_table('game')
    op.drop_index(op.f('ix_category_name'), table_name='category')
    op.drop_index(op.f('ix_category_id'), table_name='category')
    op.drop_table('category')
    # ### end Alembic commands ###
