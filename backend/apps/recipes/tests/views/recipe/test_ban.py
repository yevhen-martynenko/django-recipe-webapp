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
def test_ban_recipe_success_by_admin(verified_user_with_recipe, api_recipe_endpoints):
    client, user, recipe, recipe_data, recipe_id = verified_user_with_recipe

    user.is_admin = True
    user.is_staff = True
    user.is_superuser = True
    user.save()

    recipe.status = RecipeStatus.PUBLISHED
    recipe.is_private = False
    recipe.save()

    response = client.patch(
        api_recipe_endpoints['ban'](recipe.slug),
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get('detail') == 'Recipe has been banned.'


@pytest.mark.django_db
def test_unban_recipe_success_by_admin(verified_user_with_recipe, api_recipe_endpoints):
    client, user, recipe, recipe_data, recipe_id = verified_user_with_recipe

    user.is_admin = True
    user.is_staff = True
    user.is_superuser = True
    user.save()

    recipe.status = RecipeStatus.PUBLISHED
    recipe.is_private = False
    recipe.is_banned = True
    recipe.save()

    response = client.patch(
        api_recipe_endpoints['ban'](recipe.slug),
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get('detail') == 'Recipe has been unbanned.'


@pytest.mark.django_db
def test_ban_recipe_failure_not_admin(verified_user_with_recipe, api_recipe_endpoints):
    client, user, recipe, recipe_data, recipe_id = verified_user_with_recipe

    recipe.status = RecipeStatus.PUBLISHED
    recipe.is_private = False
    recipe.is_banned = True
    recipe.save()

    response = client.patch(
        api_recipe_endpoints['ban'](recipe.slug),
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json().get('detail') == 'You do not have permission to perform this action.'


@pytest.mark.django_db
def test_ban_recipe_failure_unauthenticated(client, verified_user_with_recipe, api_recipe_endpoints):
    auth_client, user, recipe, recipe_data, recipe_id = verified_user_with_recipe

    recipe.status = RecipeStatus.PUBLISHED
    recipe.is_private = False
    recipe.save()

    response = client.patch(
        api_recipe_endpoints['ban'](recipe.slug),
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json().get('detail') == 'Authentication credentials were not provided.'


@pytest.mark.django_db
def test_ban_recipe_failure_not_found(verified_user_with_recipe, api_recipe_endpoints):
    client, user, recipe, recipe_data, recipe_id = verified_user_with_recipe

    user.is_admin = True
    user.is_staff = True
    user.is_superuser = True
    user.save()

    recipe.status = RecipeStatus.PUBLISHED
    recipe.is_private = False
    recipe.save()

    response = client.patch(
        api_recipe_endpoints['ban']('non-existent-recipe'),
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json().get('detail') == 'No Recipe matches the given query.'
