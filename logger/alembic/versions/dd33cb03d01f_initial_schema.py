"""initial schema

Revision ID: dd33cb03d01f
Revises:
Create Date: 20121-03-15 17:53:32.308761

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'dd33cb03d01f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "tweets",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("twitter_id", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("author_name", sa.String(), nullable=False),
        sa.Column("author_id", sa.String(), nullable=False),
        sa.Column("tweet", sa.Text(), nullable=False),
        sa.Column("retweet_count", sa.Integer()),
        sa.Column("location", sa.String()),
        sa.Column("place", sa.String()),
        sa.PrimaryKeyConstraint("id")
    )

def downgrade():
    op.drop_table("tweets")
