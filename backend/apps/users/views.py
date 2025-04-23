from django.conf import settings
from django.contrib.auth import login, logout
from rest_framework import generics, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, AuthenticationFailed
from rest_framework.authentication import SessionAuthentication
from rest_framework.authtoken.models import Token

from .models import User
from .authentication import TokenAuthentication
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
    """
    Register a new user

    Creates a user account with the provided credentials and logs the user in

    Returns an authentication token and the user's profile data
    """
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        user_serializer = UserProfileSerializer(user, context={'request': request})
        token, _ = Token.objects.get_or_create(user=user)

        login(request, user)

        return Response(
            {
                'token': token.key,
                'user': user_serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )


class UserListView(generics.ListAPIView):
    """
    List all user profiles (admin only)

    Returns full profile data for all users
    """
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAdminUser, IsAdmin]


class UserDetailUpdateView(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update the authenticated user's profile

    - GET: Returns the current user's profile data
    - PUT/PATCH: Update profile data of the authenticated user
    """
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserProfileSerializer
        return UserUpdateSerializer


class UserPublicDetailView(generics.RetrieveAPIView):
    """
    Retrieve a public profile of a user by username (accessible if the user is verified and not banned)
    """
    queryset = User.objects.all()
    serializer_class = UserPublicProfileSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsVerifiedAndNotBanned]
    lookup_field = 'username'

    def get_object(self):
        try:
            user = User.objects.get(username=self.kwargs['username'])
            return user
        except User.DoesNotExist:
            raise NotFound(detail='User with the given username does not exist.')


class UserDeleteView(generics.DestroyAPIView):
    """
    Delete user account

    Deletes the authenticated user account and logs the user out
    """
    queryset = User.objects.all()
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_object(self):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        Token.objects.filter(user=user).delete()
        self.perform_destroy(user)

        logout(request)

        return Response(
            {
                'detail': 'No Content: Account deleted successfully.'
            },
            status=status.HTTP_204_NO_CONTENT,
        )


class UserLoginView(generics.CreateAPIView):
    """
    Authenticate a user

    Logs in the user, regenerates the authentication token, and returns the token with the user's profile data
    """
    serializer_class = UserLoginSerializer
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
        except AuthenticationFailed:
            return Response(
                {'non_field_errors': ['Unable to log in with provided credentials.']},
                status=status.HTTP_401_UNAUTHORIZED
            )

        user = serializer.validated_data['user']
        login(request, user)

        Token.objects.filter(user=user).delete()
        token, _ = Token.objects.get_or_create(user=user)

        user_serializer = UserProfileSerializer(user, context={'request': request})

        return Response(
            {
                'token': token.key,
                'user': user_serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class UserLogoutView(APIView):
    """
    Log out a user

    Log out the authenticated user and deletes the current authentication token
    """
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if hasattr(request.user, 'auth_token'):
            request.user.auth_token.delete()
        Token.objects.filter(user=request.user).delete()

        logout(request)

        return Response(
            {
                'detail': 'Successfully logged out.',
            },
            status=status.HTTP_200_OK,
        )


user_register_view = UserRegisterView.as_view()
user_list_view = UserListView.as_view()
user_detail_update_view = UserDetailUpdateView.as_view()
user_public_detail_view = UserPublicDetailView.as_view()
user_delete_view = UserDeleteView.as_view()
user_login_view = UserLoginView.as_view()
user_logout_view = UserLogoutView.as_view()
