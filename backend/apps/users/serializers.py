import random

from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

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

    class Meta:
        model = User
        fields = [
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
