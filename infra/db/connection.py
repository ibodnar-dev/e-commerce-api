from sqlalchemy import create_engine

from app.domain.models import SQLModel


from app.settings import settings

engine = create_engine(url=settings.database_url, echo=True)


def create_tables():
    with engine.connect():
        SQLModel.metadata.create_all(engine)
