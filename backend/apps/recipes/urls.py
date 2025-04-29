from django.urls import path

from .views import (
    recipe_create_view,
    recipe_view,
    random_recipe_view,
    recipe_export_view,
    recipe_favorite_view,
    recipe_like_view,
    recipe_list_view,
    recipe_statistics_view,
    tag_list_view,
    tag_detail_view,
)


urlpatterns = [
    path('', recipe_create_view, name='recipe-create'),
    path('list/', recipe_list_view, name='recipe-list'),
    path('random/', random_recipe_view, name='recipe-random'),

    path('<uuid:id>/', recipe_view, name='recipe-detail-update-delete'),
    path('<uuid:id>/export/', recipe_export_view, name='recipe-export'),
    path('<uuid:id>/favorite/', recipe_favorite_view, name='recipe-favorite'),
    path('<uuid:id>/like/', recipe_like_view, name='recipe-like'),
    path('<uuid:id>/statistics/', recipe_statistics_view, name='recipe-statistics'),

    path('tags/', tag_list_view, name='tag-list'),
    path('tags/<str:tag_name>/', tag_detail_view, name='tag-detail'),
]
