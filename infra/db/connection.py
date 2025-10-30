from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session

from app.domain.models import SQLModel
from app.settings import settings

default_engine = create_engine(url=settings.database_url, echo=True)
DefaultSession = sessionmaker(
    autocommit=False, autoflush=False, bind=default_engine, class_=Session
)


def create_tables():
    SQLModel.metadata.create_all(default_engine)


def get_managed_db_session() -> Generator[Session]:
    """
    Creates a new database session for each request.
    Automatically closes after the request completes.
    """
    session = DefaultSession()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
