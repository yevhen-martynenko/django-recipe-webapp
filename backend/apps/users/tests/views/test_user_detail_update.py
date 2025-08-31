import pytest

from rest_framework import status


@pytest.mark.django_db
def test_get_user_data(client, api_users_endpoints, registered_user):
    client.force_authenticate(user=registered_user)

    response = client.get(api_users_endpoints['me'])
    assert response.status_code == status.HTTP_200_OK

    user = response.json()
    assert user['email'] == registered_user.email
    assert user['username'] == registered_user.email.split('@')[0]
    

@pytest.mark.django_db
def test_patch_user_data(client, api_users_endpoints, registered_user):
    client.force_authenticate(user=registered_user)

    response = client.patch(
        api_users_endpoints['me_update'],
        {'username': 'new_username'}
    )
    assert response.status_code == status.HTTP_200_OK

    user = response.json()
    assert user['email'] == registered_user.email
    assert user['username'] == 'new_username'


@pytest.mark.django_db
def test_put_user_data(client, api_users_endpoints, registered_user):
    client.force_authenticate(user=registered_user)

    response = client.patch(
        api_users_endpoints['me_update'],
        {
            'username': 'new_username',
            'description': 'new_description',
        }
    )
    assert response.status_code == status.HTTP_200_OK

    user = response.json()
    assert user['email'] == registered_user.email
    assert user['username'] == 'new_username'
    assert user['description'] == 'new_description'


@pytest.mark.django_db
def test_put_user_data_email(client, api_users_endpoints, registered_user):
    client.force_authenticate(user=registered_user)

    response = client.patch(
        api_users_endpoints['me_update'],
        {
            'email': 'new_email@test.com',
            'username': 'new_username',
            'description': 'new_description',
        }
    )
    assert response.status_code == status.HTTP_200_OK

    user = response.json()
    assert user['email'] == 'new_email@test.com'
    assert user['username'] == 'new_username'
    assert user['description'] == 'new_description'


@pytest.mark.django_db
def test_put_user_data_unauthorized(client, api_users_endpoints):
    response = client.patch(
        api_users_endpoints['me_update'],
        {'username': 'new_username'},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    data = response.json()
    assert 'Authentication credentials were not provided.' in data['detail']


@pytest.mark.django_db
def test_put_user_data_invalid_field(client, api_users_endpoints, registered_user):
    client.force_authenticate(user=registered_user)

    response = client.patch(
        api_users_endpoints['me_update'],
        {'nonexistent_field': 'value'},
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    data = response.json()
    assert 'This field is not allowed.' in data['nonexistent_field']
