from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field

from app.domain.models import ProductStatus, ProductType


class ProductCreateRequest(BaseModel):
    """
    Request schema for creating a new product.
    """

    product_type: ProductType = Field(..., description="Type of product (SIMPLE or VARIABLE)")
    name: str = Field(..., min_length=1, max_length=255, description="Product name")
    price: Decimal = Field(..., gt=0, decimal_places=2, description="Product price")
    slug: str | None = Field(
        None, max_length=255, description="URL-friendly slug (auto-generated if not provided)"
    )
    description: str | None = Field(None, description="Product description")
    status: ProductStatus = Field(default=ProductStatus.ACTIVE, description="Product status")


class ProductResponse(BaseModel):
    """
    Response schema for product data.
    """

    model_config = {"from_attributes": True}
    id: UUID
    type: ProductType
    name: str
    slug: str
    description: str | None
    price: Decimal
    sku: str | None
    status: ProductStatus
    created_at: datetime
    updated_at: datetime
