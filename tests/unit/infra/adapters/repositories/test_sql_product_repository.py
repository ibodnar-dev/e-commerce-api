from infra.adapters.repositories.sql_product_repository import (
    SQLProductRepository,
    get_product_repository,
)


def test_get_product_repository(mock_session):
    repository = get_product_repository(session=mock_session)

    assert isinstance(repository, SQLProductRepository)
    assert repository.session is mock_session
