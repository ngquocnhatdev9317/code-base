"""create users table

Revision ID: 1e42464a66e4
Revises:
Create Date: 2024-09-09 09:46:01.663625

"""
from datetime import datetime
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "1e42464a66e4"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column(sa.Integer, name="id", primary_key=True, autoincrement=True),
        sa.Column(sa.String(30), name="name", unique=True),
        sa.Column(sa.String(50), name="email", unique=True),
        sa.Column(sa.String(200), name="password"),
        sa.Column(sa.Boolean, name="is_superuser", default=False),
        sa.Column(sa.DateTime, name="created_at", default=datetime.now),
        sa.Column(sa.DateTime, name="updated_at", default=datetime.now, onupdate=datetime.now),
    )
    op.create_unique_constraint("UQ_users_name_email", "users", ["name", "email"])


def downgrade() -> None:
    op.drop_constraint("UQ_users_name_email", "users")
    op.drop_table("users")
