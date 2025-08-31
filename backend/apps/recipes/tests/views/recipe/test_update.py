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
def test_update_recipe_success(verified_user_with_recipe, api_recipe_endpoints):
    client, user, recipe, recipe_data, recipe_id = verified_user_with_recipe
    
    recipe.status = RecipeStatus.PUBLISHED
    recipe.is_private = False
    recipe.save()
    
    updated_data = {
        'title': 'Updated Recipe Title',
        'description': 'Updated recipe description',
    }
    
    response = client.patch(
        api_recipe_endpoints['update'](recipe.slug),
        updated_data
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get('detail') == 'Recipe updated successfully.'
    
    recipe_response = response.json().get('recipe')
    assert recipe_response.get('title') == updated_data['title']
    assert recipe_response.get('description') == updated_data['description']
    
    recipe.refresh_from_db()
    assert recipe.title == updated_data['title']
    assert recipe.description == updated_data['description']


@pytest.mark.django_db
def test_update_recipe_partial_success(verified_user_with_recipe, api_recipe_endpoints):
    client, user, recipe, recipe_data, recipe_id = verified_user_with_recipe
    
    original_description = recipe.description
    original_source_url = recipe.source_url
    
    updated_data = {
        'title': 'Only Title Updated'
    }
    
    response = client.patch(
        api_recipe_endpoints['update'](recipe.slug),
        updated_data
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get('detail') == 'Recipe updated successfully.'
    
    recipe_response = response.json().get('recipe')
    assert recipe_response.get('title') == updated_data['title']
    assert recipe_response.get('description') == original_description
    
    recipe.refresh_from_db()
    assert recipe.title == updated_data['title']
    assert recipe.description == original_description


@pytest.mark.django_db
def test_update_recipe_status_change(verified_user_with_recipe, api_recipe_endpoints):
    client, user, recipe, recipe_data, recipe_id = verified_user_with_recipe
    
    recipe.status = RecipeStatus.DRAFT
    recipe.save()
    
    updated_data = {
        'status': RecipeStatus.PUBLISHED.value
    }
    
    response = client.patch(
        api_recipe_endpoints['update'](recipe.slug),
        updated_data
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get('detail') == 'Recipe updated successfully.'
    
    recipe_response = response.json().get('recipe')
    assert recipe_response.get('status') == RecipeStatus.PUBLISHED.value
    
    recipe.refresh_from_db()
    assert recipe.status == RecipeStatus.PUBLISHED


@pytest.mark.django_db
def test_update_recipe_privacy_toggle(verified_user_with_recipe, api_recipe_endpoints):
    client, user, recipe, recipe_data, recipe_id = verified_user_with_recipe
    
    recipe.is_private = False
    recipe.save()
    
    updated_data = {
        'is_private': True
    }
    
    response = client.patch(
        api_recipe_endpoints['update'](recipe.slug),
        updated_data
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get('detail') == 'Recipe updated successfully.'
    
    recipe_response = response.json().get('recipe')
    assert recipe_response.get('is_private') is True
    
    recipe.refresh_from_db()
    assert recipe.is_private is True


@pytest.mark.django_db
def test_update_recipe_forbidden_not_owner(verified_user_with_recipe, auth_client_2, api_recipe_endpoints):
    client, user, recipe, recipe_data, recipe_id = verified_user_with_recipe
    
    client_2, user_2 = auth_client_2
    user_2.is_verified = True
    user_2.save()
    
    updated_data = {
        'title': 'Unauthorized Update Attempt'
    }
    
    response = client_2.patch(
        api_recipe_endpoints['update'](recipe.slug),
        updated_data
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json().get('detail') == 'User must be owner.'
    
    recipe.refresh_from_db()
    assert recipe.title != updated_data['title']


@pytest.mark.django_db
def test_update_recipe_forbidden_admin_user(verified_user_with_recipe, auth_client_2, api_recipe_endpoints):
    client, user, recipe, recipe_data, recipe_id = verified_user_with_recipe

    admin_client, admin_user = auth_client_2
    admin_user.is_staff = True
    admin_user.is_superuser = True
    admin_user.is_verified = True
    admin_user.save()

    updated_data = {
        'title': 'Admin Update Attempt'
    }

    response = admin_client.patch(
        api_recipe_endpoints['update'](recipe.slug),
        updated_data
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json().get('detail') == 'User must be owner.'

    recipe.refresh_from_db()
    assert recipe.title != updated_data['title']


@pytest.mark.django_db
def test_update_recipe_forbidden_unauthenticated(client, verified_user_with_recipe, api_recipe_endpoints):
    auth_client, user, recipe, recipe_data, recipe_id = verified_user_with_recipe
    
    updated_data = {
        'title': 'Unauthenticated Update Attempt'
    }
    
    response = client.patch(
        api_recipe_endpoints['update'](recipe.slug),
        updated_data,
        content_type='application/json'
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    recipe.refresh_from_db()
    assert recipe.title != updated_data['title']


@pytest.mark.django_db
def test_update_recipe_not_found(auth_client, api_recipe_endpoints):
    client, user = auth_client
    user.is_verified = True
    user.save()
    
    updated_data = {
        'title': 'Update non-existent Recipe'
    }
    
    response = client.patch(
        api_recipe_endpoints['update']('non-existent-slug'),
        updated_data
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_update_recipe_invalid_data(verified_user_with_recipe, api_recipe_endpoints):
    client, user, recipe, recipe_data, recipe_id = verified_user_with_recipe
    
    invalid_data = {
        'title': '',
    }
    
    response = client.patch(
        api_recipe_endpoints['update'](recipe.slug),
        invalid_data
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    recipe.refresh_from_db()
    assert recipe.title != invalid_data['title']


@pytest.mark.django_db
def test_update_recipe_banned_recipe(verified_user_with_recipe, api_recipe_endpoints):
    client, user, recipe, recipe_data, recipe_id = verified_user_with_recipe
    
    recipe.is_banned = True
    recipe.save()
    
    updated_data = {
        'title': 'Update Banned Recipe'
    }
    
    response = client.patch(
        api_recipe_endpoints['update'](recipe.slug),
        updated_data
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get('detail') == 'Recipe updated successfully.'
    
    recipe.refresh_from_db()
    assert recipe.title == updated_data['title']
    assert recipe.is_banned is True
