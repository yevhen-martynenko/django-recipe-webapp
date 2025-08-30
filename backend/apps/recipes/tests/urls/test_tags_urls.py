import pytest

from django.urls import reverse, resolve
from rest_framework import status

from apps.recipes.views.tag import (
    tag_list_view,
    tag_create_view,
    tag_detail_view,
    tag_update_view,
    tag_delete_view,
    tag_suggestion_create_view,
)


@pytest.mark.parametrize(
    'name, kwargs, view',
    [
        ('tag-list', None, tag_list_view),
        ('tag-create', None, tag_create_view),

        ('tag-detail', {'slug': 'test-slug'}, tag_detail_view),
        ('tag-update', {'slug': 'test-slug'}, tag_update_view),
        ('tag-delete', {'slug': 'test-slug'}, tag_delete_view),
        ('tag-suggestion-create', None, tag_suggestion_create_view),
    ]
)
def test_tag_urls_resolve_correct_view(name, kwargs, view):
    path = reverse(name, kwargs=kwargs)
    resolved = resolve(path)
    assert resolved.func == view
