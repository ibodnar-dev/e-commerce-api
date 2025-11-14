from abc import ABC, abstractmethod


class CounterRepository(ABC):
    """
    Repository for generating sequential counter values.
    """

    @abstractmethod
    def get_next_sku_value(self) -> int:
        """
        Get the next sequential value for SKU generation.
        This operation is atomic and thread-safe.

        Returns:
            int: The next sequential value
        """
        pass
