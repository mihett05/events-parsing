"""Add super user

Revision ID: 5be9adf87828
Revises: 8a2794772c38
Create Date: 2025-05-08 16:45:32.438150

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "5be9adf87828"
down_revision: Union[str, None] = "8a2794772c38"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("ALTER TABLE organizations ALTER COLUMN owner_id SET DEFAULT 0")
    op.execute(
        "INSERT INTO users (id, email, is_active, salt, hashed_password, fullname) "
        "VALUES (0, 'admin@admin.com', true, 'xktpxZ4o+4YtOvlMX6lo5P05biLfDZp7pPMezpt7vSA=', '$2b$12$vlYjXXy.QJi7PoSPzESOVOBSZfaTqRPMMcLybCC04mqtCkWh42PDy', 'admin')"
    )
    op.execute(
        "INSERT INTO organizations (id, owner_id, title) VALUES (0, 0, 'SUPER ORG')"
    )
    op.execute("INSERT INTO user_organization_role VALUES (0, 0, 'SUPER_USER')")


def downgrade() -> None:
    op.execute(
        "DELETE FROM user_organization_role WHERE user_id=0 AND organization_id=0"
    )
    op.execute("DELETE FROM organizations WHERE id=0")
    op.execute("DELETE FROM users WHERE id=0")
