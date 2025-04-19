from django.urls import path
from .views import (
    user_register_view,
    user_list_view,
    user_detail_update_view,
)


urlpatterns = [
    path('', user_detail_update_view, name='user-detail-update'),
    path('register/', user_register_view, name='user-register'),
    path('delete/', user_detail_update_view, name='user-delete'),
    path('<str:username>/', user_detail_update_view, name='user-detail-update'),
    path('list/', user_list_view, name='user-list'),
]
