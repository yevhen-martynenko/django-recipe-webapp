import pytest

from rest_framework import status

from apps.recipes.models import Recipe


@pytest.mark.django_db
def test_create_recipe(client, auth_client, api_recipe_endpoints, generate_recipe_data):
    client, user = auth_client
    user.is_verified = True
    user.save()

    recipe_data = generate_recipe_data()
    response = client.post(
        api_recipe_endpoints['create'],
        recipe_data,
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json().get('detail') == 'Recipe created successfully.'

    recipe = response.json().get('recipe')
    assert recipe.get('author') == user.username
    assert recipe.get('title') == recipe_data.get('title')
    assert recipe.get('description') == recipe_data.get('description')
    assert recipe.get('status') == recipe_data.get('status')
    assert recipe.get('source_url') == recipe_data.get('source_url')

    recipe_obj = Recipe.objects.get(id=recipe.get('id'))
    assert recipe_obj.title == recipe.get('title')
    assert recipe_obj.description == recipe.get('description')
    assert recipe_obj.status == recipe.get('status')
    assert recipe_obj.source_url == recipe.get('source_url')


@pytest.mark.django_db
def test_create_recipe_invalid(client, auth_client, api_recipe_endpoints, generate_recipe_data):
    client, user = auth_client
    user.is_verified = True
    user.save()

    recipe_data = generate_recipe_data({'title': ''})
    response = client.post(
        api_recipe_endpoints['create'],
        recipe_data,
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    assert response.json().get('recipe') is None
    assert response.json().get('title') == ['This field may not be blank.']


@pytest.mark.django_db
def test_create_recipe_unauthorized(client, api_recipe_endpoints, generate_recipe_data):
    recipe_data = generate_recipe_data()
    response = client.post(
        api_recipe_endpoints['create'],
        recipe_data,
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    response = response.json()
    assert response.get('recipe') is None
    assert response.get('detail') == 'Authentication credentials were not provided.'


@pytest.mark.django_db
def test_create_recipe_unverified(client, auth_client, api_recipe_endpoints, generate_recipe_data):
    client, user = auth_client

    recipe_data = generate_recipe_data()
    response = client.post(
        api_recipe_endpoints['create'],
        recipe_data,
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN

    response = response.json()
    assert response.get('recipe') is None
    assert response.get('detail') == 'User must be verified, active, and not banned.'


@pytest.mark.django_db
def test_create_recipe_banned_user(client, auth_client, api_recipe_endpoints, generate_recipe_data):
    client, user = auth_client
    user.is_verified = True
    user.is_banned = True
    user.save()

    recipe_data = generate_recipe_data()
    response = client.post(
        api_recipe_endpoints['create'],
        recipe_data,
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN

    response = response.json()
    assert response.get('recipe') is None
    assert response.get('detail') == 'User must be verified, active, and not banned.'
