import pytest


@pytest.mark.django_db
def test_create_user(user, client):
    response = client.post(
        "/api/accounts/register",
        {
            "username": "test",
            "email": "test@gmail.com",
            "password": "test",
        },
    )

    assert response.status_code == 201
    assert response.data["username"] == "test"
    assert response.data["email"] == "test@gmail.com"
    assert "password" not in response.data
    assert "id" not in response.data


@pytest.mark.django_db
def test_login_user(user, client):
    response = client.post(
        "/api/accounts/login",
        {
            "username": "test_user",
            "password": "test",
        },
    )

    assert response.status_code == 200
    assert "access_token" in response.data
    assert "password" not in response.data
    assert "id" not in response.data


@pytest.mark.django_db
def test_create_customer(tokenized_client, user):
    response = tokenized_client.post(
        "/api/customers",
        {
            "name": "test",
            "email": "customer@gmail.com",
            "phonenumber": "+254768850678",
            "user": user.id,
        },
    )
    assert response.status_code == 201
    assert response.data["name"] == "test"
    assert response.data["email"] == "customer@gmail.com"
    assert response.data["phonenumber"] == "+254768850678"
    assert "id" in response.data
