import pytest
from django.urls import reverse, resolve
from rest_framework import status

from apps.users.views import (
    user_register_view,
    user_activate_view,
    user_login_view,
    user_logout_view,
    user_list_view,
    user_detail_update_view,
    user_delete_view,
    user_public_detail_view,
    user_google_login_view,
    user_google_login_callback_view,
)


@pytest.mark.parametrize(
    'name, kwargs, view',
    [
        ('user-register', None, user_register_view),
        ('user-activate', None, user_activate_view),
        ('user-login', None, user_login_view),
        ('user-logout', None, user_logout_view),
        ('user-list', None, user_list_view),
        ('user-detail-update', None, user_detail_update_view),
        ('user-delete', None, user_delete_view),
        ('user-public-detail', {'username': 'testuser'}, user_public_detail_view),
        ('user-google-login', None, user_google_login_view),
        ('user-google-login-callback', None, user_google_login_callback_view),
    ]
)
def test_url_resolves_correct_view(name, kwargs, view):
    path = reverse(name, kwargs=kwargs)
    resolved = resolve(path)
    assert resolved.func == view


@pytest.mark.django_db
def test_invalid_path(client):
    response = client.get('/api/invalid/')
    assert response.status_code in [status.HTTP_404_NOT_FOUND, status.HTTP_400_BAD_REQUEST]
