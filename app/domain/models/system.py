from enum import Enum

from sqlalchemy import BigInteger, Column
from sqlmodel import Field, SQLModel


class CounterName(Enum):
    PRODUCT_SKU_NUMBER = "product_sku_number"


class Counters(SQLModel, table=True):
    __tablename__ = "counters"

    name: CounterName = Field(primary_key=True, max_length=50)
    current_value: int = Field(default=0, sa_column=Column(BigInteger))
