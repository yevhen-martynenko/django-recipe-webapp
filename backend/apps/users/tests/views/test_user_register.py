import pytest

from rest_framework import status
from rest_framework.authtoken.models import Token

from apps.users.models import User


@pytest.mark.django_db
def test_registration(client, api_auth_endpoints, generate_user_data):
    user_data = generate_user_data()
    response = client.post(
        api_auth_endpoints['register'],
        user_data,
    )
    assert response.status_code == status.HTTP_201_CREATED

    user = response.json().get('user')
    token = response.json().get('token')
    assert user.get('email') == user_data.get('email')
    assert user.get('username')
    assert 'password' not in user
    assert 'id' in user

    user_obj = User.objects.get(id=user.get('id'))
    assert user_obj.email == user.get('email')
    assert user_obj.username == user.get('username')

    token_obj = Token.objects.get(key=token)
    assert token_obj.user == user_obj


@pytest.mark.django_db
def test_registration_with_username(client, api_auth_endpoints, generate_user_data):
    user_data = generate_user_data({'username': 'test'})

    response = client.post(
        api_auth_endpoints['register'],
        user_data,
    )
    assert response.status_code == status.HTTP_201_CREATED

    user = response.json().get('user')
    token = response.json().get('token')
    assert user.get('email') == user_data.get('email')
    assert user.get('username') == user_data.get('username')
    assert 'password' not in user
    assert 'id' in user

    user_obj = User.objects.get(id=user.get('id'))
    assert user_obj.email == user.get('email')
    assert user_obj.username == user.get('username')

    token_obj = Token.objects.get(key=token)
    assert token_obj.user == user_obj


@pytest.mark.django_db
def test_registration_duplicate_email(client, api_auth_endpoints, generate_user_data):
    response1 = client.post(
        api_auth_endpoints['register'],
        generate_user_data({'email': 'test@test.com'})
    )
    assert response1.status_code == status.HTTP_201_CREATED

    response2 = client.post(
        api_auth_endpoints['register'],
        generate_user_data({'email': 'test@test.com'})
    )
    assert response2.status_code == status.HTTP_400_BAD_REQUEST

    data = response2.json()
    assert 'email' in data
    assert 'Email already exists.' in data['email']


@pytest.mark.django_db
def test_registration_duplicate_username(client, api_auth_endpoints, generate_user_data):
    response1 = client.post(
        api_auth_endpoints['register'],
        generate_user_data({'username': 'test'})
    )
    assert response1.status_code == status.HTTP_201_CREATED

    response2 = client.post(
        api_auth_endpoints['register'],
        generate_user_data({'username': 'test'})
    )
    assert response2.status_code == status.HTTP_400_BAD_REQUEST

    data = response2.json()
    assert 'username' in data
    assert 'Username already exists.' in data['username']


@pytest.mark.django_db
def test_registration_common_password(client, api_auth_endpoints, generate_user_data):
    response = client.post(
        api_auth_endpoints['register'],
        generate_user_data({'password': 'abc123'})
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    data = response.json()
    assert 'password' in data
    assert 'This password is too common.' in data['password']
    assert 'This password is too short. It must contain at least 8 characters.' in data['password']
