from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session

from app.domain.models import Product
from app.domain.models.system import Counter, CounterName
from app.domain.ports.repositories import CounterRepository, ProductRepository
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


class SQLCounterRepository(CounterRepository):
    def __init__(self, session: Session):
        self.session = session

    def find_by_name(self, name: CounterName) -> Counter | None:
        try:
            return self.session.get(Counter, name)
        except SQLAlchemyError as e:
            logger.exception(
                f"Failed to find counter with name '{name.value}'",
                extra={"counter_name": name.value},
            )
            raise DatabaseException(f"Failed to find counter with name '{name.value}'") from e

    def save(self, counter: Counter) -> Counter:
        try:
            self.session.add(counter)
            self.session.flush()
            logger.debug("Counter saved successfully", extra={"counter_name": counter.name.value})
            return counter
        except SQLAlchemyError as e:
            logger.exception(
                "Failed to save counter",
                extra={"counter_name": counter.name.value},
            )
            raise DatabaseException(
                f"Failed to save counter with name '{counter.name.value}'"
            ) from e

    def delete(self, counter: Counter) -> None:
        try:
            self.session.delete(counter)
            self.session.flush()
            logger.debug("Counter deleted successfully", extra={"counter_name": counter.name.value})
        except SQLAlchemyError as e:
            logger.exception(
                "Failed to delete counter",
                extra={"counter_name": counter.name.value},
            )
            raise DatabaseException(
                f"Failed to delete counter with name '{counter.name.value}'"
            ) from e


def get_product_repository(session: Session) -> ProductRepository:
    return SQLProductRepository(session)


def get_counter_repository(session: Session) -> CounterRepository:
    return SQLCounterRepository(session)
