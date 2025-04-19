from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import (
    user_register_view,
    user_list_view,
    user_detail_update_view,
    user_delete_view,
)


urlpatterns = [
    path('', user_detail_update_view, name='user-detail-update'),
    path('register/', user_register_view, name='user-register'),
    path('<str:username>/', user_detail_update_view, name='user-detail-update'),
    path('<str:username>/delete/', user_delete_view, name='user-delete'),
    path('list/', user_list_view, name='user-list'),
]
