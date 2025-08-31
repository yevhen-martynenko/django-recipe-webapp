import pytest

from django.urls import reverse, resolve
from rest_framework import status

from apps.recipes.views.recipe import (
    recipe_create_view,
    recipe_list_view,
    recipe_admin_list_view,
    random_recipe_view,

    recipe_detail_view,
    recipe_update_view,
    recipe_delete_view,
    deleted_recipe_list_view,
    recipe_restore_view,
    recipe_export_view,
    recipe_report_view,
    recipe_ban_view,
    recipe_like_view,
    recipe_statistics_view,
)


@pytest.mark.parametrize(
    'name, kwargs, view',
    [
        ('recipe-list-user', None, recipe_list_view),
        ('recipe-list', None, recipe_admin_list_view),
        ('recipe-create', None, recipe_create_view),
        ('recipe-random', None, random_recipe_view),
        ('recipe-deleted', None, deleted_recipe_list_view),

        ('recipe-detail', {'slug': 'test-slug'}, recipe_detail_view),
        ('recipe-update', {'slug': 'test-slug'}, recipe_update_view),
        ('recipe-delete', {'slug': 'test-slug'}, recipe_delete_view),
        ('recipe-restore', {'slug': 'test-slug'}, recipe_restore_view),
        ('recipe-export', {'slug': 'test-slug'}, recipe_export_view),
        ('recipe-report', {'slug': 'test-slug'}, recipe_report_view),
        ('recipe-ban', {'slug': 'test-slug'}, recipe_ban_view),
        ('recipe-like', {'slug': 'test-slug'}, recipe_like_view),
        ('recipe-statistics', {'slug': 'test-slug'}, recipe_statistics_view),
    ]
)
def test_recipe_urls_resolve_correct_view(name, kwargs, view):
    path = reverse(name, kwargs=kwargs)
    resolved = resolve(path)
    assert resolved.func == view
