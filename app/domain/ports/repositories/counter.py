from abc import ABC, abstractmethod

from app.domain.models.system import Counter, CounterName


class CounterRepository(ABC):
    @abstractmethod
    def find_by_name(self, name: CounterName) -> Counter | None:
        pass

    @abstractmethod
    def save(self, counter: Counter) -> Counter:
        pass

    @abstractmethod
    def delete(self, counter: Counter) -> None:
        pass
