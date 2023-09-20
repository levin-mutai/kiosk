import pytest
from products.factory import ProductFactory


# @pytest.mark.django_db
# def test_create_product(tokenized_client, product_factory):
#     product = product_factory()
#     assert product.name == "test_product"
#     assert product.price == 10
#     assert product.description == "test_description"
#     assert product.quantity == 10
#     assert product.category.name == "test_category"


def test_create_product_api(tokenized_client, product_factory):
    product = product_factory
    response = tokenized_client.post(
        "/api/products",
        {
            "name": product.name,
            "price": product.price,
            "stock": product.stock,
            "description": "A very quality bluetooth speaker to work with.",
            "image_url": product.image_url,
        },
    )
    assert response.status_code == 201
    assert response.data["name"] == product.name
    assert response.data["price"] == product.price
    assert response.data["stock"] == product.stock
    assert (
        response.data["description"] == "A very quality bluetooth speaker to work with."
    )
    assert response.data["image_url"] == product.image_url


def test_list_products_api(tokenized_client, product_factory):
    product = product_factory
    tokenized_client.post(
        "/api/products",
        {
            "name": product.name,
            "price": product.price,
            "stock": product.stock,
            "description": "A very quality bluetooth speaker to work with.",
            "image_url": product.image_url,
        },
    )
    tokenized_client.post(
        "/api/products",
        {
            "name": "JBL Speaker",
            "price": 4000,
            "stock": 21,
            "description": "A very quality bluetooth speaker to work with.",
            "image_url": "",
        },
    )
    response = tokenized_client.get("/api/products")
    assert response.status_code == 200
    assert len(response.data) == 2
