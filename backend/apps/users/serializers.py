import random

from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
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
        format="%Y-%m-%d %H:%M:%S",
        read_only=True
    )
    last_login = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S",
        read_only=True
    )
    url = serializers.HyperlinkedIdentityField(
        view_name='user-detail-update',
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
            'is_banned'
        ]
        read_only_fields = [
            'id',
            'email',
            'date_joined',
            'last_login',
            'is_banned'
        ]


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
    )

    class Meta:
        model = User
        fields = ['email', 'username', 'password']
        extra_kwargs = {
            'password': {'write_only': True, 'required': True},
        }

    def validate(self, attrs):
        email = attrs.get('email')
        username = attrs.get('username', '')

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email': 'Email already exists'})
        
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({'username': 'Username already exists'})
        
        return attrs

    def create(self, validated_data):
        username = validated_data['username']
        if not username:
            base_username = validated_data['email'].split('@')[0]
            max_attempts = 10
            for _ in range(max_attempts):
                new_username = f"{base_username}{random.randint(1, 9999):04d}"
                if not User.objects.filter(username=new_username).exists():
                    username = new_username
                    break
            else:
                raise serializers.ValidationError({'username': 'Could not generate a unique username'})

        user = User.objects.create_user(
            email=validated_data['email'],
            username=username,
            password=validated_data['password'],
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
        # return reverse('user-delete', kwargs={'username': obj.username}, request=request)


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        request = self.context.get('request')
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(request=request, username=email, password=password)

        if not user:
            raise serializers.ValidationError('Unable to log in with provided credentials.')

        attrs['user'] = user
        return attrs
