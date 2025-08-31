import random
import requests

from django.conf import settings
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.utils.encoding import force_str
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers, exceptions
from rest_framework.reverse import reverse
from allauth.socialaccount.models import SocialAccount

from apps.users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'email',
            'username',
            'description',
            'avatar',
            'date_joined',
            'last_login',
            'is_active',
            'is_staff',
            'is_superuser',
            'is_banned',
        ]


class UserProfileSerializer(serializers.ModelSerializer):
    date_joined = serializers.DateTimeField(
        format='%Y-%m-%d %H:%M:%S',
        read_only=True,
    )
    last_login = serializers.DateTimeField(
        format='%Y-%m-%d %H:%M:%S',
        read_only=True,
    )
    url = serializers.HyperlinkedIdentityField(
        view_name='user-public-detail',
        lookup_field='username',
    )

    class Meta:
        model = User
        fields = [
            'url',
            'id',
            'email',
            'username',
            'description',
            'avatar',
            'date_joined',
            'last_login',
            'is_banned',
        ]
        read_only_fields = [
            'id',
            'email',
            'date_joined',
            'last_login',
            'is_banned',
        ]


class UserPublicProfileSerializer(serializers.ModelSerializer):
    date_joined = serializers.DateTimeField(
        format='%Y-%m-%d %H:%M:%S',
        read_only=True,
    )
    last_login = serializers.DateTimeField(
        format='%Y-%m-%d %H:%M:%S',
        read_only=True,
    )

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'description',
            'avatar',
            'date_joined',
            'last_login',
        ]
        read_only_fields = fields


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
    )

    class Meta:
        model = User
        fields = [
            'email',
            'username',
            'password',
        ]
        extra_kwargs = {
            'password': {'write_only': True, 'required': True},
            'email': {'validators': []},
            'username': {'validators': []},
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email already exists.')
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('Username already exists.')
        return value

    def create(self, validated_data):
        email = validated_data['email']
        password = validated_data['password']
        username = validated_data.get('username') or ''

        if not username:
            base_username = email.split('@', 1)[0]

            if not User.objects.filter(username=base_username).exists():
                username = base_username
            else:
                max_attempts = 10
                for _ in range(max_attempts):
                    new_username = f'{base_username}{random.randint(1, 9999):04d}'
                    if not User.objects.filter(username=new_username).exists():
                        username = new_username
                        break
                else:
                    raise serializers.ValidationError({'username': 'Could not generate a unique username.'})

        user = User.objects.create_user(
            email=email,
            username=username,
            password=password,
            description='',
            avatar='',
        )
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    url_delete = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'email',
            'username',
            'description',
            'avatar',
            'url_delete',
        ]

    def get_url_delete(self, obj):
        request = self.context.get('request')
        return reverse('user-delete', request=request)

    def to_internal_value(self, data):
        """
        Raise validation error if unknown fields are passed
        """
        allowed = set(self.fields) - {
            field for field, type_ in self.fields.items()
            if isinstance(type_, serializers.SerializerMethodField)
        }
        incoming = set(data)

        unknown_fields = incoming - allowed
        if unknown_fields:
            raise serializers.ValidationError({
                field: 'This field is not allowed.' for field in unknown_fields
            })

        return super().to_internal_value(data)


class UserLoginSerializer(serializers.Serializer):
    email_or_username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, attrs):
        request = self.context.get('request')
        email_or_username = attrs.get('email_or_username')
        password = attrs.get('password')

        user = None

        try:
            if '@' in email_or_username:
                user_obj = User.objects.get(email=email_or_username)
            else:
                user_obj = User.objects.get(username=email_or_username)

            user = authenticate(
                request=request,
                username=user_obj.email,
                password=password,
            )
        except User.DoesNotExist:
            pass

        if not user:
            raise exceptions.AuthenticationFailed('Unable to log in with provided credentials.')

        attrs['user'] = user
        return attrs


class GoogleAuthSerializer(serializers.Serializer):
    code = serializers.CharField()

    def validate_code(self, code):
        response = requests.post(
            'https://oauth2.googleapis.com/token',
            data={
                'code': code,
                'client_id': settings.GOOGLE_OAUTH2_CLIENT_ID,
                'client_secret': settings.GOOGLE_OAUTH2_CLIENT_SECRET,
                'redirect_uri': settings.GOOGLE_OAUTH2_CALLBACK_URL,
                'grant_type': 'authorization_code',
            }
        )
        if response.status_code != 200:
            raise serializers.ValidationError('Failed to fetch access token')

        access_token = response.json().get('access_token')
        if not access_token:
            raise serializers.ValidationError('Access token not found')

        self.access_token = access_token
        return code

    def validate(self, attrs):
        user_info = self.get_user_info()
        user = self.get_or_create_user(user_info)

        attrs['user'] = user
        return attrs

    def get_user_info(self):
        response = requests.get(
            'https://www.googleapis.com/oauth2/v3/userinfo',
            headers={'Authorization': f'Bearer {self.access_token}'}
        )
        user_info = response.json() if response.status_code == 200 else None

        if not user_info:
            raise serializers.ValidationError('Failed to fetch user info')

        return user_info

    def get_or_create_user(self, user_info):
        User = get_user_model()
        email = user_info.get('email')
        if not email:
            raise serializers.ValidationError('Email not provided by Google')
        sub = user_info.get('sub')
        if not sub:
            raise serializers.ValidationError('User ID (sub) not found')

        try:
            return SocialAccount.objects.get(provider='google', uid=sub).user
        except SocialAccount.DoesNotExist:
            pass

        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'username': email.split('@')[0],
                'description': '',
                'avatar': user_info.get('picture', ''),
            }
        )

        if created:
            user.set_unusable_password()
            user.save()

        SocialAccount.objects.create(
            provider='google',
            uid=sub,
            user=user,
            extra_data={
                'access_token': self.access_token,
                'extra_data': user_info,
            }
        )

        return user


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value, is_active=True)
        except User.DoesNotExist:
            raise serializers.ValidationError('No active user found with this email.')
        return value

    def validate(self, attrs):
        email = attrs.get('email')
        try:
            user = User.objects.get(email=email, is_active=True)
            attrs['user'] = user
        except User.DoesNotExist:
            raise serializers.ValidationError('No active user found with this email.')
        return attrs


class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField(write_only=True)
    code = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    confirm_new_password = serializers.CharField(write_only=True)

    def validate_uid(self, value):
        try:
            decoded = force_str(urlsafe_base64_decode(value))
            return decoded
        except Exception:
            raise serializers.ValidationError("Invalid UID format")

    def validate_code(self, value):
        try:
            decoded = force_str(urlsafe_base64_decode(value))
            return decoded
        except Exception:
            raise serializers.ValidationError("Invalid reset code format")

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_new_password']:
            raise serializers.ValidationError({"confirm_new_password": "Passwords do not match"})

        try:
            validate_password(attrs['new_password'])
        except DjangoValidationError as e:
            raise serializers.ValidationError({"new_password": e.messages})

        return attrs
