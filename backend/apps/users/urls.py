from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import (
    user_register_view,
    user_list_view,
    user_detail_update_view,
    user_delete_view,
    user_login_view,
)


urlpatterns = [
    path('user/', user_detail_update_view, name='user-detail-update'),
    path('user/<str:username>/', user_detail_update_view, name='user-detail-update'),
    path('user/<str:username>/delete/', user_delete_view, name='user-delete'),
    path('list/', user_list_view, name='user-list'),

    path('register/', user_register_view, name='user-register'),
    path('login/', user_login_view, name='user-login'),
]
