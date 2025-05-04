from rest_framework import generics, views, status, permissions
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication

from apps.users.authentication import TokenAuthentication
from apps.users.permissions import (
    IsAdmin,
    IsVerifiedAndNotBanned,
)
from apps.recipes.models import (
    Recipe,
)
from apps.recipes.serializers.recipe import (
    RecipeSerializer,
    RecipeCreateSerializer,
)


class RecipeCreateView(generics.CreateAPIView):
    """
    Create a new recipe

    Creates a new recipe associated with the authenticated user
    """
    queryset = Recipe.objects.all()
    serializer_class = RecipeCreateSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsVerifiedAndNotBanned]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        recipe = serializer.save()

        recipe_serializer = RecipeSerializer(recipe, context={'request': request})
        return Response(
            {
                'recipe': recipe_serializer.data,
                'detail': 'Recipe created successfully.',
            },
            status=status.HTTP_201_CREATED,
        )


class RecipeListView(generics.ListAPIView):
    """
    GET /recipes/?tag=<str:tag_name>
    GET /recipes/?search=<str:query>
    GET /recipes/?sort=<date>
    """
    pass


class RecipeAdminListView(generics.ListAPIView):
    """
    Only Admins
    GET /recipes/?tag=<str:tag_name>
    GET /recipes/?search=<str:query>
    GET /recipes/?sort=<date>
    """
    pass


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
