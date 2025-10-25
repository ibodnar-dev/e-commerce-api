from abc import ABC, abstractmethod

from app.domain.models.product import Product


class ProductRepository(ABC):
    @abstractmethod
    def find_by_id(self, product_id: str) -> Product | None:
        pass

    @abstractmethod
    def save(self, product: Product) -> Product:
        pass
