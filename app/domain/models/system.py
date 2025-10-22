from sqlalchemy import BigInteger, Column
from sqlmodel import Field, SQLModel


class Counter(SQLModel, table=True):
    __tablename__ = "counter"

    name: str = Field(primary_key=True, max_length=50)
    current_value: int = Field(default=0, sa_column=Column(BigInteger))
