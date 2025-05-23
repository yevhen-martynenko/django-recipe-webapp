import pytest

from django.test import Client
from rest_framework import status

from apps.recipes.models import Recipe, RecipeStatus


@pytest.mark.django_db
def test_recipe_detail_success(client, auth_client, api_recipe_endpoints, generate_recipe_data):
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
    recipe_slug = recipe.slug

    recipe.status = RecipeStatus.PUBLISHED
    recipe.private = False
    recipe.save()

    response = client.get(
        f"{api_recipe_endpoints['detail']}{recipe_slug}/"
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get('detail') == 'Recipe retrieved successfully.'

    recipe = response.json().get('recipe')
    assert recipe.get('id') == recipe_id
    assert recipe.get('author') == user.username
    assert recipe.get('title') == recipe_data.get('title')
    assert recipe.get('description') == recipe_data.get('description')
    assert recipe.get('source_url') == recipe_data.get('source_url')
    assert recipe.get('status') == RecipeStatus.PUBLISHED.value


@pytest.mark.django_db
def test_recipe_detail_success_by_other_user(client, auth_client, auth_client_2, api_recipe_endpoints, generate_recipe_data):
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
    recipe_slug = recipe.slug

    recipe.status = RecipeStatus.PUBLISHED
    recipe.private = False
    recipe.save()

    client_2, user_2 = auth_client_2
    user_2.is_verified = True
    user_2.save()

    response = client_2.get(
        f"{api_recipe_endpoints['detail']}{recipe_slug}/"
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get('detail') == 'Recipe retrieved successfully.'

    recipe = response.json().get('recipe')
    assert recipe.get('id') == recipe_id
    assert recipe.get('author') == user.username
    assert recipe.get('title') == recipe_data.get('title')
    assert recipe.get('description') == recipe_data.get('description')
    assert recipe.get('source_url') == recipe_data.get('source_url')
    assert recipe.get('status') == RecipeStatus.PUBLISHED.value


@pytest.mark.django_db
def test_recipe_detail_failure_by_other_user(client, auth_client, auth_client_2, api_recipe_endpoints, generate_recipe_data):
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
    recipe_slug = recipe.slug

    client_2, user_2 = auth_client_2
    user_2.is_verified = True
    user_2.save()

    response = client_2.get(
        f"{api_recipe_endpoints['detail']}{recipe_slug}/"
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json().get('detail') == 'No Recipe matches the given query.'


@pytest.mark.django_db
def test_recipe_detail_success_by_unauthenticated_user(client, auth_client, api_recipe_endpoints, generate_recipe_data):
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
    recipe_slug = recipe.slug

    recipe.status = RecipeStatus.PUBLISHED
    recipe.private = False
    recipe.save()

    unauthorized_client = Client()

    response = unauthorized_client.get(
        f"{api_recipe_endpoints['detail']}{recipe_slug}/"
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get('detail') == 'Recipe retrieved successfully.'


@pytest.mark.django_db
def test_recipe_detail_non_existing_slug(client, auth_client, api_recipe_endpoints):
    client, user = auth_client
    user.is_verified = True
    user.save()

    response = client.get(
        f"{api_recipe_endpoints['detail']}non-existing-recipe/"
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json().get('detail') == 'No Recipe matches the given query.'


@pytest.mark.django_db
def test_recipe_detail_for_banned_recipe(client, auth_client, auth_client_2, api_recipe_endpoints, generate_recipe_data):
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
    recipe_slug = recipe.slug

    recipe.is_banned = True
    recipe.save()

    client_2, user_2 = auth_client_2
    user_2.is_verified = True
    user_2.save()

    response = client_2.get(
        f"{api_recipe_endpoints['detail']}{recipe_slug}/"
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json().get('detail') == 'This recipe has been flagged as inappropriate and is hidden.'


@pytest.mark.django_db
def test_recipe_detail_for_banned_recipe_by_owner(client, auth_client, api_recipe_endpoints, generate_recipe_data):
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
    recipe_slug = recipe.slug

    recipe.is_banned = True
    recipe.save()

    response = client.get(
        f"{api_recipe_endpoints['detail']}{recipe_slug}/"
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get('detail') == 'Recipe retrieved successfully.'


@pytest.mark.django_db
def test_recipe_detail_for_deleted_recipe(client, auth_client, auth_client_2, api_recipe_endpoints, generate_recipe_data):
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
    recipe_slug = recipe.slug

    recipe.delete()

    client_2, user_2 = auth_client_2
    user_2.is_verified = True
    user_2.save()

    response = client_2.get(
        f"{api_recipe_endpoints['detail']}{recipe_slug}/"
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json().get('detail') == 'This recipe has been deleted.'


@pytest.mark.django_db
def test_recipe_detail_for_draft_recipe(client, auth_client, auth_client_2, api_recipe_endpoints, generate_recipe_data):
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
    recipe_slug = recipe.slug

    recipe.status = RecipeStatus.DRAFT
    recipe.save()

    client_2, user_2 = auth_client_2
    user_2.is_verified = True
    user_2.save()

    response = client_2.get(
        f"{api_recipe_endpoints['detail']}{recipe_slug}/"
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json().get('detail') == 'No Recipe matches the given query.'


@pytest.mark.django_db
def test_recipe_detail_for_draft_recipe_by_owner(client, auth_client, auth_client_2, api_recipe_endpoints, generate_recipe_data):
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
    recipe_slug = recipe.slug

    recipe.status = RecipeStatus.DRAFT
    recipe.save()

    response = client.get(
        f"{api_recipe_endpoints['detail']}{recipe_slug}/"
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get('detail') == 'Recipe retrieved successfully.'


@pytest.mark.django_db
def test_recipe_detail_for_private_recipe(client, auth_client, auth_client_2, api_recipe_endpoints, generate_recipe_data):
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
    recipe_slug = recipe.slug

    recipe.status = RecipeStatus.PUBLISHED
    recipe.private = True
    recipe.save()

    client_2, user_2 = auth_client_2
    user_2.is_verified = True
    user_2.save()

    response = client_2.get(
        f"{api_recipe_endpoints['detail']}{recipe_slug}/"
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json().get('detail') == 'No Recipe matches the given query.'


@pytest.mark.django_db
def test_recipe_detail_for_private_recipe_by_owner(client, auth_client, api_recipe_endpoints, generate_recipe_data):
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
    recipe_slug = recipe.slug

    recipe.status = RecipeStatus.PUBLISHED
    recipe.private = True
    recipe.save()

    response = client.get(
        f"{api_recipe_endpoints['detail']}{recipe_slug}/"
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get('detail') == 'Recipe retrieved successfully.'
