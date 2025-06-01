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


@pytest.fixture
def verified_user_with_mixed_recipes(auth_client, api_recipe_endpoints, generate_recipe_data):
    """Helper fixture to create a verified user with both deleted and non-deleted recipes"""
    client, user = auth_client
    user.is_verified = True
    user.save()
    
    deleted_recipes = []
    active_recipes = []
    
    for _ in range(3):
        recipe_data = generate_recipe_data()
        response = client.post(
            api_recipe_endpoints['create'],
            recipe_data,
        )
        assert response.status_code == status.HTTP_201_CREATED
        
        recipe_id = response.json()['recipe']['id']
        recipe = Recipe.objects.get(id=recipe_id)
        recipe.is_deleted = True
        recipe.save()
        deleted_recipes.append(recipe)
    
    for _ in range(2):
        recipe_data = generate_recipe_data()
        response = client.post(
            api_recipe_endpoints['create'],
            recipe_data,
        )
        assert response.status_code == status.HTTP_201_CREATED
        
        recipe_id = response.json()['recipe']['id']
        recipe = Recipe.objects.get(id=recipe_id)
        active_recipes.append(recipe)
    
    return client, user, deleted_recipes, active_recipes


@pytest.mark.django_db
def test_deleted_recipe_list_success(verified_user_with_recipe, api_recipe_endpoints):
    client, user, recipes = verified_user_with_recipe
    
    for recipe in recipes:
        recipe.is_deleted = True
        recipe.save()
    
    response = client.get(
        api_recipe_endpoints['deleted'],
    )
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert len(response_data) == 4
    
    response_ids = {recipe['id'] for recipe in response_data}
    recipe_ids = {str(recipe.id) for recipe in recipes}
    assert response_ids == recipe_ids


@pytest.mark.django_db
def test_deleted_recipe_list_mixed_recipes(verified_user_with_mixed_recipes, api_recipe_endpoints):
    client, user, deleted_recipes, active_recipes = verified_user_with_mixed_recipes
    
    response = client.get(
        api_recipe_endpoints['deleted'],
    )
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert len(response_data) == 3
    
    response_ids = {recipe['id'] for recipe in response_data}
    deleted_recipe_ids = {str(recipe.id) for recipe in deleted_recipes}
    assert response_ids == deleted_recipe_ids


@pytest.mark.django_db
def test_deleted_recipe_list_no_deleted_recipes(auth_client, api_recipe_endpoints, generate_recipe_data):
    client, user = auth_client
    user.is_verified = True
    user.save()
    
    for _ in range(2):
        recipe_data = generate_recipe_data()
        response = client.post(
            api_recipe_endpoints['create'],
            recipe_data,
        )
        assert response.status_code == status.HTTP_201_CREATED
    
    response = client.get(
        api_recipe_endpoints['deleted'],
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


@pytest.mark.django_db
def test_deleted_recipe_list_unauthenticated(client, api_recipe_endpoints):
    response = client.get(
        api_recipe_endpoints['deleted'],
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json().get('detail') == 'Authentication credentials were not provided.'


@pytest.mark.django_db
def test_deleted_recipe_list_unverified_user(auth_client, api_recipe_endpoints):
    client, user = auth_client
    
    response = client.get(
        api_recipe_endpoints['deleted'],
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []
