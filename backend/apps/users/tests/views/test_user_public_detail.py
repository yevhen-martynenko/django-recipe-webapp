import pytest

from rest_framework import status


@pytest.mark.django_db
def test_get_user_public_detail(client, api_users_endpoints, registered_user, registered_user2):
    client.force_authenticate(user=registered_user2)

    registered_user.is_verified = True
    registered_user.is_banned = False
    registered_user.save()
    client.force_authenticate(user=registered_user)

    response = client.get(f'{api_users_endpoints['list']}{registered_user2.username}/')
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data['username'] == registered_user2.username
    assert 'avatar' in data
    assert 'description' in data
    assert 'date_joined' in data
    assert 'last_login' in data


@pytest.mark.django_db
def test_get_user_public_detail_user_not_found(client, api_users_endpoints, registered_user):
    registered_user.is_verified = True
    registered_user.is_banned = False
    registered_user.save()
    client.force_authenticate(user=registered_user)

    response = client.get(f'{api_users_endpoints['list']}user_not_exist/')
    assert response.status_code == status.HTTP_404_NOT_FOUND

    data = response.json()
    assert 'User with the given username does not exist.' in data['detail']


@pytest.mark.django_db
def test_get_user_public_detail_user_not_verified(client, api_users_endpoints, registered_user, registered_user2):
    client.force_authenticate(user=registered_user2)

    registered_user.is_verified = False
    registered_user.is_banned = False
    registered_user.save()
    client.force_authenticate(user=registered_user)

    response = client.get(f'{api_users_endpoints['list']}{registered_user2.username}/')
    assert response.status_code == status.HTTP_403_FORBIDDEN

    data = response.json()
    assert 'User must be verified, active, and not banned.' in data['detail']


@pytest.mark.django_db
def test_get_user_public_detail_user_banned(client, api_users_endpoints, registered_user, registered_user2):
    client.force_authenticate(user=registered_user2)

    registered_user.is_verified = True
    registered_user.is_banned = True
    registered_user.save()
    client.force_authenticate(user=registered_user)

    response = client.get(f'{api_users_endpoints['list']}{registered_user2.username}/')
    assert response.status_code == status.HTTP_403_FORBIDDEN

    data = response.json()
    assert 'User must be verified, active, and not banned.' in data['detail']


@pytest.mark.django_db
def test_get_user_public_detail_user_unauthorized(client, api_users_endpoints):
    response = client.get(f'{api_users_endpoints['list']}user/')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    data = response.json()
    assert 'Authentication credentials were not provided.' in data['detail']
