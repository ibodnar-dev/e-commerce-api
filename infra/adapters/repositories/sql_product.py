from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session

from app.domain.models import Product
from app.domain.ports.repositories import ProductRepository
from infra.adapters.logging import get_logger
from infra.adapters.repositories.exceptions import DatabaseException

logger = get_logger(__name__)


class SQLProductRepository(ProductRepository):
    def __init__(self, session: Session):
        self.session = session

    def find_by_id(self, product_id: str) -> Product | None:
        try:
            product_uuid = UUID(product_id)
            return self.session.get(Product, product_uuid)
        except SQLAlchemyError as e:
            logger.exception(
                f"Failed to find product with id '{product_id}'",
                extra={"product_id": product_id},
            )
            raise DatabaseException(f"Failed to find product with id '{product_id}'") from e

    def save(self, product: Product) -> Product:
        try:
            product.updated_at = datetime.now(UTC)
            self.session.add(product)
            self.session.flush()
            logger.debug("Product saved successfully", extra={"product_id": str(product.id)})
            return product
        except SQLAlchemyError as e:
            logger.exception(
                "Failed to save product",
                extra={"product_id": str(product.id)},
            )
            raise DatabaseException(f"Failed to save product with id '{product.id}'") from e


def get_product_repository(session: Session) -> ProductRepository:
    return SQLProductRepository(session)
