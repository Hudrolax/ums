"""create tables

Revision ID: 37a3559f33c9
Revises: 
Create Date: 2023-06-09 23:29:05.236459

"""
from alembic import op
import os


# revision identifiers, used by Alembic.
revision = '37a3559f33c9'
down_revision = None
branch_labels = None
depends_on = None

create_tables_sql_path = os.path.join(os.path.dirname(__file__), "../../queries/create_tables.sql")
drop_tables_sql_path = os.path.join(os.path.dirname(__file__), "../../queries/drop_all_tables.sql")



def upgrade() -> None:
    with open(create_tables_sql_path) as file:
        sql = file.read()
    op.execute(sql)


def downgrade() -> None:
    with open(drop_tables_sql_path) as file:
        sql = file.read()
    op.execute(sql)
