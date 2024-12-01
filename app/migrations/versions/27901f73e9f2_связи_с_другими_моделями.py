"""Связи с другими моделями

Revision ID: 27901f73e9f2
Revises: ce814162b36d
Create Date: 2024-12-01 16:48:46.459226

"""
from typing import Sequence, Union

import fastapi_users_db_sqlalchemy
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '27901f73e9f2'
down_revision: Union[str, None] = 'ce814162b36d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('routereviews', sa.Column('author_id', fastapi_users_db_sqlalchemy.generics.GUID(), nullable=False))
    op.create_foreign_key(None, 'routereviews', 'user', ['author_id'], ['id'])
    op.add_column('routes', sa.Column('author_id', fastapi_users_db_sqlalchemy.generics.GUID(), nullable=False))
    op.create_foreign_key(None, 'routes', 'user', ['author_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'routes', type_='foreignkey')
    op.drop_column('routes', 'author_id')
    op.drop_constraint(None, 'routereviews', type_='foreignkey')
    op.drop_column('routereviews', 'author_id')
    # ### end Alembic commands ###
