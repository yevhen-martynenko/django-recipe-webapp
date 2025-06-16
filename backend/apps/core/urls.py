from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from apps.core.views.auth import (
    auth_view,
    activate_view,
    auth_password_reset_view,
    auth_password_reset_confirm_view,
)
from apps.core.views.users import (
    user_detail_view,
    user_me_detail_view,
    user_me_delete_view,  # BUG: ?????
)
from apps.core.views.recipes import (
    recipe_list_view,
    recipe_create_view,
    recipe_detail_view,
    recipe_update_view,
    recipe_restore_view,
    recipe_report_view,
    random_recipe_detail_view,
)
from apps.core.views.misc import (
    main_view,
    coming_soon_view,
    feedback_view,
    site_map_view,
)


urlpatterns = [
    # Main
    path('', main_view, name='main'),

    # Auth
    path('auth/', auth_view, name='user-auth'),
    path('auth/activate/', activate_view, name='user-activate'),
    path('auth/password-reset/', auth_password_reset_view, name='password-reset'),
    path('auth/password-reset-confirm/<uidb64>/<token>/', auth_password_reset_confirm_view, name='password-reset-confirm'),

    # User
    path('users/me/', user_me_detail_view, name='user-update'),
    path('users/me/delete/', user_me_delete_view, name='user-delete'),
    path('users/view/<str:username>/', user_detail_view, name='user-view'),

    # Recipes
    path('recipes/', recipe_list_view, name='recipe-list'),
    path('recipes/create/', recipe_create_view, name='recipe-create'),
    path('recipes/random/', random_recipe_detail_view, name='recipe-random'),
    path('recipes/view/<slug:slug>/', recipe_detail_view, name='recipe-detail'),
    path('recipes/view/<slug:slug>/update/', recipe_update_view, name='recipe-update'),
    path('recipes/view/<slug:slug>/restore/', recipe_restore_view, name='recipe-restore'),
    path('recipes/view/<slug:slug>/report/', recipe_report_view, name='recipe-report'),
    # path('recipes/view/<slug:slug>/export/<str:format>/', coming_soon_view, name='recipe-export'),  # format = txt|pdf|json

    # Tags
    # path('tags/', coming_soon_view, name='tag-list'),
    # path('tags/create/', coming_soon_view, name='tag-create'),
    # path('tags/view/<slug:slug>/', coming_soon_view, name='tag-detail'),
    # path('tags/view/<slug:slug>/update/', coming_soon_view, name='tag-update'),
    # path('tags/view/<slug:slug>/delete/', coming_soon_view, name='tag-delete'),
    # path('tags/view/<slug:slug>/suggest/', coming_soon_view, name='tag-suggest'),

    # Misc
    path('feedback/', feedback_view, name='feedback'),
    path('coming-soon/', coming_soon_view, name='coming-soon'),
    path('site-map/', site_map_view, name='site-map'),
    # path('privacy-policy/', coming_soon_view, name='privacy-policy'),
    # path('terms-and-conditions/', coming_soon_view, name='terms-and-conditions'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
