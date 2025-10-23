from sqlmodel import Session, select

from app.domain.models import Counter
from app.domain.models.system import CounterName


def generate_sku(session: Session) -> str:
    prefix = "SKU"
    statement = select(Counter).where(Counter.name == CounterName.PRODUCT_SKU_COUNTER).with_for_update()
    counter: Counter | None = session.exec(statement).first()
    counter.current_value = counter.current_value + 1 if counter else 1
    session.add(counter)
    session.flush()
    return f"{prefix}-{counter.current_value:06d}"
