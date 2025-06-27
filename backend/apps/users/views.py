import secrets
import urllib.parse

from django.conf import settings
from django.shortcuts import redirect
from django.db import transaction
from django.contrib.auth import login, logout
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from rest_framework import generics, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, AuthenticationFailed
from rest_framework.authentication import SessionAuthentication
from rest_framework.authtoken.models import Token

from apps.users.models import User, ActivationCode
from apps.users.authentication import TokenAuthentication
from apps.users.serializers import (
    UserSerializer,
    UserProfileSerializer,
    UserPublicProfileSerializer,
    UserRegisterSerializer,
    UserUpdateSerializer,
    UserLoginSerializer,
    GoogleAuthSerializer,
)
from apps.users.permissions import (
    IsOwner,
    IsAdmin,
    IsVerifiedAndNotBanned,
)
from apps.users.tasks import (
    send_activation_email,
)


class UserRegisterView(generics.CreateAPIView):
    """
    Register a new user

    Creates a user account with the provided credentials and logs the user in

    Returns an authentication token and the user's profile data
    """
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        token, _ = Token.objects.get_or_create(user=user)
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        send_activation_email(user=user)

        user_serializer = UserProfileSerializer(user, context={'request': request})
        return Response(
            {
                'token': token.key,
                'user': user_serializer.data,
                'detail': 'User created successfully.',
            },
            status=status.HTTP_201_CREATED,
        )


class UserActivateView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        uid_encoded = request.query_params.get('uid')
        code_encoded = request.query_params.get('code')

        if not uid_encoded or not code_encoded:
            return Response(
                {'detail': 'Missing activation data'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            uid = force_str(urlsafe_base64_decode(uid_encoded))
            code = force_str(urlsafe_base64_decode(code_encoded))
        except (TypeError, ValueError, UnicodeDecodeError):
            return Response(
                {'detail': 'Invalid activation link format'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.filter(id=uid).first()
        if not user:
            return Response(
                {'detail': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        if user.is_verified:
            return Response(
                {'detail': 'Account already activated'},
                status=status.HTTP_400_BAD_REQUEST
            )

        activation_code = ActivationCode.objects.filter(user=user).first()
        if not activation_code:
            return Response(
                {'detail': 'Activation code not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        if activation_code.is_expired():
            user.delete()
            activation_code.delete()
            return Response(
                {'detail': 'Activation link has expired'},
                status=status.HTTP_410_GONE
            )
        if not secrets.compare_digest(code, activation_code.code):
            user.delete()
            activation_code.delete()
            return Response(
                {'detail': 'Invalid activation code'},
                status.HTTP_400_BAD_REQUEST
            )

        try:
            with transaction.atomic():
                user.is_verified = True
                user.save()
                activation_code.delete()
            return Response(
                {'detail': 'Account successfully activated'},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'detail': 'Account activation failed'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
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
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')

        Token.objects.filter(user=user).delete()
        token, _ = Token.objects.get_or_create(user=user)

        user_serializer = UserProfileSerializer(user, context={'request': request})

        return Response(
            {
                'token': token.key,
                'user': user_serializer.data,
                'detail': 'Successfully logged in.',
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


class UserGoogleLoginView(APIView):
    """
    Google Login

    Returns the Google OAuth2 callback URL
    """
    def get(self, request):
        params = {
            'client_id': settings.GOOGLE_OAUTH2_CLIENT_ID,
            'redirect_uri': settings.GOOGLE_OAUTH2_CALLBACK_URL,
            'response_type': 'code',
            'scope': 'openid email profile',
            'access_type': 'offline',
            'prompt': 'consent',
        }
        google_auth_url = 'https://accounts.google.com/o/oauth2/v2/auth?' + urllib.parse.urlencode(params)
        return Response({'url': google_auth_url})


class UserGoogleLoginCallbackView(APIView):
    """
    Google Login Callback

    Handles the OAuth2 callback and returns an auth token
    """
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        serializer = GoogleAuthSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')

        frontend_redirect_url = settings.FRONTEND_AFTER_GOOGLE_LOGIN_URL

        query_params = urllib.parse.urlencode({
            'token': token.key,
        })

        redirect_url = f"{frontend_redirect_url}?{query_params}"

        return redirect(redirect_url)


user_register_view = UserRegisterView.as_view()
user_activate_view = UserActivateView.as_view()
user_list_view = UserListView.as_view()
user_detail_update_view = UserDetailUpdateView.as_view()
user_public_detail_view = UserPublicDetailView.as_view()
user_delete_view = UserDeleteView.as_view()
user_login_view = UserLoginView.as_view()
user_logout_view = UserLogoutView.as_view()
user_google_login_view = UserGoogleLoginView.as_view()
user_google_login_callback_view = UserGoogleLoginCallbackView.as_view()
