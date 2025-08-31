from django.contrib import admin
from django.utils import timezone

from apps.users.models import (
    User,
    ActivationCode,
)


@admin.action(description='verify: set True')
def verify_users(modeladmin, request, queryset):
    queryset.update(is_verified=True)


@admin.action(description='verify: set False')
def unverify_users(modeladmin, request, queryset):
    queryset.update(is_verified=False)


@admin.action(description='ban: set True')
def ban_users(modeladmin, request, queryset):
    queryset.update(is_banned=True)


@admin.action(description='ban: set False')
def unban_users(modeladmin, request, queryset):
    queryset.update(is_banned=False)


@admin.action(description='active: set True')
def activate_users(modeladmin, request, queryset):
    queryset.update(is_active=True)


@admin.action(description='active: set False')
def deactivate_users(modeladmin, request, queryset):
    queryset.update(is_active=False)


@admin.action(description='superuser: set True')
def make_superuser(modeladmin, request, queryset):
    queryset.update(is_superuser=True)


@admin.action(description='superuser: set False')
def remove_superuser(modeladmin, request, queryset):
    queryset.update(is_superuser=False)


@admin.action(description='staff: set True')
def make_staff(modeladmin, request, queryset):
    queryset.update(is_staff=True)


@admin.action(description='staff: set False')
def remove_staff(modeladmin, request, queryset):
    queryset.update(is_staff=False)


@admin.action(description='admin: set True')
def make_admin(modeladmin, request, queryset):
    queryset.update(is_admin=True)


@admin.action(description='admin: set False')
def remove_admin(modeladmin, request, queryset):
    queryset.update(is_admin=False)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'email',
        'username',
        'is_active',
        'is_verified',
        'is_banned',
        'is_admin',
        'is_staff',
        'is_superuser',
        'date_joined'
    )
    list_filter = (
        'is_active',
        'is_banned',
        'is_verified',
        'is_admin',
        'is_staff',
        'is_superuser',
    )
    search_fields = ('email', 'username')
    ordering = ('-date_joined',)
    readonly_fields = (
        'id', 'email', 'password', 'description', 'avatar',
        'date_joined', 'last_login',
    )
    actions = (
        verify_users,
        unverify_users,
        ban_users,
        unban_users,
        activate_users,
        deactivate_users,
        make_superuser,
        remove_superuser,
        make_staff,
        remove_staff,
        make_admin,
        remove_admin,
    )

    fieldsets = (
        (None, {
            'fields': (
                'id',
                'username',
                'email',
                'password',
            )
        }),
        ('Profile', {
            'fields': (
                'description',
                'avatar',
            )
        }),
        ('Info', {
            'fields': (
                'date_joined',
                'last_login',
            )
        }),
        ('Permissions', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'is_admin',
                'is_banned',
                'is_verified',
            )
        }),
    )

    def has_delete_permission(self, request, obj=None):
        if obj and obj.is_superuser:
            return False
        return super().has_delete_permission(request, obj)


@admin.action(description='activation: +1 day')
def extend_activation_1(modeladmin, request, queryset):
    for obj in queryset:
        obj.expires_at += timezone.timedelta(days=1)
        obj.save()


@admin.action(description='activation: +7 day')
def extend_activation_7(modeladmin, request, queryset):
    for obj in queryset:
        obj.expires_at += timezone.timedelta(days=7)
        obj.save()


@admin.action(description='activation: expire now')
def expire(modeladmin, request, queryset):
    for obj in queryset:
        obj.expires_at = timezone.now() - timezone.timedelta(seconds=1)
        obj.save()


@admin.register(ActivationCode)
class ActivationCodeAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'code',
        'expires_at',
        'is_expired',
    )
    search_fields = ('user__email', 'user__username', 'code')
    readonly_fields = (
        'user',
        'code',
        'created_at',
        'is_expired',
    )
    actions = [expire, extend_activation_1, extend_activation_7]

    fieldsets = (
        (None, {
            'fields': (
                'user',
                'code',
                'created_at',
                'expires_at',
                'is_expired',
            )
        }),
    )
