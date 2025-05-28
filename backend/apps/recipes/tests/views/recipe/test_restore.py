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


def delete_recipe(client, api_recipe_endpoints, recipe):
    response = client.delete(
        api_recipe_endpoints['delete'](slug=recipe.slug),
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    recipe.refresh_from_db()


@pytest.mark.django_db
def test_recipe_restore_success(verified_user_with_recipe, api_recipe_endpoints):
    client, user, recipe = verified_user_with_recipe
    delete_recipe(client, api_recipe_endpoints, recipe)

    response = client.patch(
        api_recipe_endpoints['restore'](slug=recipe.slug),
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get('detail') == 'Recipe has been restored.'


@pytest.mark.django_db
def test_recipe_restore_failure_not_deleted(verified_user_with_recipe, api_recipe_endpoints):
    client, user, recipe = verified_user_with_recipe

    response = client.patch(
        api_recipe_endpoints['restore'](slug=recipe.slug),
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json().get('detail') == 'This recipe has not been deleted.'


@pytest.mark.django_db
def test_recipe_restore_failure_unauthenticated(client, verified_user_with_recipe, api_recipe_endpoints):
    auth_client, user, recipe = verified_user_with_recipe
    delete_recipe(auth_client, api_recipe_endpoints, recipe)

    response = client.patch(
        api_recipe_endpoints['restore'](slug=recipe.slug),
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json().get('detail') == 'Authentication credentials were not provided.'


@pytest.mark.django_db
def test_recipe_restore_failure_does_not_exist(verified_user_with_recipe, api_recipe_endpoints):
    client, user, recipe = verified_user_with_recipe
    delete_recipe(client, api_recipe_endpoints, recipe)

    response = client.patch(
        api_recipe_endpoints['restore'](slug='non-existing-recipe'),
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json().get('detail') == 'No Recipe matches the given query.'
