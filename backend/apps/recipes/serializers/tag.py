from rest_framework import serializers

from apps.recipes.models import Tag


class TagSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='tag-detail',
        lookup_field='slug',
    )

    class Meta:
        model = Tag
        fields = [
            'url',
            'id',
            'name',
        ]
        read_only_fields = [
            'url',
            'id',
        ]
