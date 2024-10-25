"""Initial migration.

Revision ID: ffd0e83f3c4c
Revises: 
Create Date: 2022-05-31 19:48:45.442620

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "ffd0e83f3c4c"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # ### end Alembic commands ###
    op.execute(
        'ALTER TABLE "geopaysages"."conf" ADD CONSTRAINT pk_conf PRIMARY KEY ("key")'
    )


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # ### end Alembic commands ###
    op.execute('ALTER TABLE "geopaysages"."conf" DROP CONSTRAINT pk_conf')
