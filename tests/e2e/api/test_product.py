from app.domain.models import ProductType


def test_create_product(create_product_counter, test_client):  # noqa: ARG001
    response = test_client.post(
        "/api/v1/products",
        json={"product_type": ProductType.SIMPLE.value, "name": "Test", "price": 10.0},
    )
    assert response.status_code == 201
