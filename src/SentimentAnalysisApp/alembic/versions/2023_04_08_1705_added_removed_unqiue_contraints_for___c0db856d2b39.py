"""added removed unqiue contraints for aspect

Revision ID: c0db856d2b39
Revises: 8818d4711d6f
Create Date: 2023-04-08 17:05:33.396744

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c0db856d2b39'
down_revision = '8818d4711d6f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('aspect_review_id_model_id_key', 'aspect', type_='unique')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('aspect_review_id_model_id_key', 'aspect', ['review_id', 'model_id'])
    # ### end Alembic commands ###
