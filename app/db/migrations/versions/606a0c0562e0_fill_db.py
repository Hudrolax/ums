"""fill db

Revision ID: 606a0c0562e0
Revises: 37a3559f33c9
Create Date: 2023-06-10 09:01:52.220597

"""
from alembic import op
import os


# revision identifiers, used by Alembic.
revision = '606a0c0562e0'
down_revision = '37a3559f33c9'
branch_labels = None
depends_on ='37a3559f33c9' 

fill_db_path = os.path.join(os.path.dirname(__file__), "../../queries/fill_db.sql")
create_tables_sql_path = os.path.join(os.path.dirname(__file__), "../../queries/create_tables.sql")
drop_tables_sql_path = os.path.join(os.path.dirname(__file__), "../../queries/drop_all_tables.sql")

def upgrade() -> None:
    with open(fill_db_path) as file:
        sql = file.read()
    op.execute(sql)


def downgrade() -> None:
    with open(drop_tables_sql_path) as file:
        sql = file.read()
    op.execute(sql)
    with open(create_tables_sql_path) as file:
        sql = file.read()
    op.execute(sql)
