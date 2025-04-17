from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import (
    main_view,
    user_auth_view,
    coming_soon_view,
)


urlpatterns = [
    # Main
    path('', main_view, name='main'),

    # Auth
    path('auth/', user_auth_view, name='user-auth'),
    path('auth/logout/', coming_soon_view, name='user-logout'),
    path('auth/password-reset/', coming_soon_view, name='password-reset'),
    path('auth/password-reset-confirm/<uidb64>/<token>/', coming_soon_view, name='password-reset-confirm'),

    # User
    path('user/', coming_soon_view, name='user-detail'),

    # Recipes
    # TODO: path('recipes/', recipe_list_view, name='recipe-list'),
    path('recipes/', coming_soon_view, name='recipe-list'),
    # TODO: path('recipes/random/', recipe_random_view, name='recipe-random'),
    path('recipes/random/', coming_soon_view, name='recipe-random'),
    # TODO: path('recipes/create/', recipe_create_view, name='recipe-create'),
    path('recipes/create/', coming_soon_view, name='recipe-create'),
    # TODO: path('recipes/<int:recipe_id>/', recipe_detail_view, name='recipe-detail'),
    path('recipes/<int:recipe_id>/', coming_soon_view, name='recipe-detail'),
    # TODO: path('recipes/<int:recipe_id>/update/', recipe_update_view, name='recipe-update'),
    path('recipes/<int:recipe_id>/update/', coming_soon_view, name='recipe-update'),
    # TODO: path('recipes/<int:recipe_id>/delete/', recipe_delete_view, name='recipe-delete'),
    path('recipes/<int:recipe_id>/delete/', coming_soon_view, name='recipe-delete'),
    # TODO: path('recipes/<int:recipe_id>/rate/', recipe_rate_view, name='recipe-rate'),
    path('recipes/<int:recipe_id>/rate/', coming_soon_view, name='recipe-rate'),
    # TODO: path('recipes/<int:recipe_id>/export/', recipe_export_view, name='recipe-export'),
    path('recipes/<int:recipe_id>/export/<str:format>/', coming_soon_view, name='recipe-export'),  # format = txt|pdf|json

    # Misc
    # TODO: path('feedback/', feedback_view, name='feedback'),
    path('feedback/', coming_soon_view, name='feedback'),
    path('coming-soon/', coming_soon_view, name='coming-soon'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
