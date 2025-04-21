from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

from .views import (
    user_register_view,
    user_list_view,
    user_detail_update_view,
    user_public_detail_view,
    user_delete_view,
    user_login_view,
    user_logout_view,
)


urlpatterns = [
    path('users/', include([
        path('', user_list_view, name='user-list'),
        path('me/', user_detail_update_view, name='user-detail-update'),
        path('me/delete/', user_delete_view, name='user-delete'),
        path('<str:username>/', user_public_detail_view, name='user-public-detail'),
    ])),

    path('auth/', include([
        path('register/', user_register_view, name='user-register'),
        path('login/', user_login_view, name='user-login'),
        path('logout/', user_logout_view, name='user-logout'),
    ])),
]
