import django_filters

from apps.recipes.models import Recipe


class BaseRecipeFilter(django_filters.FilterSet):
    """
    Base filter for Recipe objects
    """
    created_at = django_filters.DateFromToRangeFilter()  # ?created_at_after= & ?created_at_before=
    published_at = django_filters.DateFromToRangeFilter()

    author = django_filters.CharFilter(field_name='author__username', lookup_expr='icontains')
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    description = django_filters.CharFilter(field_name='description', lookup_expr='icontains')

    views_min = django_filters.NumberFilter(field_name='view_count', lookup_expr='gte')
    views_max = django_filters.NumberFilter(field_name='view_count', lookup_expr='lte')
    likes_min = django_filters.NumberFilter(field_name='like_count', lookup_expr='gte')
    likes_max = django_filters.NumberFilter(field_name='like_count', lookup_expr='lte')

    class Meta:
        model = Recipe
        fields = [
            'created_at',
            'published_at',

            'author',
            'title',
            'description',

            'views_min',
            'views_max',
            'likes_min',
            'likes_max',
        ]

    def filter_queryset(self, queryset):
        """
        If no filters are applied, return an empty queryset
        """
        if not self.is_valid():
            return Recipe.objects.none()

        if not self.data:
            return queryset

        if any(self.data.get(key) for key in self.filters):
            queryset = super().filter_queryset(queryset)
            return queryset if queryset.exists() else Recipe.objects.none()

        return Recipe.objects.none()


class RecipeFilter(BaseRecipeFilter):
    """
    Filter for Recipe objects
    """
    class Meta(BaseRecipeFilter.Meta):
        model = Recipe
        fields = [
            'created_at',
            'published_at',

            'author',
            'title',
            'description',

            'views_min',
            'views_max',
            'likes_min',
            'likes_max',
        ]


class RecipeAdminFilter(BaseRecipeFilter):
    """
    Admin filter for Recipe objects
    """
    is_deleted = django_filters.BooleanFilter()
    is_featured = django_filters.BooleanFilter()
    is_banned = django_filters.BooleanFilter()
    private = django_filters.BooleanFilter()
    status = django_filters.CharFilter()

    slug = django_filters.CharFilter(field_name='slug', lookup_expr='icontains')

    class Meta(BaseRecipeFilter.Meta):
        model = Recipe
        fields = [
            'is_deleted',
            'is_featured',
            'is_banned',
            'is_private',
            'status',

            'created_at',
            'published_at',

            'author',
            'title',
            'description',
            'slug',

            'views_min',
            'views_max',
            'likes_min',
            'likes_max',
        ]
