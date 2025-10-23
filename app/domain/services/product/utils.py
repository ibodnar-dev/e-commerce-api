from sqlmodel import Session, select

from app.domain.models import Counter
from app.domain.models.system import CounterName
from app.domain.services.exceptions import CounterNotInitializedError


def generate_sku(session: Session) -> str:
    prefix = "SKU"
    statement = select(Counter).where(Counter.name == CounterName.PRODUCT_SKU_COUNTER).with_for_update()
    counter: Counter | None = session.exec(statement).first()
    if counter is None:
        raise CounterNotInitializedError("Product SKU counter is not initialized")
    counter.current_value = counter.current_value + 1 if counter else 1
    session.add(counter)
    session.flush()
    return f"{prefix}-{counter.current_value:06d}"


def generate_slug(name: str) -> str:
    lower_hyphenated = name.lower().replace(" ", "-")
    return "".join(char for char in lower_hyphenated if char.isalnum() or char == "-")
