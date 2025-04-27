import pytest
from django.contrib.auth import get_user_model
from rest_framework.exceptions import AuthenticationFailed
from apps.users.serializers import UserLoginSerializer

User = get_user_model()


@pytest.mark.django_db
def test_login_serializer_valid_with_email(registered_user):
    data = {
        'email_or_username': registered_user.email,
        'password': 'Password019283',
    }

    serializer = UserLoginSerializer(data=data)
    assert serializer.is_valid()
    assert serializer.validated_data['user'] == registered_user


@pytest.mark.django_db
def test_login_serializer_valid_with_username(registered_user):
    data = {
        'email_or_username': registered_user.username,
        'password': 'Password019283',
    }

    serializer = UserLoginSerializer(data=data)
    assert serializer.is_valid()
    assert serializer.validated_data['user'] == registered_user


@pytest.mark.django_db
def test_login_serializer_invalid_credentials(registered_user):
    data = {
        'email_or_username': registered_user.email,
        'password': 'wrongpassword'
    }

    serializer = UserLoginSerializer(data=data, context={'request': None})

    with pytest.raises(AuthenticationFailed) as e:
        serializer.is_valid(raise_exception=True)

    assert str(e.value) == 'Unable to log in with provided credentials.'
