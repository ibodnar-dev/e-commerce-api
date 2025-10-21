from infra.adapters.repositories.sql_product_repository import (
    get_product_repository,
    SQLProductRepository,
)


def test_get_product_repository(mock_session):
    repository = get_product_repository(session=mock_session)

    assert isinstance(repository, SQLProductRepository)
    assert repository.session is mock_session
