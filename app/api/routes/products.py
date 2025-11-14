from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import (
    get_counter_repository_dependency,
    get_product_repository_dependency,
)
from app.api.schemas import ProductCreateRequest, ProductResponse
from app.domain.ports.repositories import CounterRepository, ProductRepository
from app.domain.services.product.main import create_product
from app.external.adapters.repositories.exceptions import DatabaseException

router = APIRouter(prefix="/products", tags=["products"])


@router.post(
    "",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new product",
)
def create_product_endpoint(
    request: ProductCreateRequest,
    product_repository: Annotated[ProductRepository, Depends(get_product_repository_dependency)],
    counter_repository: Annotated[CounterRepository, Depends(get_counter_repository_dependency)],
) -> ProductResponse:
    """
    Create a new product.

    - **product_type**: Type of product (SIMPLE or VARIABLE)
    - **name**: Product name
    - **price**: Product price (must be greater than 0)
    - **slug**: URL-friendly slug (auto-generated if not provided)
    - **description**: Optional product description
    - **status**: Product status (defaults to ACTIVE)
    """
    try:
        product = create_product(
            product_repository=product_repository,
            counter_repository=counter_repository,
            product_type=request.product_type,
            name=request.name,
            price=request.price,
            slug=request.slug,
            description=request.description,
            status=request.status,
        )
        return ProductResponse.model_validate(product)
    except DatabaseException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        ) from e
