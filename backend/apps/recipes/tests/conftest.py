import pytest
import random

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
            "password": kwargs.get("password", "TestPassword123!"),
        }
        user = User.objects.create_user(**user_data)
        return user
    return _create_client


@pytest.fixture
def auth_client():
    user = create_user()
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
            data = {
                "title": base_title,
                "description": "A test description",
                "status": "draft",
                "source_url": "https://example.com/recipe",
            }
            if overrides:
                data.update(overrides)
            return data
        return _generate
