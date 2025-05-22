import pytest

from rest_framework import status

from django.db.models import Q
from apps.recipes.models import Recipe, RecipeStatus


@pytest.mark.django_db
def test_random_recipe_empty(client, auth_client, api_recipe_endpoints):
    client, user = auth_client

    response = client.get(api_recipe_endpoints['random'])

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json().get('detail') == 'No recipes found.'


@pytest.mark.django_db
def test_random_recipe_unverified(client, auth_client, auth_client_2, api_recipe_endpoints, generate_recipe_data):
    client, user = auth_client
    user.is_verified = True
    user.save()

    published_data = generate_recipe_data({'status': RecipeStatus.PUBLISHED.value})
    published_response = client.post(
        api_recipe_endpoints['create'],
        published_data,
    )
    assert published_response.status_code == status.HTTP_201_CREATED
    published_recipe = published_response.json().get('recipe')

    client_2, user_2 = auth_client_2

    response = client.get(api_recipe_endpoints['random'])

    assert response.status_code == status.HTTP_200_OK
    assert response.json().get('detail') == 'Random recipe retrieved successfully.'
    assert response.json().get('recipe').get('id') == published_recipe.get('id')
    assert response.json().get('recipe').get('status') == RecipeStatus.PUBLISHED.value


@pytest.mark.django_db
def test_random_recipe_authenticated(client, auth_client, api_recipe_endpoints, generate_recipe_data):
    client, user = auth_client
    user.is_verified = True
    user.save()

    published_data = generate_recipe_data({'status': RecipeStatus.PUBLISHED.value})
    published_response = client.post(
        api_recipe_endpoints['create'],
        published_data,
    )
    assert published_response.status_code == status.HTTP_201_CREATED
    published_recipe = published_response.json().get('recipe')
    
    draft_data = generate_recipe_data({'status': RecipeStatus.DRAFT.value})
    draft_response = client.post(
        api_recipe_endpoints['create'],
        draft_data,
    )
    assert draft_response.status_code == status.HTTP_201_CREATED

    response = client.get(api_recipe_endpoints['random'])
    
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get('detail') == 'Random recipe retrieved successfully.'
    assert response.json().get('recipe').get('id') == published_recipe.get('id')
    assert response.json().get('recipe').get('status') == RecipeStatus.PUBLISHED.value


@pytest.mark.django_db
def test_random_recipe_banned_recipe(client, auth_client, api_recipe_endpoints, generate_recipe_data):
    client, user = auth_client
    user.is_verified = True
    user.save()

    recipe_data = generate_recipe_data({'status': RecipeStatus.PUBLISHED.value})
    response = client.post(
        api_recipe_endpoints['create'],
        recipe_data,
    )
    assert response.status_code == status.HTTP_201_CREATED
    recipe_json = response.json().get('recipe')
    recipe_id = recipe_json.get('id')

    recipe = Recipe.objects.get(id=recipe_id)
    recipe.is_banned = True
    recipe.save()
    
    response = client.get(api_recipe_endpoints['random'])

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json().get('detail') == 'No recipes found.'


@pytest.mark.django_db
def test_random_recipe_deleted_recipe(client, auth_client, api_recipe_endpoints, generate_recipe_data):
    client, user = auth_client
    user.is_verified = True
    user.save()

    recipe_data = generate_recipe_data({'status': RecipeStatus.PUBLISHED.value})
    response = client.post(
        api_recipe_endpoints['create'],
        recipe_data,
    )
    assert response.status_code == status.HTTP_201_CREATED
    recipe_json = response.json().get('recipe')
    recipe_id = recipe_json.get('id')

    recipe = Recipe.objects.get(id=recipe_id)
    recipe.is_deleted = True
    recipe.save()
    
    response = client.get(api_recipe_endpoints['random'])

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json().get('detail') == 'No recipes found.'


@pytest.mark.django_db
def test_random_recipe_superuser(client, auth_client, auth_client_2, api_recipe_endpoints, generate_recipe_data):
    client, user = auth_client
    user.is_verified = True
    user.is_superuser = True
    user.save()
    
    regular_client, regular_user = auth_client_2
    
    recipe_data = generate_recipe_data({'status': RecipeStatus.DRAFT.value})
    response = client.post(
        api_recipe_endpoints['create'],
        recipe_data,
    )
    recipe = response.json().get('recipe')
    
    response = client.get(api_recipe_endpoints['random'])
    
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get('detail') == 'Random recipe retrieved successfully.'
    assert response.json().get('recipe').get('id') == recipe.get('id')
    assert response.json().get('recipe').get('status') == RecipeStatus.DRAFT.value
