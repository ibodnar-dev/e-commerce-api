from app.domain.models.system import CounterName
from app.domain.ports.repositories import CounterRepository
from app.domain.services.exceptions import CounterNotInitializedError


def generate_sku(counter_repository: CounterRepository) -> str:
    prefix = "SKU"
    counter = counter_repository.find_by_name_for_update(CounterName.PRODUCT_SKU_COUNTER)
    if counter is None:
        raise CounterNotInitializedError("Product SKU counter is not initialized")
    counter.current_value = counter.current_value + 1
    counter_repository.save(counter)
    return f"{prefix}-{counter.current_value:06d}"


def generate_slug(name: str) -> str:
    lower_hyphenated = name.lower().replace(" ", "-")
    return "".join(char for char in lower_hyphenated if char.isalnum() or char == "-")
