"""empty message

Revision ID: 898bcdb02c37
Revises:
Create Date: 2024-11-20 17:09:29.163363

"""

from typing import Sequence, Union

import sqlalchemy_utils
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "898bcdb02c37"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "structure",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("path", sqlalchemy_utils.types.ltree.LtreeType(), nullable=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("company_id", sa.UUID(), nullable=True),
        sa.ForeignKeyConstraint(
            ["company_id"],
            ["company.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_position_path", "structure", ["path"], unique=False, postgresql_using="gist"
    )
    op.drop_index("ix_positions_path", table_name="position", postgresql_using="gist")
    op.drop_table("position")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "position",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("name", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column(
            "path",
            sqlalchemy_utils.types.ltree.LtreeType(),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column("company_id", sa.UUID(), autoincrement=False, nullable=True),
        sa.ForeignKeyConstraint(
            ["company_id"], ["company.id"], name="position_company_id_fkey"
        ),
        sa.PrimaryKeyConstraint("id", name="position_pkey"),
    )
    op.create_index(
        "ix_positions_path", "position", ["path"], unique=False, postgresql_using="gist"
    )
    op.drop_index("ix_position_path", table_name="structure", postgresql_using="gist")
    op.drop_table("structure")
    # ### end Alembic commands ###