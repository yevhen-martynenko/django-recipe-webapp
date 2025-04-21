from rest_framework import generics, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from django.contrib.auth import login, logout

from .models import User
from .serializers import (
    UserSerializer,
    UserProfileSerializer,
    UserPublicProfileSerializer,
    UserRegisterSerializer,
    UserUpdateSerializer,
    UserLoginSerializer,
)
from .permissions import (
    IsOwner,
    IsAdmin,
    IsVerifiedAndNotBanned,
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
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [permissions.IsAdminUser, IsAdmin]


class UserDetailUpdateView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserProfileSerializer
        return UserUpdateSerializer

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)


class UserPublicDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserPublicProfileSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsVerifiedAndNotBanned]
    lookup_field = 'username'

    def get_object(self):
        try:
            user = User.objects.get(username=self.kwargs['username'])
            return user
        except User.DoesNotExist:
            raise NotFound(detail="User with the given username does not exist")


class UserDeleteView(generics.DestroyAPIView):
    queryset = User.objects.all()
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_object(self):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)

        return Response(status=status.HTTP_204_NO_CONTENT)


class UserLoginView(generics.CreateAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        login(request, user)

        return Response(
            {
                'user': UserSerializer(user, context={'request': request}).data,
            },
            status=status.HTTP_200_OK,
        )


class UserLogoutView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if hasattr(request.user, 'auth_token'):
            request.user.auth_token.delete()

        logout(request)
        return Response(
            {"detail": "Successfully logged out"},
            status=status.HTTP_200_OK
        )


user_register_view = UserRegisterView.as_view()
user_list_view = UserListView.as_view()
user_detail_update_view = UserDetailUpdateView.as_view()
user_public_detail_view = UserPublicDetailView.as_view()
user_delete_view = UserDeleteView.as_view()
user_login_view = UserLoginView.as_view()
user_logout_view = UserLogoutView.as_view()
