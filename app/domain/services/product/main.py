from decimal import Decimal

from sqlmodel import Session

from app.domain.models import Product, ProductType, ProductStatus
from app.domain.services.product.utils import generate_sku, generate_slug


def create_product(
    session: Session,
    product_type: ProductType,
    name: str,
    price: Decimal,
    slug: str | None = None,
    description: str | None = None,
    status: ProductStatus = ProductStatus.ACTIVE,
) -> Product:
    product = Product(
        product_type=product_type,
        name=name,
        price=price,
        slug=slug or generate_slug(name),
        description=description,
        sku=generate_sku(session),
        status=status,
    )
    session.add(product)
    session.flush()
    return product
