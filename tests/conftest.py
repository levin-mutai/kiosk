import pytest
from rest_framework.test import APIClient

from user_auth.models import User

from oauth2_provider.models import Application

from oauth2_provider.models import Application
from products.factory import ProductFactory


# ==========================================FACTORIES =============================================
@pytest.fixture
def product_factory():
    return ProductFactory()


# ================================================================================================


@pytest.fixture()
def user(db):
    User.objects.create_user("test_user", "test@gmail.com", "test")
    user = User.objects.get(username="test_user")
    return user


@pytest.fixture()
def oauth2_test_application(db):
    application = Application.objects.create(
        name="kiosk",
        client_type=Application.CLIENT_CONFIDENTIAL,
        authorization_grant_type=Application.GRANT_AUTHORIZATION_CODE,
        redirect_uris="http://localhost:8000/callback/",
    )
    return application


@pytest.fixture()
def client():
    return APIClient()


@pytest.fixture()
def tokenized_client(client, user, oauth2_test_application, db):
    print(oauth2_test_application)
    respomse = client.post(
        "/api/accounts/login", {"username": "test_user", "password": "test"}
    )
    client.credentials(HTTP_AUTHORIZATION="Bearer " + respomse.data["access_token"])

    return client


@pytest.fixture
def customer(tokenized_client, user, db):
    response = tokenized_client.post(
        "/api/customers",
        {
            "name": "test",
            "email": "customer@gmail.com",
            "phonenumber": "+254768850678",
            "user": user.id,
        },
    )
    return response.data


@pytest.fixture
def products_list_for_customer(
    tokenized_client,
    product_factory,
):
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

    return response.data
