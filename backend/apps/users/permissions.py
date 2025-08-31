from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Allows access only to owner
    """
    message = 'User must be owner.'

    def has_object_permission(self, request, view, obj):
        owner = getattr(obj, 'user', obj)
        return owner == request.user


class IsAdmin(permissions.BasePermission):
    """
    Allows access only to admin users
    """
    message = 'User must be admin.'

    def has_permission(self, request, view):
        user = request.user
        return (
            user and
            getattr(user, 'is_authenticated', False) and
            getattr(user, 'is_active', False) and
            (
                getattr(user, 'is_admin', False) or
                getattr(user, 'is_superuser', False) or
                getattr(user, 'is_staff', False)
            )
        )


class IsVerifiedAndNotBanned(permissions.BasePermission):
    """
    Allows access only to users who are verified, active, and not banned
    """
    message = 'User must be verified, active, and not banned.'

    def has_permission(self, request, view):
        user = request.user
        return (
            user and
            getattr(user, 'is_authenticated', False) and
            getattr(user, 'is_active', False) and
            getattr(user, 'is_verified', False) and
            not getattr(user, 'is_banned', False)
        )
