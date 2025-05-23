import pytest
import random
from io import BytesIO
from PIL import Image

from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from apps.users.models import User
from apps.recipes.models import Recipe


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def create_client():
    def _create_client(**kwargs):
        user_data = {
            "email": kwargs.get("email", f"test{random.randint(1000, 9999)}@example.com"),
            "username": kwargs.get("username", f"user{random.randint(1000, 9999)}"),
            "password": kwargs.get("password", "TestPassword123!?"),
            "description": kwargs.get("description", ""),
        }
        user = User.objects.create_user(**user_data)
        return user
    return _create_client


@pytest.fixture
def auth_client(create_client):
    user = create_client()
    client = APIClient()
    client.force_authenticate(user=user)
    return client, user


@pytest.fixture
def auth_client_2(create_client):
    user = create_client()
    client = APIClient()
    client.force_authenticate(user=user)
    return client, user


@pytest.fixture
def generate_recipe_data():
    """
    Return a callable that generates unique recipe data
    """
    def _generate(overrides:dict=None):
        base_title = f"Test Recipe {random.randint(1000, 9999)}"

        image_io = BytesIO()
        image = Image.new("RGB", (100, 100), color="red")
        image.save(image_io, format="JPEG")
        image_io.seek(0)

        data = {
            "title": base_title,
            "description": "A test description",
            "status": "draft",
            "source_url": "https://example.com/recipe",
            "final_image": SimpleUploadedFile(
                name=f"{base_title}.jpg",
                content=image_io.read(),
                content_type="image/jpeg"
            )
        }
        if overrides:
            data.update(overrides)
        return data
    return _generate


@pytest.fixture
def api_recipe_endpoints():
    BASE_ENDPOINT = 'http://127.0.0.1:8000/api/recipes/'
    BASE_VIEW_ENDPOINT = f'{BASE_ENDPOINT}view/'

    return {
        'list': f'{BASE_ENDPOINT}',
        'admin-list': f'{BASE_ENDPOINT}list/',
        'create': f'{BASE_ENDPOINT}create/',
        'random': f'{BASE_ENDPOINT}random/',
        'deleted': f'{BASE_ENDPOINT}deleted/',

        'detail': f'{BASE_VIEW_ENDPOINT}',
        'update': f'{BASE_VIEW_ENDPOINT}update/',
        'delete': f'{BASE_VIEW_ENDPOINT}delete/',
        'restore': f'{BASE_VIEW_ENDPOINT}restore/',
        'export': f'{BASE_VIEW_ENDPOINT}export/',
        'report': f'{BASE_VIEW_ENDPOINT}report/',
        'ban': f'{BASE_VIEW_ENDPOINT}ban/',
        'like': f'{BASE_VIEW_ENDPOINT}like/',
        'statistics': f'{BASE_VIEW_ENDPOINT}statistics/',
    }


@pytest.fixture
def api_tag_endpoints():
    BASE_ENDPOINT = 'http://127.0.0.1:8000/api/tags/'
    BASE_VIEW_ENDPOINT = f'{BASE_ENDPOINT}view/<slug:slug>/'

    return {
        'list': f'{BASE_ENDPOINT}',
        'create': f'{BASE_ENDPOINT}create/',

        'detail': f'{BASE_VIEW_ENDPOINT}',
        'update': f'{BASE_VIEW_ENDPOINT}update/',
        'delete': f'{BASE_VIEW_ENDPOINT}delete/',
        'suggest': f'{BASE_VIEW_ENDPOINT}suggest/',
    }
