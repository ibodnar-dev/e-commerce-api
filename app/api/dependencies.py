from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from app.domain.ports.repositories import CounterRepository, ProductRepository
from app.external.adapters.repositories import get_counter_repository, get_product_repository
from app.external.db import get_managed_db_session


def get_product_repository_dependency(
    session: Annotated[Session, Depends(get_managed_db_session)],
) -> ProductRepository:
    return get_product_repository(session)


def get_counter_repository_dependency(
    session: Annotated[Session, Depends(get_managed_db_session)],
) -> CounterRepository:
    return get_counter_repository(session)
