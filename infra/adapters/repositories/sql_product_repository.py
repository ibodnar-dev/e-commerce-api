from datetime import datetime, timezone
from uuid import UUID

from fastapi.params import Depends
from sqlmodel import Session

from app.domain.ports.repositories import ProductRepository
from app.domain.models import Product
from infra.db import get_db_session_generator


class SQLProductRepository(ProductRepository):
    def __init__(self, session: Session):
        self.session = session

    async def find_by_id(self, product_id: str) -> Product | None:
        product_uuid = UUID(product_id)
        return self.session.get(Product, product_uuid)

    async def save(self, product: Product) -> None:
        product.updated_at = datetime.now(timezone.utc)
        self.session.add(product)
        self.session.flush()


def get_product_repository(session: Session = Depends(get_db_session_generator)) -> ProductRepository:
    return SQLProductRepository(session)
