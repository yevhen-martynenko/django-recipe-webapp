import pytest

from rest_framework.exceptions import ValidationError

from apps.users.serializers import UserUpdateSerializer


@pytest.mark.django_db
def test_user_update_serializer_valid_data(registered_user):
    serializer = UserUpdateSerializer(registered_user)

    data = serializer.data
    assert data['email'] == registered_user.email
    assert data['username'] == registered_user.username
    assert 'url_delete' in data


@pytest.mark.django_db
def test_user_update_serializer_with_unknown_fields():
    data = {
        'email': 'user@test.com',
        'unknown_field': 'not allowed',
    }
    serializer = UserUpdateSerializer(data=data)

    with pytest.raises(ValidationError) as e:
        serializer.is_valid(raise_exception=True)

    assert 'unknown_field' in e.value.detail
    assert e.value.detail['unknown_field'] == 'This field is not allowed.'
