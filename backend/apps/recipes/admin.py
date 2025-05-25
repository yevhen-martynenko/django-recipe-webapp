from django.contrib import admin
from django.utils.text import slugify

from apps.recipes.models import (
    Recipe,
    RecipeBlock,
    RecipeSpecialBlock,
    RecipeReport,
    Tag,
)


@admin.action(description='ban: set True')
def make_banned(modeladmin, request, queryset):
    queryset.update(is_banned=True)


@admin.action(description='ban: set False')
def remove_banned(modeladmin, request, queryset):
    queryset.update(is_banned=False)


@admin.action(description='featured: set True')
def make_featured(modeladmin, request, queryset):
    queryset.update(is_featured=True)


@admin.action(description='featured: set False')
def remove_featured(modeladmin, request, queryset):
    queryset.update(is_featured=False)


class InlineRecipeBlock(admin.TabularInline):
    model = RecipeBlock
    extra = 1
    verbose_name_plural = 'Recipe Blocks'
    classes = ['collapse']


class InlineSpecialRecipeBlock(admin.TabularInline):
    model = RecipeSpecialBlock
    extra = 1
    verbose_name_plural = 'Special Recipe Blocks'
    classes = ['collapse']


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'status',
        'author',
        'is_banned',
        'is_featured',
        'published_at',
    )
    list_filter = (
        'status',
        'is_banned',
        'is_featured',
        'is_deleted',
    )
    search_fields = ('title', 'description', 'slug')
    ordering = ['-published_at']
    readonly_fields = (
        'id', 'author',
        'title', 'status', 'description', 'final_image', 'source_url',
        'calories', 'protein', 'fat', 'carbs',
        'created_at', 'updated_at', 'published_at',
        'is_deleted', 'deleted_at',
        'is_private', 'views_count', 'likes_count',
    )
    actions = (
        make_banned,
        remove_banned,
        make_featured,
        remove_featured,
    )
    fieldsets = (
        (None, {
            'fields': (
                'id',
                'title',
                'slug',
                'description',
                'final_image',
                'source_url',
                'tags',
            )
        }),
        ('Macronutrients', {
            'fields': (
                'calories',
                'protein',
                'fat',
                'carbs',
            )
        }),
        ('Status & SEO', {
            'fields': (
                'status',
                'is_private',
                'is_banned',
                'is_featured',
                'is_deleted',
                'deleted_at',
                'meta_title',
                'meta_description',
            )
        }),
        ('Timestamps', {
            'fields': (
                'created_at',
                'updated_at',
                'published_at',
            )
        }),
    )
    inlines = [InlineRecipeBlock, InlineSpecialRecipeBlock]


@admin.register(RecipeReport)
class RecipeReportAdmin(admin.ModelAdmin):
    list_display = (
        'recipe',
        'user',
        'status',
        'created_at',
    )
    list_filter = (
        'status',
        'created_at',
    )
    search_fields = ('recipe__title', 'user__username', 'description')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    autocomplete_fields = ('recipe', 'user')
    readonly_fields = (
        'id', 'recipe', 'user',
        'reason', 'created_at',
    )
    list_select_related = ('recipe', 'user')

    fieldsets = (
        (None, {
            'fields': (
                'recipe',
                'user',
                'status',
                'created_at',
                'reason',
                'response',
            ),
        }),
    )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    readonly_fields = ('id', 'slug')
    ordering = ('name',)

    fieldsets = (
        (None, {
            'fields': (
                'id',
                'name',
                'slug',
            )
        }),
    )

    def save_model(self, request, obj, form, change):
        if not obj.slug or change:
            obj.slug = slugify(obj.name)
        super().save_model(request, obj, form, change)
