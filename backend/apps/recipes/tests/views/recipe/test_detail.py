import pytest

from django.test import Client
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
    assert response.json().get('detail') == 'Recipe retrieved successfully.'

    recipe = response.json().get('recipe')
    assert recipe.get('id') == recipe_id
    assert recipe.get('author') == user.username
    assert recipe.get('title') == recipe_data.get('title')
    assert recipe.get('description') == recipe_data.get('description')
    assert recipe.get('source_url') == recipe_data.get('source_url')


@pytest.mark.django_db
def test_recipe_detail_success(verified_user_with_recipe, api_recipe_endpoints):
    client, user, recipe, recipe_data, recipe_id = verified_user_with_recipe

    recipe.status = RecipeStatus.PUBLISHED
    recipe.is_private = False
    recipe.save()

    response = client.get(
        api_recipe_endpoints['detail'](recipe.slug),
    )
    assert_recipe_response_success(response, recipe_data, user, recipe_id)


@pytest.mark.django_db
def test_recipe_detail_success_by_other_user(verified_user_with_recipe, auth_client_2, api_recipe_endpoints):
    client, user, recipe, recipe_data, recipe_id = verified_user_with_recipe

    recipe.status = RecipeStatus.PUBLISHED
    recipe.is_private = False
    recipe.save()

    client_2, user_2 = auth_client_2
    user_2.is_verified = True
    user_2.save()

    response = client_2.get(
        api_recipe_endpoints['detail'](recipe.slug),
    )
    assert_recipe_response_success(response, recipe_data, user, recipe_id)


@pytest.mark.django_db
def test_recipe_detail_success_by_unauthenticated_user(client, verified_user_with_recipe, api_recipe_endpoints):
    auth_client, user, recipe, recipe_data, recipe_id = verified_user_with_recipe

    recipe.status = RecipeStatus.PUBLISHED
    recipe.is_private = False
    recipe.save()

    response = client.get(
        api_recipe_endpoints['detail'](recipe.slug),
    )
    assert_recipe_response_success(response, recipe_data, user, recipe_id)


@pytest.mark.django_db
def test_recipe_detail_non_existing_slug(auth_client, api_recipe_endpoints):
    client, user = auth_client
    user.is_verified = True
    user.save()

    response = client.get(
        api_recipe_endpoints['detail']('non-existing-recipe'),
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json().get('detail') == 'No Recipe matches the given query.'


@pytest.mark.django_db
def test_recipe_detail_for_banned_recipe(verified_user_with_recipe, auth_client_2, api_recipe_endpoints):
    client, user, recipe, recipe_data, recipe_id = verified_user_with_recipe

    recipe.is_banned = True
    recipe.save()

    client_2, user_2 = auth_client_2
    user_2.is_verified = True
    user_2.save()

    response = client_2.get(
        api_recipe_endpoints['detail'](recipe.slug),
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json().get('detail') == 'This recipe has been flagged as inappropriate and is hidden.'


@pytest.mark.django_db
def test_recipe_detail_for_banned_recipe_by_owner(verified_user_with_recipe, api_recipe_endpoints):
    client, user, recipe, recipe_data, recipe_id = verified_user_with_recipe

    recipe.is_banned = True
    recipe.save()

    response = client.get(
        api_recipe_endpoints['detail'](recipe.slug),
    )
    assert_recipe_response_success(response, recipe_data, user, recipe_id)


@pytest.mark.django_db
def test_recipe_detail_for_deleted_recipe(verified_user_with_recipe, auth_client_2, api_recipe_endpoints):
    client, user, recipe, recipe_data, recipe_id = verified_user_with_recipe

    recipe.delete()

    client_2, user_2 = auth_client_2
    user_2.is_verified = True
    user_2.save()

    response = client_2.get(
        api_recipe_endpoints['detail'](recipe.slug),
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json().get('detail') == 'This recipe has been deleted.'


@pytest.mark.django_db
def test_recipe_detail_for_draft_recipe(verified_user_with_recipe, auth_client_2, api_recipe_endpoints):
    client, user, recipe, recipe_data, recipe_id = verified_user_with_recipe

    recipe.status = RecipeStatus.DRAFT
    recipe.save()

    client_2, user_2 = auth_client_2
    user_2.is_verified = True
    user_2.save()

    response = client_2.get(
        api_recipe_endpoints['detail'](recipe.slug),
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json().get('detail') == 'No Recipe matches the given query.'


@pytest.mark.django_db
def test_recipe_detail_for_draft_recipe_by_owner(verified_user_with_recipe, auth_client_2, api_recipe_endpoints):
    client, user, recipe, recipe_data, recipe_id = verified_user_with_recipe

    recipe.status = RecipeStatus.DRAFT
    recipe.save()

    response = client.get(
        api_recipe_endpoints['detail'](recipe.slug),
    )
    assert_recipe_response_success(response, recipe_data, user, recipe_id)


@pytest.mark.django_db
def test_recipe_detail_for_private_recipe(verified_user_with_recipe, auth_client_2, api_recipe_endpoints):
    client, user, recipe, recipe_data, recipe_id = verified_user_with_recipe

    recipe.status = RecipeStatus.PUBLISHED
    recipe.is_private = True
    recipe.save()

    client_2, user_2 = auth_client_2
    user_2.is_verified = True
    user_2.save()

    response = client_2.get(
        api_recipe_endpoints['detail'](recipe.slug),
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json().get('detail') == 'No Recipe matches the given query.'


@pytest.mark.django_db
def test_recipe_detail_for_private_recipe_by_owner(verified_user_with_recipe, api_recipe_endpoints):
    client, user, recipe, recipe_data, recipe_id = verified_user_with_recipe

    recipe.status = RecipeStatus.PUBLISHED
    recipe.is_private = True
    recipe.save()

    response = client.get(
        api_recipe_endpoints['detail'](recipe.slug),
    )
    assert_recipe_response_success(response, recipe_data, user, recipe_id)
