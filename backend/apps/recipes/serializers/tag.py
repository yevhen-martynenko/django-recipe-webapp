from rest_framework import serializers

from apps.recipes.models import Tag, TagSuggestion
from apps.users.serializers import UserSerializer


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


class TagSuggestionSerializer(serializers.ModelSerializer):
    suggested_by = UserSerializer(read_only=True)
    reviewed_by = UserSerializer(read_only=True)
    created_tag = TagSerializer(read_only=True)

    class Meta:
        model = TagSuggestion
        fields = [
            'id',
            'suggested_name',
            'description',
            'status',
            'suggested_by',
            'created_tag',

            'review_by',
            'review_notes',

            'created_at',
            'updated_at',
        ]


class TagSuggestionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagSuggestion
        fields = [
            'suggested_name',
            'description',
        ]

    def validate_suggested_name(self, value):
        """Validate the suggested tag name"""
        value = value.strip().lower()

        if len(value) < 2:
            raise serializers.ValidationError('Tag name must be at least 2 characters long')
        if len(value) > 64:
            raise serializers.ValidationError('Tag name cannot exceed 64 characters')

        if Tag.objects.filter(name__iexact=value).exists():
            raise serializers.ValidationError('This tag already exists')

        if TagSuggestion.objects.filter(
            suggested_name__iexact=value,
            status='pending'
        ).exists():
            raise serializers.ValidationError('This tag is already suggested and pending review')

        return value
