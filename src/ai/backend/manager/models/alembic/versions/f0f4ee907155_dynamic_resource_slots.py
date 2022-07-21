"""dynamic-resource-slots

Revision ID: f0f4ee907155
Revises: ff4bfca66bf8
Create Date: 2019-01-27 17:05:13.997279

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "f0f4ee907155"
down_revision = "ff4bfca66bf8"
branch_labels = None
depends_on = None


def upgrade():

    # ### commands auto generated by Alembic - please adjust! ###
    connection = op.get_bind()
    op.alter_column(
        "kernels",
        "service_ports",
        existing_type=sa.JSON(),
        type_=postgresql.JSONB(),
        postgresql_using="CAST(service_ports AS jsonb)",
    )
    op.add_column(
        "agents",
        sa.Column(
            "available_slots",
            postgresql.JSONB(),
            nullable=False,
            server_default=sa.text("'{}'::jsonb"),
        ),
    )
    op.add_column(
        "agents",
        sa.Column(
            "occupied_slots",
            postgresql.JSONB(),
            nullable=False,
            server_default=sa.text("'{}'::jsonb"),
        ),
    )
    query = """
    UPDATE agents SET available_slots = json_strip_nulls(json_build_object(
        'cpu', cpu_slots,
        'mem', mem_slots::text || 'g'
    ));
    UPDATE agents SET available_slots = available_slots || json_build_object(
        'cuda.device', gpu_slots
    )::jsonb
    WHERE gpu_slots > 0;
    UPDATE agents SET available_slots = available_slots || json_build_object(
        'tpu.device', tpu_slots
    )::jsonb
    WHERE tpu_slots > 0;

    UPDATE agents SET occupied_slots = json_strip_nulls(json_build_object(
        'cpu', used_cpu_slots,
        'mem', used_mem_slots::text || 'g'
    ));
    UPDATE agents SET occupied_slots = occupied_slots || json_build_object(
        'cuda.device', used_gpu_slots
    )::jsonb
    WHERE used_gpu_slots > 0;
    UPDATE agents SET occupied_slots = occupied_slots || json_build_object(
        'tpu.device', used_tpu_slots
    )::jsonb
    WHERE used_tpu_slots > 0;
    """
    connection.execute(query)
    op.drop_column("agents", "cpu_slots")
    op.drop_column("agents", "mem_slots")
    op.drop_column("agents", "gpu_slots")
    op.drop_column("agents", "tpu_slots")
    op.drop_column("agents", "used_cpu_slots")
    op.drop_column("agents", "used_mem_slots")
    op.drop_column("agents", "used_gpu_slots")
    op.drop_column("agents", "used_tpu_slots")

    op.add_column(
        "kernels",
        sa.Column(
            "occupied_slots",
            postgresql.JSONB(),
            nullable=False,
            server_default=sa.text("'{}'::jsonb"),
        ),
    )
    op.add_column(
        "kernels",
        sa.Column(
            "occupied_shares",
            postgresql.JSONB(),
            nullable=False,
            server_default=sa.text("'{}'::jsonb"),
        ),
    )
    query = """
    UPDATE kernels SET occupied_slots = json_build_object(
        'cpu', cpu_slot,
        'mem', mem_slot,
        'cuda.device', gpu_slot,
        'tpu.device', tpu_slot
    );
    UPDATE kernels SET occupied_shares = json_build_object(
        'cpu', cpu_set,
        'mem', mem_slot,
        'cuda.device', '{}'::json,
        'tpu.device', '{}'::json
    );
    """
    connection.execute(query)
    op.drop_column("kernels", "cpu_slot")
    op.drop_column("kernels", "mem_slot")
    op.drop_column("kernels", "gpu_slot")
    op.drop_column("kernels", "tpu_slot")
    op.drop_column("kernels", "cpu_set")
    op.drop_column("kernels", "gpu_set")
    op.drop_column("kernels", "tpu_set")
    # ### end Alembic commands ###


def downgrade():
    op.alter_column(
        "kernels",
        "service_ports",
        existing_type=postgresql.JSONB(),
        type_=sa.JSON(),
        postgresql_using="CAST(service_ports AS json)",
    )
    connection = op.get_bind()

    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "kernels",
        sa.Column("cpu_set", postgresql.ARRAY(sa.INTEGER()), autoincrement=False, nullable=True),
    )
    op.add_column(
        "kernels",
        sa.Column("gpu_set", postgresql.ARRAY(sa.INTEGER()), autoincrement=False, nullable=True),
    )
    op.add_column(
        "kernels",
        sa.Column("tpu_set", postgresql.ARRAY(sa.INTEGER()), autoincrement=False, nullable=True),
    )
    op.add_column(
        "kernels",
        sa.Column(
            "cpu_slot",
            postgresql.DOUBLE_PRECISION(precision=53),
            autoincrement=False,
            nullable=False,
            server_default="0",
        ),
    )
    op.add_column(
        "kernels",
        sa.Column("mem_slot", sa.BIGINT(), autoincrement=False, nullable=False, server_default="0"),
    )
    op.add_column(
        "kernels",
        sa.Column(
            "gpu_slot",
            postgresql.DOUBLE_PRECISION(precision=53),
            autoincrement=False,
            nullable=False,
            server_default="0",
        ),
    )
    op.add_column(
        "kernels",
        sa.Column(
            "tpu_slot",
            postgresql.DOUBLE_PRECISION(precision=53),
            autoincrement=False,
            nullable=False,
            server_default="0",
        ),
    )
    query = """
    UPDATE kernels
    SET
        cpu_set = (
            SELECT coalesce(array_agg(v::text::int), '{}')
            FROM json_array_elements((occupied_shares->>'cpu')::json) v),
        gpu_set = (
            SELECT coalesce(array_agg(v::text::int), '{}')
            FROM json_array_elements((occupied_shares->>'cuda.device')::json) v),
        tpu_set = (
            SELECT coalesce(array_agg(v::text::int), '{}')
            FROM json_array_elements((occupied_shares->>'tpu.device')::json) v)
    ;
    """
    connection.execute(query)
    query = """
    UPDATE kernels
    SET
        cpu_slot = coalesce((occupied_slots->>'cpu')::text::float, 0),
        mem_slot = coalesce((occupied_slots->>'mem')::text::bigint, 0),
        gpu_slot = coalesce((occupied_slots->>'cuda.device')::text::float, 0),
        tpu_slot = coalesce((occupied_slots->>'tpu.device')::text::float, 0)
    ;
    """
    connection.execute(query)
    op.drop_column("kernels", "occupied_shares")
    op.drop_column("kernels", "occupied_slots")

    op.add_column(
        "agents",
        sa.Column(
            "gpu_slots",
            postgresql.DOUBLE_PRECISION(precision=53),
            autoincrement=False,
            nullable=False,
            server_default="0",
        ),
    )
    op.add_column(
        "agents",
        sa.Column(
            "used_cpu_slots",
            postgresql.DOUBLE_PRECISION(precision=53),
            autoincrement=False,
            nullable=False,
            server_default="0",
        ),
    )
    op.add_column(
        "agents",
        sa.Column(
            "tpu_slots",
            postgresql.DOUBLE_PRECISION(precision=53),
            autoincrement=False,
            nullable=False,
            server_default="0",
        ),
    )
    op.add_column(
        "agents",
        sa.Column(
            "used_mem_slots", sa.BIGINT(), autoincrement=False, nullable=False, server_default="0"
        ),
    )
    op.add_column(
        "agents",
        sa.Column(
            "cpu_slots",
            postgresql.DOUBLE_PRECISION(precision=53),
            autoincrement=False,
            nullable=False,
            server_default="0",
        ),
    )
    op.add_column(
        "agents",
        sa.Column(
            "used_gpu_slots",
            postgresql.DOUBLE_PRECISION(precision=53),
            autoincrement=False,
            nullable=False,
            server_default="0",
        ),
    )
    op.add_column(
        "agents",
        sa.Column(
            "mem_slots", sa.BIGINT(), autoincrement=False, nullable=False, server_default="0"
        ),
    )
    op.add_column(
        "agents",
        sa.Column(
            "used_tpu_slots",
            postgresql.DOUBLE_PRECISION(precision=53),
            autoincrement=False,
            nullable=False,
            server_default="0",
        ),
    )
    query = """
    UPDATE agents
    SET
        cpu_slots = coalesce((available_slots->>'cpu')::text::float, 0),
        mem_slots = coalesce((available_slots->>'mem')::text::bigint, 0),
        gpu_slots = coalesce((available_slots->>'cuda.device')::text::float, 0),
        tpu_slots = coalesce((available_slots->>'tpu.device')::text::float, 0)
    ;
    """
    connection.execute(query)
    query = """
    UPDATE agents
    SET
        used_cpu_slots = coalesce((occupied_slots->>'cpu')::text::float, 0),
        used_mem_slots = coalesce((occupied_slots->>'mem')::text::bigint, 0),
        used_gpu_slots = coalesce((occupied_slots->>'cuda.device')::text::float, 0),
        used_tpu_slots = coalesce((occupied_slots->>'tpu.device')::text::float, 0)
    ;
    """
    connection.execute(query)
    op.drop_column("agents", "occupied_slots")
    op.drop_column("agents", "available_slots")
    # ### end Alembic commands ###
