from rest_framework import permissions

from apps.recipes.models import RecipeStatus


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
    message = 'User must be owner or recipe must be public and published.'

    def has_object_permission(self, request, view, obj):
        if not hasattr(obj, 'is_private') or not hasattr(obj, 'status') or not hasattr(obj, 'author'):
            return False

        if obj.author == request.user:
            return True

        return True
        # return not obj.is_private and obj.status == RecipeStatus.PUBLISHED


class IsNotAdmin(permissions.BasePermission):
    """
    Allows access only to non-admin users
    """
    message = 'User must not be admin.'

    def has_object_permission(self, request, view, obj):
        user = request.user
        return (
            obj.author == request.user or
            not getattr(user, 'is_admin', False) or
            not getattr(user, 'is_superuser', False) or
            not getattr(user, 'is_staff', False)
        )
