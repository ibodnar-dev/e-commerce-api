from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session

from app.domain.ports.repositories import CounterRepository
from app.external.adapters.logging import get_logger
from app.external.adapters.repositories.exceptions import DatabaseException
from app.external.db.sequences import product_sku_sequence

logger = get_logger(__name__)


class SQLCounterRepository(CounterRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_next_sku_value(self) -> int:
        """
        Get next SKU value from PostgreSQL sequence.
        This operation is atomic and requires no locking.

        Returns:
            int: The next sequential value for SKU generation

        Raises:
            DatabaseException: If the sequence operation fails
        """
        try:
            return self.session.exec(product_sku_sequence)
        except SQLAlchemyError as e:
            logger.exception("Failed to get next SKU value from sequence")
            raise DatabaseException("Failed to generate SKU value") from e


def get_counter_repository(session: Session) -> CounterRepository:
    return SQLCounterRepository(session)
