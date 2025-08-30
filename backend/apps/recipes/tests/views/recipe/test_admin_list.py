import pytest

from rest_framework import status

from apps.recipes.models import Recipe


@pytest.fixture
def verified_user_with_recipe(auth_client, api_recipe_endpoints, generate_recipe_data):
    """Helper fixture to create a verified user with a recipe"""
    client, user = auth_client
    user.is_verified = True
    user.save()
    recipes = []
    
    for _ in range(4):
        recipe_data = generate_recipe_data()
        response = client.post(
            api_recipe_endpoints['create'],
            recipe_data,
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json().get('detail') == 'Recipe created successfully.'
        
        recipe_id = response.json()['recipe']['id']
        recipe = Recipe.objects.get(id=recipe_id)
        recipes.append(recipe)
    
    return client, user, recipes


@pytest.mark.django_db
def test_admin_list_recipes_success(verified_user_with_recipe, api_recipe_endpoints):
    client, user, recipes = verified_user_with_recipe
    user.is_admin = True
    user.is_staff = True
    user.is_superuser = True
    user.save()

    response = client.get(
        api_recipe_endpoints['list'],
        HTTP_ACCEPT='application/json',
    )
    assert response.status_code == status.HTTP_200_OK

    response_data = response.json()
    assert len(response_data) == 4
    
    response_ids = {recipe['id'] for recipe in response_data}
    recipe_ids = {str(recipe.id) for recipe in recipes}
    assert response_ids == recipe_ids
    
    for recipe_data in response_data:
        assert 'id' in recipe_data
        assert 'title' in recipe_data
        assert 'author' in recipe_data
        assert 'description' in recipe_data
        assert 'final_image' in recipe_data
        assert 'is_liked' in recipe_data
        assert 'views_count' in recipe_data
        assert 'likes_count' in recipe_data


@pytest.mark.django_db
def test_admin_list_recipes_failure_unathenticated(client, api_recipe_endpoints):
    response = client.get(
        api_recipe_endpoints['list'],
        HTTP_ACCEPT='application/json',
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json().get('detail') == 'Authentication credentials were not provided.'


@pytest.mark.django_db
def test_admin_list_recipes_no_recipes(auth_client, api_recipe_endpoints):
    client, user = auth_client
    user.is_admin = True
    user.is_staff = True
    user.is_superuser = True
    user.save()

    response = client.get(
        api_recipe_endpoints['list'],
        HTTP_ACCEPT='application/json',
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []
