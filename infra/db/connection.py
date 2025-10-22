from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session

from app.domain.models import SQLModel
from app.settings import settings

engine = create_engine(url=settings.database_url, echo=True)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=Session
)


def create_tables():
    SQLModel.metadata.create_all(engine)


def get_db_session():
    """
    Creates a new database session for each request.
    Automatically closes after request completes.
    """
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
