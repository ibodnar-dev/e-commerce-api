from datetime import datetime, timezone
from decimal import Decimal
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel


class ProductType(str, Enum):
    """Product type enumeration."""

    SIMPLE = "SIMPLE"
    VARIABLE = "VARIABLE"


class ProductStatus(str, Enum):
    """Product status enumeration."""

    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    ARCHIVED = "ARCHIVED"


class Product(SQLModel, table=True):
    """
    Main product table. Contains all products regardless of whether they have variants.

    - SIMPLE products: Single SKU, no variants (e.g., a book)
    - VARIABLE products: Multiple variants with different options (e.g., t-shirt with sizes/colors)
    """

    __tablename__ = "products"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    type: ProductType = Field(nullable=False)
    name: str = Field(max_length=255, nullable=False)
    slug: str = Field(max_length=255, unique=True, nullable=False, index=True)
    description: str | None = Field(default=None)
    price: Decimal = Field(decimal_places=2, max_digits=10, nullable=False)
    sku: str | None = Field(default=None, max_length=100, unique=True, index=True)
    status: ProductStatus = Field(default=ProductStatus.DRAFT, nullable=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    variants: list["ProductVariant"] = Relationship(back_populates="product")
    inventory: Optional["Inventory"] = Relationship(back_populates="product")


class VariantAttributeValue(SQLModel, table=True):
    """
    Junction table linking variants to their attribute values.
    Example: A "Black T-Shirt in Medium" variant would have two entries linking to Black and Medium.
    """

    __tablename__ = "variant_attribute_values"

    variant_id: UUID = Field(foreign_key="product_variants.id", primary_key=True, nullable=False)
    attribute_value_id: UUID = Field(
        foreign_key="attribute_values.id", primary_key=True, nullable=False
    )


class ProductVariant(SQLModel, table=True):
    """
    Child products that represent specific configurations.
    Only exists for VARIABLE products (e.g., "T-Shirt - Black - Medium").
    """

    __tablename__ = "product_variants"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    product_id: UUID = Field(foreign_key="products.id", nullable=False, index=True)
    sku: str = Field(max_length=100, unique=True, nullable=False, index=True)
    name: str | None = Field(default=None, max_length=255)
    price: Decimal | None = Field(default=None, decimal_places=2, max_digits=10)
    is_active: bool = Field(default=True, nullable=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    product: Product = Relationship(back_populates="variants")
    inventory: Optional["Inventory"] = Relationship(back_populates="variant")
    attribute_values: list["AttributeValue"] = Relationship(
        back_populates="variants", link_model=VariantAttributeValue
    )


class Attribute(SQLModel, table=True):
    """
    Defines what options are available (e.g., "Color", "Size").
    """

    __tablename__ = "attributes"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(max_length=50, nullable=False)
    slug: str = Field(max_length=50, nullable=False, unique=True, index=True)

    # Relationships
    values: list["AttributeValue"] = Relationship(back_populates="attribute")


class AttributeValue(SQLModel, table=True):
    """
    Defines the actual values for each attribute (e.g., "Red", "Small").
    """

    __tablename__ = "attribute_values"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    attribute_id: UUID = Field(foreign_key="attributes.id", nullable=False, index=True)
    value: str = Field(max_length=100, nullable=False)
    slug: str = Field(max_length=100, nullable=False, index=True)

    # Relationships
    attribute: Attribute = Relationship(back_populates="values")
    variants: list[ProductVariant] = Relationship(
        back_populates="attribute_values", link_model=VariantAttributeValue
    )


class Inventory(SQLModel, table=True):
    """
    Tracks stock levels for products or variants.

    - For SIMPLE products: product_id is set, variant_id is NULL
    - For VARIABLE products: product_id is NULL, variant_id is set
    """

    __tablename__ = "inventory"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    product_id: UUID | None = Field(
        default=None, foreign_key="products.id", nullable=True, index=True
    )
    variant_id: UUID | None = Field(
        default=None, foreign_key="product_variants.id", nullable=True, index=True
    )
    quantity_available: int = Field(default=0, nullable=False)
    quantity_reserved: int = Field(default=0, nullable=False)
    low_stock_threshold: int = Field(default=10, nullable=False)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    product: Product | None = Relationship(back_populates="inventory")
    variant: ProductVariant | None = Relationship(back_populates="inventory")
