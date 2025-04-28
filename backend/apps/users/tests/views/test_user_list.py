import pytest

from rest_framework import status


@pytest.mark.django_db
def test_list_users_as_admin(client, api_users_endpoints, registered_admin):
    client.force_authenticate(user=registered_admin)

    response = client.get(api_users_endpoints['list'])
    assert response.status_code == status.HTTP_200_OK

    users = response.json()
    assert len(users) > 0
    for user in users:
        assert 'email' in user
        assert 'username' in user


@pytest.mark.django_db
def test_list_users_as_user(client, api_users_endpoints, registered_user):
    client.force_authenticate(user=registered_user)

    response = client.get(api_users_endpoints['list'])
    assert response.status_code == status.HTTP_403_FORBIDDEN

    data = response.json()
    assert 'You do not have permission to perform this action.' in data['detail']


@pytest.mark.django_db
def test_list_users_unauthorized(client, api_users_endpoints):
    response = client.get(api_users_endpoints['list'])
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    data = response.json()
    assert 'Authentication credentials were not provided.' in data['detail']
