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


@pytest.mark.django_db
def test_like_recipe_success(verified_user_with_recipe, api_recipe_endpoints):
    client, user, recipe, recipe_data, recipe_id = verified_user_with_recipe

    recipe.status = RecipeStatus.PUBLISHED
    recipe.is_private = False
    recipe.save()

    response = client.post(
        api_recipe_endpoints['like'](recipe.slug),
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json().get('detail') == 'Recipe liked.'
    assert recipe.is_liked_by(user) is True


@pytest.mark.django_db
def test_unlike_recipe_success(verified_user_with_recipe, api_recipe_endpoints):
    client, user, recipe, recipe_data, recipe_id = verified_user_with_recipe

    recipe.status = RecipeStatus.PUBLISHED
    recipe.is_private = False
    recipe.save()

    response = client.post(
        api_recipe_endpoints['like'](recipe.slug),
    )
    assert response.status_code == status.HTTP_201_CREATED

    response = client.delete(
        api_recipe_endpoints['like'](recipe.slug),
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    # assert response.json().get('detail') == 'Recipe unliked.'
    assert recipe.is_liked_by(user) is False


@pytest.mark.django_db
def test_like_recipe_failure(verified_user_with_recipe, api_recipe_endpoints):
    client, user, recipe, recipe_data, recipe_id = verified_user_with_recipe

    recipe.status = RecipeStatus.PUBLISHED
    recipe.is_private = False
    recipe.save()

    response = client.post(
        api_recipe_endpoints['like'](recipe.slug),
    )
    assert response.status_code == status.HTTP_201_CREATED

    response = client.post(
        api_recipe_endpoints['like'](recipe.slug),
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json().get('detail') == 'You have already liked this recipe.'
    assert recipe.is_liked_by(user) is True


@pytest.mark.django_db
def test_unlike_recipe_failure(verified_user_with_recipe, api_recipe_endpoints):
    client, user, recipe, recipe_data, recipe_id = verified_user_with_recipe

    recipe.status = RecipeStatus.PUBLISHED
    recipe.is_private = False
    recipe.save()

    response = client.delete(
        api_recipe_endpoints['like'](recipe.slug),
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json().get('detail') == 'You haven\'t liked this recipe yet.'
    assert recipe.is_liked_by(user) is False


@pytest.mark.django_db
def test_like_recipe_failure_unauthenticated(client, verified_user_with_recipe, api_recipe_endpoints):
    auth_client, user, recipe, recipe_data, recipe_id = verified_user_with_recipe

    recipe.status = RecipeStatus.PUBLISHED
    recipe.is_private = False
    recipe.save()

    response = client.post(
        api_recipe_endpoints['like'](recipe.slug),
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json().get('detail') == 'Authentication credentials were not provided.'


@pytest.mark.django_db
def test_unlike_recipe_failure_unauthenticated(client, verified_user_with_recipe, api_recipe_endpoints):
    auth_client, user, recipe, recipe_data, recipe_id = verified_user_with_recipe

    recipe.status = RecipeStatus.PUBLISHED
    recipe.is_private = False
    recipe.save()

    response = client.delete(
        api_recipe_endpoints['like'](recipe.slug),
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json().get('detail') == 'Authentication credentials were not provided.'
