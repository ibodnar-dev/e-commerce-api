# E-Commerce API - Architecture

## Architectural Style

This project follows **Hexagonal Architecture** (Ports & Adapters) combined with **Domain-Driven Design** principles.

## Directory Structure

### Core (Application/Domain)

```
domain/
  ports/
    repositories/
      product_repository.py    # Repository interfaces (output ports)
      # ... other repository interfaces
    # Future: services/, use_cases/ (input ports)
```

**Purpose**: Contains the application core, business logic, and interface definitions (ports).

**Key Principles**:
- Defines contracts/interfaces that the application needs
- No dependencies on external libraries or frameworks
- Stable and rarely changes
- Infrastructure depends on this, not vice versa

### Infrastructure (Adapters)

```
infra/
  adapters/
    repositories/
      sql_product_repository.py  # Implements domain.ports.repositories.ProductRepository
      # ... other repository implementations
    # Future: api_clients/, messaging/, etc.
```

**Purpose**: Contains concrete implementations of ports and external system integrations.

**Key Principles**:
- Implements interfaces defined in `domain/ports/`
- Depends on domain (dependency inversion)
- Can be swapped without affecting domain logic
- Contains framework-specific and technology-specific code

## Dependency Direction

```
Domain/Ports (interfaces) ←── Infrastructure/Adapters (implementations)
         ↑
         │
    Application uses ports
```

**Critical Rule**: Dependencies point INWARD toward the domain. The domain never imports from infrastructure.

## Repository Pattern

**Interface Location**: `domain/ports/repositories/`
- Defines the contract for data access
- Uses domain entities
- Abstract base classes or Protocols

**Implementation Location**: `infra/adapters/repositories/`
- Concrete implementations (SQL, NoSQL, etc.)
- Implements port interfaces
- Handles persistence details

### Example

```python
# domain/ports/repositories/product.py
from abc import ABC, abstractmethod
from domain.models.product import Product

class ProductRepository(ABC):
    @abstractmethod
    async def find_by_id(self, product_id: str) -> Product | None:
        pass

    @abstractmethod
    async def save(self, product: Product) -> None:
        pass

# infra/adapters/repositories/sql_product_repository.py
from domain.ports.repositories.product_repository import ProductRepository
from domain.models.product import Product

class SQLProductRepository(ProductRepository):
    async def find_by_id(self, product_id: str) -> Product | None:
        # SQLAlchemy implementation
        pass

    async def save(self, product: Product) -> None:
        # SQLAlchemy implementation
        pass
```

## Benefits

1. **Testability**: Mock ports easily without touching adapters
2. **Flexibility**: Swap database, external APIs, or messaging systems without changing domain
3. **Clarity**: Clear separation between business logic and technical details
4. **Maintainability**: Changes to infrastructure don't ripple into domain
