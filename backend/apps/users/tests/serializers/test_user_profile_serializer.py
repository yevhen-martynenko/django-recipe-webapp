import pytest

from apps.users.serializers import UserProfileSerializer, UserPublicProfileSerializer


@pytest.mark.django_db
def test_user_profile_serializer_valid_data(registered_user):
    serializer = UserProfileSerializer(registered_user, context={'request': None})
    data = serializer.data
    assert data['email'] == registered_user.email
    assert data['username'] == registered_user.username
    assert 'url' in data
    assert data['url'].endswith(f'/users/view/{registered_user.username}/')
    assert 'date_joined' in data
    assert 'last_login' in data


@pytest.mark.django_db
def test_public_profile_serializer_valid_data(registered_user):
    serializer = UserPublicProfileSerializer(registered_user, context={'request': None})
    data = serializer.data
    assert 'emain' not in data
    assert data['username'] == registered_user.username
    assert 'date_joined' in data
    assert 'last_login' in data
