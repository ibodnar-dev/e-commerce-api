from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from app.domain.ports.repositories import CounterRepository, ProductRepository
from infra.adapters.repositories.sql_product_repository import (
    get_counter_repository,
    get_product_repository,
)
from infra.db.connection import get_db_session_generator


def get_product_repository_dependency(
    session: Annotated[Session, Depends(get_db_session_generator)],
) -> ProductRepository:
    return get_product_repository(session)


def get_counter_repository_dependency(
    session: Annotated[Session, Depends(get_db_session_generator)],
) -> CounterRepository:
    return get_counter_repository(session)
