from django.urls import path
from .views import (
    user_register_view,
    user_list_view,
)


urlpatterns = [
    path('register/', user_register_view, name='user-register'),
    path('list/', user_list_view, name='user-list'),
]
