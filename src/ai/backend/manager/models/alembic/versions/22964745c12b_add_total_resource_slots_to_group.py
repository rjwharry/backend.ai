"""add_total_resource_slots_to_group

Revision ID: 22964745c12b
Revises: 02950808ca3d
Create Date: 2019-06-17 15:57:39.442741

"""
import textwrap

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "22964745c12b"
down_revision = "02950808ca3d"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("domains", sa.Column("integration_id", sa.String(length=512), nullable=True))
    op.alter_column(
        "domains",
        "total_resource_slots",
        existing_type=postgresql.JSONB(astext_type=sa.Text()),
        nullable=True,
    )
    op.add_column("groups", sa.Column("integration_id", sa.String(length=512), nullable=True))
    op.add_column(
        "groups",
        sa.Column("total_resource_slots", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    )
    op.add_column("users", sa.Column("integration_id", sa.String(length=512), nullable=True))
    # ### end Alembic commandk ###

    print("\nSet group's total_resource_slots with empty dictionary.")
    query = textwrap.dedent(
        """\
        UPDATE groups SET total_resource_slots = '{}'::jsonb;
    """
    )
    connection = op.get_bind()
    connection.execute(query)


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("users", "integration_id")
    op.drop_column("groups", "total_resource_slots")
    op.drop_column("groups", "integration_id")
    op.alter_column(
        "domains",
        "total_resource_slots",
        existing_type=postgresql.JSONB(astext_type=sa.Text()),
        nullable=False,
    )
    op.drop_column("domains", "integration_id")
    # ### end Alembic commands ###
