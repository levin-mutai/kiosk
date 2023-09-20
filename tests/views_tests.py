# import pytest
# from django.urls import reverse
# from rest_framework import status
# from rest_framework.test import APIClient


# # test for product creation
# product_0 = ""
# product_1 = ""


# def test_product_creation():
#     client = APIClient()
#     url = reverse("Products_detail-list")
#     print(url)
#     data = {
#         "name": "test Product",
#         "price": 4000,
#         "stock": 21,
#         "description": "A very quality product to work with.",
#         "image_url": "",
#     }
#     data_1 = {
#         "name": "test Product",
#         "price": 4000,
#         "stock": 21,
#         "description": "A very quality product to work with.",
#         "image_url": "",
#     }

#     try:
#         product_0 = client.post(url, data, format="json")
#         product_1 = client.post(url, data_1, format="json")
#     except:
#         print("error")

#         assert False

#     assert product_0.status_code == status.HTTP_201_CREATED
#     assert product_0.data["name"] == data["name"]
#     assert product_0.data["price"] == data["price"]
#     assert product_1.data["name"] == data["name"]
#     assert product_1.data["price"] == data["price"]


# # test for product update


# def test_product_update():
#     product_0.object.update(
#         name="updated test Product",
#         price=5000,
#         stock=21,
#         description="A very quality product to work with.",
#         image_url="",
#     )
#     assert product_0.data["name"] == "updated test Product"
#     assert product_0.data["price"] == 5000


# # test for order creation


# def test_order_creation():
#     client = APIClient()
#     url = reverse("Orders_detail-list")
#     data = {
#         "user_id": 1,
#         "products": [
#             {"product": product_1.id, "quantity": 1},
#             {"product": product_0.id, "quantity": 2},
#         ],
#     }
#     response = client.post(url, data, format="json")
#     assert response.status_code == status.HTTP_201_CREATED


# # test for order update


# def test_order_update():
#     client = APIClient()
#     url = reverse("Orders_detail-list", args=[1])
#     data = {
#         "user_id": 1,
#         "products": [
#             {"product": product_1.id, "quantity": 1},
#             {"product": product_0.id, "quantity": 2},
#         ],
#     }
#     response = client.put(url, data, format="json")
#     assert response.status_code == status.HTTP_200_OK
#     assert response.data["products"][0]["quantity"] == 1
#     assert response.data["products"][1]["quantity"] == 2
#     assert response.data["user_id"] == 1


# # test for order delete


# def test_order_delete():
#     client = APIClient()
#     url = reverse("Orders_detail-list", args=[1])
#     response = client.delete(url)


# # test for user creation


# def test_user_creation():
#     client = APIClient()
#     url = reverse("Users_list")
#     data = {
#         "username": "test_user",
#         "password": "test_password",
#         "first_name": "test_first_name",
#         "last_name": "test_last_name",
#         "email": "test@email.com",
#         "phone_number": "+254768850685",
#     }
#     response = client.post(url, data, format="json")
#     assert response.status_code == status.HTTP_201_CREATED
#     assert response.data["username"] == "test_user"
#     assert response.data["password"] == "test_password"
#     assert response.data["first_name"] == "test_first_name"
#     assert response.data["last_name"] == "test_last_name"
#     assert response.data["email"] == "test@email.com"
#     assert response.data["phone_number"] == "+254768850685"


# # test for user update
# def test_user_update():
#     client = APIClient()
#     url = reverse("Users_detail-list", args=[1])
#     data = {
#         "username": "test_user",
#         "password": "test_password",
#         "first_name": "test_first_name",
#         "last_name": "test_last_name",
#         "email": "test@email.com",
#         "phone_number": "+254768850685",
#     }
#     response = client.put(url, data, format="json")
#     assert response.status_code == status.HTTP_200_OK
#     assert response.data["username"] == "test_user"
#     assert response.data["password"] == "test_password"
#     assert response.data["first_name"] == "test_first_name"
#     assert response.data["last_name"] == "test_last_name"
#     assert response.data["email"] == "test@email.com"
#     assert response.data["phone_number"] == "+254768850685"


# # test for user login
# def test_user_login():
#     client = APIClient()
#     url = reverse("login")
#     data = {"username": "test_user", "password": "test_password"}

#     response = client.post(url, data, format="json")
#     assert response.status_code == status.HTTP_200_Ok


# # test for user logout
# def test_user_logout():
#     client = APIClient()
#     url = reverse("logout")
#     response = client.post(url)
#     assert response.status_code == status.HTTP_200_OK
