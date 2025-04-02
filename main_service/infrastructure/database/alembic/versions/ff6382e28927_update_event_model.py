"""update event model

Revision ID: ff6382e28927
Revises: ba91cfce99d6
Create Date: 2025-04-02 10:25:54.411382

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "ff6382e28927"
down_revision: Union[str, None] = "ba91cfce99d6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "events",
        sa.Column(
            "end_registration", sa.DateTime(timezone=True), nullable=False
        ),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("events", "end_registration")
    # ### end Alembic commands ###
