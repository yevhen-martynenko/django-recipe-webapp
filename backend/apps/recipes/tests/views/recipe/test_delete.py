import pytest

from rest_framework import status

from apps.recipes.models import Recipe


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
    
    return client, user, recipe


@pytest.mark.django_db
def test_delete_recipe_success(verified_user_with_recipe, api_recipe_endpoints):
    client, user, recipe = verified_user_with_recipe

    response = client.delete(
        api_recipe_endpoints['delete'](slug=recipe.slug),
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_delete_recipe_failure_by_other_user(verified_user_with_recipe, auth_client_2, api_recipe_endpoints):
    client, user, recipe = verified_user_with_recipe

    client_2, user_2 = auth_client_2
    user_2.is_verified = True
    user_2.save()

    response = client_2.delete(
        api_recipe_endpoints['delete'](slug=recipe.slug),
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_delete_recipe_failure_already_deleted(verified_user_with_recipe, api_recipe_endpoints):
    client, user, recipe = verified_user_with_recipe

    response = client.delete(
        api_recipe_endpoints['delete'](slug=recipe.slug),
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    recepe.refresh_from_db()

    response = client.delete(
        api_recipe_endpoints['delete'](slug=recipe.slug),
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json().get('detail') == 'This recipe has already been deleted.'


@pytest.mark.django_db
def test_delete_recipe_failure_does_not_exist(auth_client, api_recipe_endpoints, generate_recipe_data):
    client, user = auth_client
    user.is_verified = True
    user.save()

    response = client.delete(
        api_recipe_endpoints['delete'](slug='non-existent-recipe'),
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json().get('detail') == 'No Recipe matches the given query.'


@pytest.mark.django_db
def test_delete_recipe_failure_unauthenticated(client, verified_user_with_recipe, api_recipe_endpoints):
    auth_client, user, recipe = verified_user_with_recipe

    response = client.delete(
        api_recipe_endpoints['delete'](slug=recipe.slug),
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json().get('detail') == 'Authentication credentials were not provided.'
