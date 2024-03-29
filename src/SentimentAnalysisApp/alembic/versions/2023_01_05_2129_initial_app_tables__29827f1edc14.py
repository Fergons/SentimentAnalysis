"""initial app tables

Revision ID: 29827f1edc14
Revises: 57b460a916d4
Create Date: 2023-01-05 21:29:48.984238

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils

# revision identifiers, used by Alembic.
revision = '29827f1edc14'
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
    sa.Column('name_tsv', sqlalchemy_utils.types.ts_vector.TSVectorType(), sa.Computed('to_tsvector(\'english\', "name")', persisted=True), nullable=True),
    sa.Column('image_url', sa.String(), nullable=True),
    sa.Column('release_date', sa.DateTime(timezone=True), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_game_name_tsv', 'game', ['name_tsv'], unique=False, postgresql_using='gin')
    op.create_index(op.f('ix_game_id'), 'game', ['id'], unique=False)
    op.create_index(op.f('ix_game_name'), 'game', ['name'], unique=False)
    op.create_table('source',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('url', sa.String(), nullable=True),
    sa.Column('user_reviews_url', sa.String(), nullable=True),
    sa.Column('critic_reviews_url', sa.String(), nullable=True),
    sa.Column('game_detail_url', sa.String(), nullable=True),
    sa.Column('list_of_games_url', sa.String(), nullable=True),
    sa.Column('reviewer_detail_url', sa.String(), nullable=True),
    sa.Column('list_of_reviewers_url', sa.String(), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_source_id'), 'source', ['id'], unique=False)
    op.create_index(op.f('ix_source_name'), 'source', ['name'], unique=True)
    op.create_index(op.f('ix_source_url'), 'source', ['url'], unique=False)
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
    sa.Column('source_game_id', sa.String(), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['game_id'], ['game.id'], ),
    sa.ForeignKeyConstraint(['source_id'], ['source.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_gamesource_id'), 'gamesource', ['id'], unique=False)
    op.create_index(op.f('ix_gamesource_source_game_id'), 'gamesource', ['source_game_id'], unique=True)
    op.create_table('reviewer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('source_reviewer_id', sa.String(), nullable=True),
    sa.Column('source_id', sa.Integer(), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('num_games_owned', sa.Integer(), nullable=True),
    sa.Column('num_reviews', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['source_id'], ['source.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('source_reviewer_id', 'source_id')
    )
    op.create_index(op.f('ix_reviewer_id'), 'reviewer', ['id'], unique=False)
    op.create_table('review',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('source_review_id', sa.String(), nullable=True),
    sa.Column('source_reviewer_id', sa.String(), nullable=True),
    sa.Column('game_id', sa.Integer(), nullable=True),
    sa.Column('reviewer_id', sa.Integer(), nullable=True),
    sa.Column('source_id', sa.Integer(), nullable=True),
    sa.Column('language', sa.String(), nullable=True),
    sa.Column('text', sa.TEXT(), nullable=True),
    sa.Column('text_tsv', sqlalchemy_utils.types.ts_vector.TSVectorType(), sa.Computed('to_tsvector(\'english\', "text")', persisted=True), nullable=True),
    sa.Column('summary', sa.TEXT(), nullable=True),
    sa.Column('score', sa.String(), nullable=True),
    sa.Column('helpful_score', sa.String(), nullable=True),
    sa.Column('good', sa.TEXT(), nullable=True),
    sa.Column('bad', sa.TEXT(), nullable=True),
    sa.Column('voted_up', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('processed_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('aspect_sum_polarity', sa.String(), nullable=True),
    sa.Column('playtime_at_review', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['game_id'], ['game.id'], ),
    sa.ForeignKeyConstraint(['reviewer_id'], ['reviewer.id'], ),
    sa.ForeignKeyConstraint(['source_id'], ['source.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('source_review_id', 'source_id')
    )
    op.create_index('idx_review_text_tsv', 'review', ['text_tsv'], unique=False, postgresql_using='gin')
    op.create_index(op.f('ix_review_id'), 'review', ['id'], unique=False)
    op.create_table('aspect',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('review_id', sa.Integer(), nullable=True),
    sa.Column('term', sa.String(), nullable=True),
    sa.Column('category', sa.String(), nullable=True),
    sa.Column('polarity', sa.String(), nullable=True),
    sa.Column('confidence', sa.String(), nullable=True),
    sa.Column('model_id', sa.String(), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['review_id'], ['review.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_aspect_id'), 'aspect', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_aspect_id'), table_name='aspect')
    op.drop_table('aspect')
    op.drop_index(op.f('ix_review_id'), table_name='review')
    op.drop_index('idx_review_text_tsv', table_name='review', postgresql_using='gin')
    op.drop_table('review')
    op.drop_index(op.f('ix_reviewer_id'), table_name='reviewer')
    op.drop_table('reviewer')
    op.drop_index(op.f('ix_gamesource_source_game_id'), table_name='gamesource')
    op.drop_index(op.f('ix_gamesource_id'), table_name='gamesource')
    op.drop_table('gamesource')
    op.drop_index(op.f('ix_gamecategory_id'), table_name='gamecategory')
    op.drop_table('gamecategory')
    op.drop_index(op.f('ix_source_url'), table_name='source')
    op.drop_index(op.f('ix_source_name'), table_name='source')
    op.drop_index(op.f('ix_source_id'), table_name='source')
    op.drop_table('source')
    op.drop_index(op.f('ix_game_name'), table_name='game')
    op.drop_index(op.f('ix_game_id'), table_name='game')
    op.drop_index('idx_game_name_tsv', table_name='game', postgresql_using='gin')
    op.drop_table('game')
    op.drop_index(op.f('ix_category_name'), table_name='category')
    op.drop_index(op.f('ix_category_id'), table_name='category')
    op.drop_table('category')
    # ### end Alembic commands ###
