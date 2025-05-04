from rest_framework import generics, views, status, permissions
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication

from apps.users.authentication import TokenAuthentication
from apps.users.permissions import (
    IsAdmin,
    IsVerifiedAndNotBanned,
)
from apps.recipes.models import (
    Tag,
)
from apps.recipes.serializers.tag import (
    TagSerializer,
)


class TagCreateView(generics.CreateAPIView):
    """
    Create a new tag
    """
    pass


class TagListView(generics.ListAPIView):
    """
    List all tags
    """
    pass


class TagDetailView(generics.RetrieveAPIView):
    """
    Retrieve a tag
    """
    pass


class TagUpdateView(generics.UpdateAPIView):
    """
    Update a tag
    """
    pass


class TagDeleteView(generics.DestroyAPIView):
    """
    Delete a tag
    """
    pass


class TagSuggestView(generics.ListAPIView):
    """
    Suggest tags
    """
    pass


tag_create_view = TagCreateView.as_view()
tag_list_view = TagListView.as_view()
tag_detail_view = TagDetailView.as_view()
tag_update_view = TagUpdateView.as_view()
tag_delete_view = TagDeleteView.as_view()
tag_suggest_view = TagSuggestView.as_view()
