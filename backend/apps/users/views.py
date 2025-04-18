from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication

from .models import User
from .serializers import (
    UserSerializer,
    UserProfileSerializer,
    UserRegisterSerializer,
)


class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        user_serializer = UserRegisterSerializer(user, context={'request': request})
        return Response(
            {
                'user': user_serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )


class UserListView(generics.ListAPIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer


user_register_view = UserRegisterView.as_view()
user_list_view = UserListView.as_view()
