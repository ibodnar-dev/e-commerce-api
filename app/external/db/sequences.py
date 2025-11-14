from sqlalchemy import Sequence

# PostgreSQL sequence for generating unique product SKUs
product_sku_sequence = Sequence(
    "product_sku_seq",
    start=1,
    increment=1,
    metadata=None,  # Will be attached to SQLModel.metadata in connection.py
)
