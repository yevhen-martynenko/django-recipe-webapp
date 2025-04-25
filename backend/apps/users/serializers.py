import random

from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers, exceptions
from rest_framework.reverse import reverse

from .models import User


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
