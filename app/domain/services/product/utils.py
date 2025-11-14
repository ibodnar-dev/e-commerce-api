from app.domain.ports.repositories import CounterRepository


def generate_sku(counter_repository: CounterRepository) -> str:
    """
    Generate a unique SKU using PostgreSQL sequence.

    Args:
        counter_repository: Repository for generating sequential values

    Returns:
        str: A unique SKU in format "SKU-XXXXXX" (e.g., "SKU-000001")
    """
    prefix = "SKU"
    next_value = counter_repository.get_next_sku_value()
    return f"{prefix}-{next_value:06d}"


def generate_slug(name: str) -> str:
    lower_hyphenated = name.lower().replace(" ", "-")
    return "".join(char for char in lower_hyphenated if char.isalnum() or char == "-")
