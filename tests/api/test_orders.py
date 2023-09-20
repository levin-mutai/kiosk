import uuid
import pytest


@pytest.mark.skip()
def test_create_order_api(db, tokenized_client, products_list_for_customer, customer):
    customer = customer.copy()
    products = products_list_for_customer.copy()
    cust_id = customer.get("id")
    print(cust_id)
    print(products[0]["id"])
    print(products[1]["id"])
    response = tokenized_client.post(
        "/api/orders",
        {
            "customer": cust_id,
            "products": [
                {"product": products[0]["id"], "quantity": 2},
                {"product": products[1]["id"], "quantity": 1},
            ],
        },
    )

    assert response.status_code == 201
    assert response.data["message"] == "Order created successfully"
    assert "order_id" in response.data
