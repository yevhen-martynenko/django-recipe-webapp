from django.db.models import Q, Count
from rest_framework import generics, views, status, permissions
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from django_filters.rest_framework import DjangoFilterBackend

from apps.users.authentication import TokenAuthentication
from apps.users.permissions import (
    IsAdmin,
    IsVerifiedAndNotBanned,
)
from apps.recipes.models import (
    Recipe,
    RecipeStatus,
    RecipeBlock,
    RecipeSpecialBlock,
    Like,
    View,
    RecipeReport,
)
from apps.recipes.serializers.recipe import (
    RecipeSerializer,
    RecipeAdminSerializer,
    RecipeMinimalSerializer,
    RecipeCreateSerializer,
    DeletedRecipeSerializer,
    RecipeBanSerializer,
    RecipeStatisticsSerializer,
    RecipeReportSerializer,
)
from apps.recipes.filters import (
    RecipeFilter,
    RecipeAdminFilter,
)


class RecipeCreateView(generics.CreateAPIView):
    """
    Create a new recipe

    Creates a new recipe associated with the authenticated user, including optional
    content blocks and structured special blocks
    """
    queryset = Recipe.objects.all()
    serializer_class = RecipeCreateSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsVerifiedAndNotBanned]

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        blocks = data.pop('blocks', [])
        special_blocks = data.pop('special_blocks', [])

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        recipe = serializer.save()

        for block in blocks:
            RecipeBlock.objects.create(
                recipe=recipe,
                type=block.get('type', RecipeBlock.TEXT),
                content=block.get('content', ''),
                image=block.get('image', None),
                order=block.get('order', 0),
            )

        for block in special_blocks:
            RecipeSpecialBlock.objects.create(
                recipe=recipe,
                type=block.get('type'),
                content=block.get('content', {}),
                order=block.get('order', 0),
            )

        recipe_serializer = RecipeSerializer(recipe, context={'request': request})
        return Response(
            {
                'recipe': recipe_serializer.data,
                'detail': 'Recipe created successfully.',
            },
            status=status.HTTP_201_CREATED,
        )


class NoFilterBrowsableAPIRenderer(BrowsableAPIRenderer):
    def get_filter_form(self, data, view, request):
        return None


class BaseRecipeListView(generics.ListAPIView):
    """
    Base view for listing recipes with filtering by tag, search, and sort

    Optional query parameters:
    - ?tag=<tag_name>: Filter recipes by tag
    - ?search=<query>: Full-text search in recipe title or description
    - ?sort=<field>: Sort recipes by a given field (e.g., created_at, -created_at)
    - ?<field>=<value>: Filter recipes by a given field

    Override 'permission_classes', 'serializer_class' and 'fiterset_class' in subclasses.
    """
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    renderer_classes = [NoFilterBrowsableAPIRenderer, JSONRenderer]
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        queryset = Recipe.objects.annotate(
            view_count=Count('views'),
            like_count=Count('likes')
        )
        if not self.request.query_params.get('sort'):
            queryset = queryset.filter(is_deleted=False)
        return queryset

    def get(self, request, *args, **kwargs):
        tag = request.query_params.get('tag')
        search = request.query_params.get('search')
        sort = request.query_params.get('sort')

        if tag:
            return self.list_by_tag(request, tag.lower())
        if search:
            return self.list_by_search(request, search.lower())
        if sort:
            return self.list_by_sort(request, sort.lower())

        return super().list(request, *args, **kwargs)

    def list_by_tag(self, request, tag):
        queryset = self.get_queryset().filter(tags__name__iexact=tag)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def list_by_search(self, request, query):
        queryset = self.get_queryset().filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def list_by_sort(self, request, sort):
        queryset = self.get_queryset().order_by(sort)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class RecipeAdminListView(BaseRecipeListView):
    """
    Admin view for listing recipes with full access

    Optional query parameters:
    - ?tag=<tag_name>: Filter recipes by tag
    - ?search=<query>: Full-text search in recipe title or description
    - ?sort=<field>: Sort recipes by a given field (e.g., created_at, -created_at)
    - ?<field>=<value>: Filter recipes by a given field
    """
    serializer_class = RecipeAdminSerializer
    permission_classes = [permissions.IsAdminUser, IsAdmin]
    filterset_class = RecipeAdminFilter


class RecipeListView(BaseRecipeListView):
    """
    Public user view for listing recipes

    Optional query parameters:
    - ?tag=<tag_name>: Filter recipes by tag
    - ?search=<query>: Full-text search in recipe title or description
    - ?sort=<field>: Sort recipes by a given field (e.g., created_at, -created_at)
    - ?<field>=<value>: Filter recipes by a given field
    """
    serializer_class = RecipeMinimalSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = RecipeFilter


class RandomRecipeView(generics.RetrieveAPIView):
    """
    GET /recipes/random/ - Get a random recipe
    """
    pass


class RecipeDetailView(generics.RetrieveAPIView):
    """
    GET /recipes/<id:uuid>/ - View Specific Recipe
    """
    pass


class RecipeUpdateView(generics.UpdateAPIView):
    """
    PUT /recipes/<id:uuid>/ - Update Specific Recipe
    """
    pass


class RecipeDeleteView(generics.DestroyAPIView):
    """
    DELETE /recipes/<id:uuid>/ - Delete Specific Recipe
    """
    pass


class DeletedRecipeListView(generics.ListAPIView):
    """
    GET /recipes/deleted/ - Admin/Owner views deleted recipes
    """
    pass


class RecipeRestoreView(generics.RetrieveAPIView):
    """
    POST /recipes/<id:uuid>/restore/ - Restore Specific Recipe
    """
    pass


class RecipeExportView(generics.RetrieveAPIView):
    """
    GET /recipes/<id:uuid>/export/?format=pdf - Save as PDF
    GET /recipes/<id:uuid>/export/?format=txt - Save as TXT
    GET /recipes/<id:uuid>/export/?format=json - Save as JSON
    """
    pass


class RecipeReportView(generics.RetrieveAPIView):
    """
    POST /recipes/<id:uuid>/report/ - Report Specific Recipe
    """
    pass


class RecipeBanView(generics.RetrieveAPIView):
    """
    POST /recipes/<id:uuid>/ban/ - Ban Specific Recipe
    """
    pass


class RecipeLikeView(generics.RetrieveAPIView):
    """
    POST /recipes/<id:uuid>/like/ - Like Specific Recipe
    """
    pass


class RecipeStatisticsView(generics.RetrieveAPIView):
    """
    GET /recipes/<id:uuid>/statistics/ - Admin/Owner views statistics
    """
    pass


recipe_create_view = RecipeCreateView.as_view()
recipe_list_view = RecipeListView.as_view()
recipe_admin_list_view = RecipeAdminListView.as_view()
random_recipe_view = RandomRecipeView.as_view()

recipe_detail_view = RecipeDetailView.as_view()
recipe_update_view = RecipeUpdateView.as_view()
recipe_delete_view = RecipeDeleteView.as_view()
deleted_recipe_list_view = DeletedRecipeListView.as_view()
recipe_restore_view = RecipeRestoreView.as_view()
recipe_export_view = RecipeExportView.as_view()
recipe_report_view = RecipeReportView.as_view()
recipe_ban_view = RecipeBanView.as_view()
recipe_like_view = RecipeLikeView.as_view()
recipe_statistics_view = RecipeStatisticsView.as_view()
