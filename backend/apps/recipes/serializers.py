from rest_framework import serializers, exceptions

from .models import Recipe


class RecipeSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    url = serializers.HyperlinkedIdentityField(
        view_name='recipe-detail-update-delete',
        lookup_field='id',
    )

    class Meta:
        model = Recipe
        fields = [
            'url',
            'id',
            'author',
            'tags',
            'title',
            'description',
            'final_image',
            'source_url',
            'private',
            'views',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'url',
            'id',
            'author',
            'views',
            'created_at',
            'updated_at',
        ]

    def to_internal_value(self, data):
        """
        Raise validation error if unknown fields are passed
        """
        allowed = set(self.fields)
        incoming = set(data)

        unknown_fields = incoming - allowed
        if unknown_fields:
            raise serializers.ValidationError({
                field: 'This field is not allowed.' for field in unknown_fields
            })

        return super().to_internal_value(data)


class RecipeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = [
            'title',
            'description',
            'final_image',
            'source_url',
            'tags',
            'private',
        ]

    def validate_title(self, value):
        if len(value) > 64:
            raise exceptions.ValidationError('Title is too long')
        return value

    def validate_description(self, value):
        return value

    def create(self, validated_data):
        user = self.context['request'].user
        tags = validated_data.pop('tags', [])
        recipe = Recipe.objects.create(author=user, **validated_data)
        recipe.tags.set(tags)

        return recipe
