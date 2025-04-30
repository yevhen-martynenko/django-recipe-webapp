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
from .serializers import (
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


class RecipeView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET /recipes/<id:uuid>/ - View specific recipe
    PATCH /recipes/<id:uuid>/ - Update recipe
    DELETE /recipes/<id:uuid>/ - Delete recipe
    """
    pass


class RandomRecipeView(generics.RetrieveAPIView):
    """
    GET /recipes/random/ - Get a random recipe
    """
    pass


class RecipeExportView(generics.RetrieveAPIView):
    """
    GET /recipes/<id:uuid>/export/?format=pdf - Save as PDF
    GET /recipes/<id:uuid>/export/?format=txt - Save as TXT
    GET /recipes/<id:uuid>/export/?format=json - Save as JSON
    """
    pass


class RecipeFavoriteView(generics.RetrieveAPIView):
    """
    POST /recipes/<id:uuid>/favorite/ - Favorite a recipe (toggle)
    """
    pass


class RecipeLikeView(views.APIView):
    """
    POST /recipes/<id:uuid>/like/ - Like a recipe
    DELETE /recipes/<id:uuid>/like/ - Unlike a recipe
    """
    pass


class RecipeListView(generics.ListAPIView):
    """
    GET /recipes/?tag=<str:tag_name>
    GET /recipes/?search=<str:query>
    GET /recipes/?sort=<date>
    """
    pass


class RecipeStatisticsView(generics.RetrieveAPIView):
    """
    GET /recipes/<id:uuid>/statistics/ - Admin/Owner views statistics
    """
    pass


class TagListView(generics.ListAPIView):
    """
    GET /tags/ - List All Tags
    """
    pass


class TagDetailView(generics.RetrieveAPIView):
    """
    GET /tags/<str:tag_name>/ - View Specific Tag
    """
    pass


recipe_create_view = RecipeCreateView.as_view()
recipe_view = RecipeView.as_view()
random_recipe_view = RandomRecipeView.as_view()
recipe_export_view = RecipeExportView.as_view()
recipe_favorite_view = RecipeFavoriteView.as_view()
recipe_like_view = RecipeLikeView.as_view()
recipe_list_view = RecipeListView.as_view()
recipe_statistics_view = RecipeStatisticsView.as_view()
tag_list_view = TagListView.as_view()
tag_detail_view = TagDetailView.as_view()
