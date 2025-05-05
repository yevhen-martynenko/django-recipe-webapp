from rest_framework import permissions


class IsRecipeOwner(permissions.BasePermission):
    """
    Allows access only to owner recipes
    """
    message = 'User must be owner.'

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsRecipeOwnerOrPublic(permissions.BasePermission):
    """
    Allows access only to owner or public recipes
    """
    message = 'User must be owner or public recipe.'

    def has_object_permission(self, request, view, obj):
        if not hasattr(obj, 'private') or not hasattr(obj, 'author'):
            return False

        return (
            not obj.private or
            obj.author == request.user
        )
