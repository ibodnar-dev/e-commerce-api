from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session, select

from app.domain.models.system import Counter, CounterName
from app.domain.ports.repositories import CounterRepository
from infra.adapters.logging import get_logger
from infra.adapters.repositories.exceptions import DatabaseException

logger = get_logger(__name__)


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

    def find_by_name_for_update(self, name: CounterName) -> Counter | None:
        try:
            statement = select(Counter).where(Counter.name == name).with_for_update()
            return self.session.exec(statement).first()
        except SQLAlchemyError as e:
            logger.exception(
                f"Failed to find counter with name '{name.value}' for update",
                extra={"counter_name": name.value},
            )
            raise DatabaseException(
                f"Failed to find counter with name '{name.value}' for update"
            ) from e

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


def get_counter_repository(session: Session) -> CounterRepository:
    return SQLCounterRepository(session)
