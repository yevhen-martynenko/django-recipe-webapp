from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import (
    # main_view,
    user_register_view,
    # coming_soon_view,
)


urlpatterns = [
    # TODO: path('', user_register_view, name='main'),
    # TODO: path('user/', user_detail_view, name='user-detail'),
    path('register/', user_register_view, name='user-register'),
    # TODO: path('register/restore-password/', user_register_view, name='user-restore-password'),
    # TODO: path('recipes/', recipe_list_view, name='recipe-list'),
    # TODO: path('recipes/<int:recipe_id>', recipe_detail_view, name='recipe-detail'),
    # TODO: path('recipes/<int:recipe_id>/create', recipe_update_view, name='recipe-create'),
    # TODO: path('recipes/<int:recipe_id>/update', recipe_update_view, name='recipe-update'),
    # path('coming-soon/', coming_soon_view, name='coming-soon'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
