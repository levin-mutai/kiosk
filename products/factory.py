# products/factories.py

import factory
from .models import Product, Customer, Order, OrderProduct
from user_auth.models import User


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = "test_user"
    email = "customer@gmail.com"
    password = "test"


class CustomerFactory(factory.Factory):
    class Meta:
        model = Product

    user = factory.SubFactory(UserFactory)
    name = "test_customer"
    email = "customer@gmail.com"
    phonenumber = "0987654321"


class ProductFactory(factory.Factory):
    class Meta:
        model = Product

    name = "test_product"
    price = 100
    description = "test_description"
    stock = 10
    image_url = "https://test_image_url.com"


class OrderProductFactory(factory.Factory):
    class Meta:
        model = Product

    product = factory.SubFactory(ProductFactory)
    quantity = 1
