from app.domain.models import ProductType


def test_create_product(test_client):
    response = test_client.post(
        "/api/v1/products",
        json={"product_type": ProductType.SIMPLE.value, "name": "Test", "price": 10.0},
    )
    assert response.status_code == 201
