import pytest
from unittest.mock import patch

from rest_framework import status
from rest_framework.authtoken.models import Token

from apps.users.models import User


@pytest.mark.django_db
def test_user_delete_success(client, api_users_endpoints, registered_user):
    client.force_authenticate(user=registered_user)
    assert User.objects.filter(id=registered_user.id).exists()
    assert Token.objects.filter(user=registered_user.id).exists()

    response = client.delete(api_users_endpoints['me_delete'])
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert 'No Content: Account deleted successfully.' in response.data['detail']
    assert not User.objects.filter(id=registered_user.id).exists()
    assert not Token.objects.filter(user=registered_user.id).exists()


@pytest.mark.django_db
def test_user_delete_unauthorized(client, api_users_endpoints):
    response = client.delete(api_users_endpoints['me_delete'])
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert 'Authentication credentials were not provided.' in response.data['detail']


@pytest.mark.django_db
@patch('apps.users.views.logout')
def test_delete_user_logs_out(mock_logout, client, api_users_endpoints, registered_user):
    client.force_authenticate(user=registered_user)

    response = client.delete(api_users_endpoints['me_delete'])
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not User.objects.filter(id=registered_user.id).exists()
    assert not Token.objects.filter(user=registered_user.id).exists()
    mock_logout.assert_called_once()
