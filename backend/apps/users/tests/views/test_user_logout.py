import pytest

from rest_framework import status
from rest_framework.authtoken.models import Token

from apps.users.models import User


def register_user(client, api_auth_endpoints, generate_user_data):
    user_data = generate_user_data()
    response = client.post(
        api_auth_endpoints['register'],
        user_data,
    )
    assert response.status_code == status.HTTP_201_CREATED
    user = response.json().get('user')
    token = response.json().get('token')

    user_obj = User.objects.get(id=user.get('id'))

    return user_obj


@pytest.mark.django_db
def test_user_logout_success(client, api_auth_endpoints, generate_user_data):
    user = register_user(client, api_auth_endpoints, generate_user_data)
    assert Token.objects.filter(user=user).exists()

    response = client.post(api_auth_endpoints['logout'])
    assert response.status_code == status.HTTP_200_OK
    assert not Token.objects.filter(user=user).exists()

    data = response.json()
    assert 'Successfully logged out.' in data['detail']


@pytest.mark.django_db
def test_user_logout_without_token(client, api_auth_endpoints, generate_user_data):
    user = register_user(client, api_auth_endpoints, generate_user_data)
    assert Token.objects.filter(user=user).exists()
    token = Token.objects.get(user=user)
    token.delete()
    assert not Token.objects.filter(user=user).exists()

    response = client.post(api_auth_endpoints['logout'])
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert 'Successfully logged out.' in data['detail']


@pytest.mark.django_db
def test_user_logout_unauthorized(client, api_auth_endpoints):
    response = client.post(api_auth_endpoints['logout'])
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    data = response.json()
    assert 'Authentication credentials were not provided.' in data['detail']
