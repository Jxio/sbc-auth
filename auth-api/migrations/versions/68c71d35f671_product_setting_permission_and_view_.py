"""product setting permission and view changes

Revision ID: 68c71d35f671
Revises: 19a7733fd001
Create Date: 2021-04-06 08:01:35.445983

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy import text
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql import column, table

from auth_api.utils.custom_sql import CustomSql


# revision identifiers, used by Alembic.
revision = "68c71d35f671"
down_revision = "19a7733fd001"
branch_labels = None
depends_on = None


authorizations_view = CustomSql(
    "authorizations_view",
    " SELECT e.business_identifier,"
    "e.name AS entity_name,"
    "e.folio_number,"
    "e.corp_type_code,"
    "m.membership_type_code AS org_membership,"
    "u.keycloak_guid,"
    "u.id AS user_id,"
    "o.id AS org_id,"
    "o.name AS org_name,"
    "o.status_code,"
    "o.type_code AS org_type,"
    "ps.product_code,"
    "o.bcol_user_id,"
    "o.bcol_account_id"
    " FROM memberships m "
    "LEFT JOIN orgs o ON m.org_id = o.id "
    "LEFT JOIN users u ON u.id = m.user_id "
    "LEFT JOIN affiliations a ON o.id = a.org_id "
    "LEFT JOIN entities e ON e.id = a.entity_id "
    "LEFT JOIN product_subscriptions ps ON ps.org_id = o.id AND ps.status_code = "
    "'ACTIVE' "
    "WHERE m.status = 1;",
)


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    permissions_table = table(
        "permissions",
        column("id", sa.Integer()),
        column("membership_type_code", sa.String(length=15)),
        column("org_status_code", sa.String(length=25)),
        column("actions", sa.String(length=100)),
    )

    conn = op.get_bind()
    res = conn.execute(text(f"select max(id) from permissions;"))
    latest_id = res.fetchall()[0][0]

    # Insert code values
    op.bulk_insert(
        permissions_table,
        [
            {
                "id": latest_id + 1,
                "membership_type_code": "ADMIN",
                "org_status_code": None,
                "actions": "request_product_package",
            },
            {
                "id": latest_id + 2,
                "membership_type_code": "COORDINATOR",
                "org_status_code": None,
                "actions": "request_product_package",
            },
        ],
    )

    op.execute(f"DROP VIEW IF EXISTS {authorizations_view.name}")
    op.execute(f"CREATE VIEW {authorizations_view.name} AS {authorizations_view.sql}")

    # ### end Alembic commands ###


def downgrade():
    op.execute('delete from permissions where action="request_product_package"')
    # ### end Alembic commands ###
