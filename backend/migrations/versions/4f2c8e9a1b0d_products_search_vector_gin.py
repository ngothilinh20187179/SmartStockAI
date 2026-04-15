"""Products search_vector (tsvector) + GIN index — single revision from model.

Revision ID: 4f2c8e9a1b0d
Revises: c36177fa7035
Create Date: 2026-04-15

"""

from typing import Sequence, Union

from alembic import op

revision: str = "4f2c8e9a1b0d"
down_revision: Union[str, Sequence[str], None] = "c36177fa7035"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        ALTER TABLE products
        ADD COLUMN IF NOT EXISTS search_vector tsvector
        GENERATED ALWAYS AS (
            to_tsvector(
                'simple',
                coalesce(product_name, '') || ' ' ||
                coalesce(sku_code, '') || ' ' ||
                coalesce(product_code, '') || ' ' ||
                coalesce(barcode, '')
            )
        ) STORED;
        """
    )
    op.execute(
        """
        CREATE INDEX IF NOT EXISTS ix_products_search_vector
        ON products USING GIN (search_vector);
        """
    )


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS ix_products_search_vector;")
    op.execute("ALTER TABLE products DROP COLUMN IF EXISTS search_vector;")
