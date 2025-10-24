from datetime import UTC, datetime
from uuid import UUID

from sqlmodel import Session

from app.domain.models import Product
from app.domain.ports.repositories import ProductRepository


class SQLProductRepository(ProductRepository):
    def __init__(self, session: Session):
        self.session = session

    def find_by_id(self, product_id: str) -> Product | None:
        product_uuid = UUID(product_id)
        return self.session.get(Product, product_uuid)

    def save(self, product: Product) -> None:
        product.updated_at = datetime.now(UTC)
        self.session.add(product)
        self.session.flush()


def get_product_repository(session: Session) -> ProductRepository:
    return SQLProductRepository(session)
