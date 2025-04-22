import pytest
import random
import io

from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def api_auth_endpoints():
    BASE_ENDPOINT = 'http://127.0.0.1:8000/api/auth/'

    return {
        'register': f'{BASE_ENDPOINT}register/',
        'login': f'{BASE_ENDPOINT}login/',
        'logout': f'{BASE_ENDPOINT}logout/',
    }


@pytest.fixture
def api_users_endpoints():
    BASE_ENDPOINT = 'http://127.0.0.1:8000/api/users/'

    return {
        'list': f'{BASE_ENDPOINT}',
        'me': f'{BASE_ENDPOINT}me/',
        'me_update': f'{BASE_ENDPOINT}me/',
        'me_delete': f'{BASE_ENDPOINT}me/delete/',
    }


@pytest.fixture
def generate_user_data():
    """
    Return a callable that generates unique user data
    """
    def _generate(overrides=None):
        user_id = f'{random.randint(1, 999_999):0>6}'
        data = {
            'email': f'test.{user_id}@test.com',
            'username': '',
            'password': f'Password{user_id}',
        }
        if overrides:
            data.update(overrides)
        return data
    return _generate
