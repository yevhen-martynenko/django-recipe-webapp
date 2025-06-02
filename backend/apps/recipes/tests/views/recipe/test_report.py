import pytest

from rest_framework import status

from apps.recipes.models import Recipe, RecipeReport


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
    
    recipe_id = response.json()['recipe']['id']
    recipe = Recipe.objects.get(id=recipe_id)
    
    return client, user, recipe


@pytest.mark.django_db
def test_report_recipe_success(verified_user_with_recipe, api_recipe_endpoints):
    client, user, recipe = verified_user_with_recipe
    report_data = {
        'reason': 'spam',
        'description': 'This recipe contains spam content',
    }
    
    response = client.post(
        api_recipe_endpoints['report'](slug=recipe.slug),
        report_data,
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json().get('detail') == 'Recipe reported successfully.'
    assert RecipeReport.objects.filter(recipe=recipe, user=user).exists()

    report = RecipeReport.objects.get(recipe=recipe, user=user)
    expected_str = f'Report on "{recipe.title}" by "{user}"'
    assert str(report) == expected_str


@pytest.mark.django_db
def test_report_recipe_invalid_reason(verified_user_with_recipe, api_recipe_endpoints):
    client, user, recipe = verified_user_with_recipe
    invalid_report_data = {
        'reason': 'ab',
        'description': 'This recipe contains spam content',
    }

    response = client.post(
        api_recipe_endpoints['report'](slug=recipe.slug),
        invalid_report_data,
    )
    assert response.status_code == 400
    assert response.json().get('reason') == ['Please provide a more detailed reason.']


@pytest.mark.django_db
def test_report_recipe_duplicate_report(verified_user_with_recipe, api_recipe_endpoints):
    client, user, recipe = verified_user_with_recipe
    report_data = {
        'reason': 'spam',
        'description': 'This recipe contains spam content',
    }
    
    response = client.post(
        api_recipe_endpoints['report'](slug=recipe.slug),
        report_data,
    )
    assert response.status_code == status.HTTP_201_CREATED
    
    response = client.post(
        api_recipe_endpoints['report'](slug=recipe.slug),
        report_data,
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json().get('detail') == 'You have already reported this recipe.'


@pytest.mark.django_db
def test_report_recipe_unauthenticated(client, verified_user_with_recipe, api_recipe_endpoints):
    auth_client, user, recipe = verified_user_with_recipe
    report_data = {
        'reason': 'spam',
        'description': 'This recipe contains spam content',
    }
    
    response = client.post(
        api_recipe_endpoints['report'](slug=recipe.slug),
        report_data,
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json().get('detail') == 'Authentication credentials were not provided.'


@pytest.mark.django_db
def test_report_recipe_invalid_data(verified_user_with_recipe, api_recipe_endpoints):
    client, user, recipe = verified_user_with_recipe
    
    response = client.post(
        api_recipe_endpoints['report'](slug=recipe.slug),
        {},
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_report_recipe_nonexistent_recipe(verified_user_with_recipe, api_recipe_endpoints):
    client, user, recipe = verified_user_with_recipe
    report_data = {
        'reason': 'spam',
        'description': 'This recipe contains spam content',
    }
    
    response = client.post(
        api_recipe_endpoints['report'](slug='non-existent-recipe'),
        report_data,
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json().get('detail') == 'No Recipe matches the given query.'
