from decimal import Decimal

from app.domain.models import Product, ProductStatus, ProductType
from app.domain.ports.repositories import CounterRepository, ProductRepository
from app.domain.services.product.utils import generate_sku, generate_slug


def create_product(
    product_repository: ProductRepository,
    counter_repository: CounterRepository,
    product_type: ProductType,
    name: str,
    price: Decimal,
    slug: str | None = None,
    description: str | None = None,
    status: ProductStatus = ProductStatus.ACTIVE,
) -> Product:
    product = Product(
        type=product_type.value,
        name=name,
        price=price,
        slug=slug or generate_slug(name),
        description=description,
        sku=generate_sku(counter_repository),
        status=status,
    )
    return product_repository.save(product)
