import pytest

from rest_framework import status

from apps.recipes.models import Recipe, RecipeStatus


@pytest.fixture
def verified_user_with_recipe(auth_client, api_recipe_endpoints, generate_recipe_data):
    """Helper fixture to create a verified user with a recipe"""
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

    recipe_id = response.json()['recipe']['id']
    recipe = Recipe.objects.get(id=recipe_id)

    return client, user, recipe, recipe_data, recipe_id


def assert_recipe_response_success(response, recipe_data, user, recipe_id):
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get('detail') == 'Random recipe retrieved successfully.'

    recipe = response.json().get('recipe')
    assert recipe.get('id') == recipe_id
    assert recipe.get('author') == user.username
    assert recipe.get('title') == recipe_data.get('title')
    assert recipe.get('description') == recipe_data.get('description')
    assert recipe.get('source_url') == recipe_data.get('source_url')
    assert recipe.get('status') == RecipeStatus.PUBLISHED.value


@pytest.mark.django_db
def test_random_recipe_success(verified_user_with_recipe, auth_client_2, api_recipe_endpoints, generate_recipe_data):
    client, user, recipe, recipe_data, recipe_id = verified_user_with_recipe

    recipe.status = RecipeStatus.PUBLISHED
    recipe.is_private = False
    recipe.save()

    client_2, user_2 = auth_client_2
    user_2.is_verified = True
    user_2.save()

    response = client.get(api_recipe_endpoints['random'])

    assert_recipe_response_success(response, recipe_data, user, recipe_id)


@pytest.mark.django_db
def test_random_recipe_failure_no_recipes(auth_client, api_recipe_endpoints):
    client, user = auth_client
    user.is_verified = True
    user.save()

    response = client.get(api_recipe_endpoints['random'])

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json().get('detail') == 'No recipes found.'


@pytest.mark.django_db
def test_random_recipe_success_authenticated(verified_user_with_recipe, auth_client_2, api_recipe_endpoints, generate_recipe_data):
    client, user, recipe, recipe_data, recipe_id = verified_user_with_recipe

    recipe.status = RecipeStatus.PUBLISHED
    recipe.is_private = False
    recipe.save()

    draft_data = generate_recipe_data({'status': RecipeStatus.DRAFT.value})
    draft_response = client.post(
        api_recipe_endpoints['create'],
        draft_data,
    )
    assert draft_response.status_code == status.HTTP_201_CREATED

    client_2, user_2 = auth_client_2
    user_2.is_verified = True
    user_2.save()

    response = client.get(api_recipe_endpoints['random'])

    assert_recipe_response_success(response, recipe_data, user, recipe_id)


@pytest.mark.django_db
def test_random_recipe_failure_banned_recipe(verified_user_with_recipe, api_recipe_endpoints):
    client, user, recipe, recipe_data, recipe_id = verified_user_with_recipe

    recipe.status = RecipeStatus.PUBLISHED
    recipe.is_private = False
    recipe.is_banned = True
    recipe.save()

    response = client.get(api_recipe_endpoints['random'])

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json().get('detail') == 'No recipes found.'


@pytest.mark.django_db
def test_random_recipe_failure_deleted_recipe(verified_user_with_recipe, api_recipe_endpoints):
    client, user, recipe, recipe_data, recipe_id = verified_user_with_recipe

    recipe.status = RecipeStatus.PUBLISHED
    recipe.is_private = False
    recipe.save()

    # recipe.is_deleted = True
    recipe.delete()

    response = client.get(api_recipe_endpoints['random'])

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json().get('detail') == 'No recipes found.'


@pytest.mark.django_db
def test_random_recipe_success_superuser(auth_client, auth_client_2, api_recipe_endpoints, generate_recipe_data):
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
