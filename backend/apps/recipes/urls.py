from django.urls import path, include

from apps.recipes.views.recipe import (
    recipe_create_view,
    recipe_list_view,
    recipe_admin_list_view,
    random_recipe_view,

    recipe_detail_view,
    recipe_update_view,
    recipe_delete_view,
    deleted_recipe_list_view,
    recipe_restore_view,
    recipe_export_view,
    recipe_report_view,
    recipe_ban_view,
    recipe_like_view,
    recipe_statistics_view,
)
from apps.recipes.views.tag import (
    tag_create_view,
    tag_list_view,
    tag_detail_view,
    tag_update_view,
    tag_delete_view,
    tag_suggest_view,
)


urlpatterns = [
    path('recipes/', include([
        path('', recipe_list_view, name='recipe-list-user'),
        path('list/', recipe_admin_list_view, name='recipe-list'),
        path('create/', recipe_create_view, name='recipe-create'),
        path('random/', random_recipe_view, name='recipe-random'),
        path('deleted/', deleted_recipe_list_view, name='recipe-deleted'),

        path('<slug:slug>/', include([
            path('', recipe_detail_view, name='recipe-detail'),
            path('update/', recipe_update_view, name='recipe-update'),
            path('delete/', recipe_delete_view, name='recipe-delete'),
            path('restore/', recipe_restore_view, name='recipe-restore'),
            path('export/', recipe_export_view, name='recipe-export'),
            path('report/', recipe_report_view, name='recipe-report'),
            path('ban/', recipe_ban_view, name='recipe-ban'),
            path('like/', recipe_like_view, name='recipe-like'),
            path('statistics/', recipe_statistics_view, name='recipe-statistics'),
        ])),
    ])),

    path('tags/', include([
        path('', tag_list_view, name='tag-list'),
        path('create/', tag_create_view, name='tag-create'),

        path('<slug:slug>/', include([
            path('', tag_detail_view, name='tag-detail'),
            path('update/', tag_update_view, name='tag-update'),
            path('delete/', tag_delete_view, name='tag-delete'),
            path('suggest/', tag_suggest_view, name='tag-suggest'),
        ])),
    ])),
]
